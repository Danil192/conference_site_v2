import re
import html
import openpyxl
from django.db import transaction
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from datetime import datetime
from .permissions import AllowAnyIfDebug, IsAdminOrOrganizer, IsAuthenticatedReadOnly
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from datetime import timedelta
from xhtml2pdf import pisa
from io import BytesIO
from xhtml2pdf.default import DEFAULT_CSS
from xhtml2pdf.files import pisaFileObject
import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import io
from django.conf import settings

from .models import (
    Konferentsiya, Uchastnik, Prozhivanie, Transfer, Doklad,
    Otkaz, UchastnikTransfer, ProzhivanieTransfer, Programma, Program, Sekciya,
    UchastnikProzhivanie, Tarif, Platezh, Schet,
    EmailShablon, UvedomlenieLog, ProfilPolzovatelya
)
from .serializers import (
    KonferentsiyaSerializer, UchastnikSerializer, ProzhivanieSerializer,
    TransferSerializer, DokladSerializer, OtkazSerializer,
    UchastnikTransferSerializer, ProzhivanieTransferSerializer,
    ProgrammaSerializer, ProgramSerializer, SekciyaSerializer,
    UchastnikProzhivanieSerializer, TarifSerializer, PlatezhSerializer, SchetSerializer,
    EmailShablonSerializer, UvedomlenieLogSerializer, ProfilPolzovatelyaSerializer
)


# ========== КЛАССЫ ПРАВ ДОСТУПА ==========

class IsAuthenticatedReadOnly(permissions.BasePermission):
    """
    Все аутентифицированные могут читать, писать только админы/организаторы
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Чтение доступно всем авторизованным
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Запись только для суперпользователей
        if request.user.is_superuser:
            return True
        
        # Проверка роли через профиль
        if hasattr(request.user, 'profilpolzovatelya'):
            return request.user.profilpolzovatelya.rol in ['admin', 'organizer']
        
        return False


class IsAdminOrOrganizer(permissions.BasePermission):
    """Только администраторы и организаторы"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if request.user.is_superuser:
            return True
        
        if hasattr(request.user, 'profilpolzovatelya'):
            return request.user.profilpolzovatelya.rol in ['admin', 'organizer']
        
        return False


# ========== ИМПОРТ ==========

class ImportViewSet(viewsets.ViewSet):
    """API для импорта данных из Excel (формат ИСЭМ СО РАН)"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])  
    def participants(self, request):          
        """Импорт участников из Excel файла (формат ИСЭМ СО РАН)"""
        if 'file' not in request.FILES:
            return Response(
                {'error': 'Файл не загружен'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        excel_file = request.FILES['file']
        
        try:
            wb = openpyxl.load_workbook(excel_file)
            ws = wb.active
            rows = list(ws.iter_rows(min_row=2, values_only=True))
            
            imported_count = 0
            created_sections = []
            created_conferences = []
            errors = []
            
            STATUS_MAP = {
                'одобрена': 'подтвердил участие',
                'принята': 'подтвердил участие',
                'зарегистрирован': 'зарегистрирован',
                'отказ': 'отказался',
                'не оплатил': 'не оплатил',
                'оплатил': 'оплатил',
            }
            
            with transaction.atomic():
                for row_idx, row in enumerate(rows, start=2):
                    try:
                        if not row or all(v is None for v in row[:10]):
                            continue
                        
                        row_num = row[0] if len(row) > 0 else None
                        data_podachi = row[1] if len(row) > 1 else None
                        konferentsiya_name = str(row[2]).strip() if len(row) > 2 and row[2] else None
                        status_excel = str(row[3]).strip().lower() if len(row) > 3 and row[3] else ''
                        comment = str(row[4]).strip() if len(row) > 4 and row[4] else ''
                        familiya = str(row[5]).strip() if len(row) > 5 and row[5] else ''
                        name = str(row[6]).strip() if len(row) > 6 and row[6] else ''
                        otchestvo = str(row[7]).strip() if len(row) > 7 and row[7] else ''
                        organizatsiya = str(row[8]).strip() if len(row) > 8 and row[8] else ''
                        gorod = str(row[9]).strip() if len(row) > 9 and row[9] else ''
                        uchenaya_stepen = str(row[10]).strip() if len(row) > 10 and row[10] else ''
                        doljnost = str(row[11]).strip() if len(row) > 11 and row[11] else ''
                        telefon = str(row[12]).strip() if len(row) > 12 and row[12] else ''
                        email = str(row[13]).strip().lower() if len(row) > 13 and row[13] else ''
                        sekciya_raw = str(row[14]).strip() if len(row) > 14 and row[14] else ''
                        
                        if not email or not familiya:
                            errors.append(f'Строка {row_idx}: отсутствуют Email или Фамилия')
                            continue
                        
                        if organizatsiya and isinstance(organizatsiya, str):
                            organizatsiya = html.unescape(organizatsiya)
                        
                        if telefon:
                            telefon = re.sub(r'[^\d+]', '', telefon)
                            if telefon.startswith('8') and len(telefon) == 11:
                                telefon = '+7' + telefon[1:]
                        
                        if gorod and ';' in gorod:
                            gorod = gorod.split(';')[0].strip()
                        
                        status_uchastnika = STATUS_MAP.get(status_excel, 'зарегистрирован')
                        
                        # Находим или создаём конференцию
                        konferentsiya = None
                        if konferentsiya_name:
                            konferentsiya = Konferentsiya.objects.filter(
                                nazvanie__iexact=konferentsiya_name
                            ).first()
                            
                            if not konferentsiya:
                                conf_start_date = data_podachi
                                if hasattr(conf_start_date, 'date'):
                                    conf_start_date = conf_start_date.date()
                                elif isinstance(data_podachi, str) and data_podachi:
                                    try:
                                        conf_start_date = datetime.strptime(data_podachi, '%Y-%m-%d').date()
                                    except:
                                        conf_start_date = timezone.now().date()
                                elif not conf_start_date:
                                    conf_start_date = timezone.now().date()
                                
                                konferentsiya = Konferentsiya.objects.create(
                                    nazvanie=konferentsiya_name,
                                    status='планируется',
                                    data_nachala=conf_start_date,
                                    data_okonchaniya=conf_start_date,
                                )
                                created_conferences.append(konferentsiya_name)
                        
                        # Обработка секций
                        sekciya = None
                        if sekciya_raw:
                            section_names = [s.strip() for s in sekciya_raw.split(',') if s.strip()]
                            if section_names:
                                first_section = section_names[0]
                                sekciya, _ = Sekciya.objects.get_or_create(nazvanie=first_section)
                                for sec_name in section_names[1:]:
                                    Sekciya.objects.get_or_create(nazvanie=sec_name)
                                    if sec_name not in created_sections:
                                        created_sections.append(sec_name)
                        
                        uchastnik, created = Uchastnik.objects.update_or_create(
                            email=email,
                            defaults={
                                'familiya': familiya,
                                'name': name,
                                'otchestvo': otchestvo,
                                'organizatsiya': organizatsiya,
                                'gorod': gorod,
                                'uchenaya_stepen': uchenaya_stepen if uchenaya_stepen not in ['-', 'нет', 'отсутствует', None] else '',
                                'doljnost': doljnost,
                                'telefon': telefon,
                                'status_uchastnika': status_uchastnika,
                                'konferentsiya': konferentsiya,
                                'sektsiya': sekciya,
                                'kommentarii': comment,
                                'nuzhen_transfer': False,
                            }
                        )
                        
                        imported_count += 1
                        
                    except Exception as e:
                        errors.append(f'Строка {row_idx}: {str(e)}')
            
            return Response({
                'success': True,
                'imported': imported_count,
                'sections_created': len(set(created_sections)),
                'conferences_created': len(set(created_conferences)),
                'errors': errors[:20]
            })
            
        except Exception as e:
            return Response(
                {'error': f'Ошибка обработки файла: {str(e)}'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ========== КОНФЕРЕНЦИИ ==========

class KonferentsiyaViewSet(viewsets.ModelViewSet):
    queryset = Konferentsiya.objects.all()
    serializer_class = KonferentsiyaSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['nazvanie']


# ========== СЕКЦИИ ==========

class SekciyaViewSet(viewsets.ModelViewSet):
    queryset = Sekciya.objects.all()
    serializer_class = SekciyaSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['konferentsiya']
    search_fields = ['nazvanie']
    
    def get_queryset(self):
        """Фильтруем секции по конференции из query params"""
        queryset = Sekciya.objects.all()
        konferentsiya_id = self.request.query_params.get('konferentsiya', None)
        if konferentsiya_id:
            queryset = queryset.filter(konferentsiya_id=konferentsiya_id)
        return queryset


# ========== ПРОЖИВАНИЕ ==========

class ProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = Prozhivanie.objects.all()
    serializer_class = ProzhivanieSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['kategoriya_nomerov']
    search_fields = ['nazvanie', 'turbaza_nazvanie']


# ========== ТРАНСФЕР ==========

class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tip_transfera']
    search_fields = ['mesto_vstrechi']


# ========== УЧАСТНИКИ ==========

class UchastnikViewSet(viewsets.ModelViewSet):
    queryset = Uchastnik.objects.all()
    serializer_class = UchastnikSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status_uchastnika', 'konferentsiya', 'sektsiya']
    search_fields = ['familiya', 'name', 'email', 'organizatsiya']


# ========== СВЯЗЬ УЧАСТНИК-ПРОЖИВАНИЕ ==========

class UchastnikProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = UchastnikProzhivanie.objects.all()
    serializer_class = UchastnikProzhivanieSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'prozhivanie']


# ========== ПРОГРАММЫ ==========

class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['konferentsiya']
    search_fields = ['nazvanie']


class ProgrammaViewSet(viewsets.ModelViewSet):
    queryset = Programma.objects.all()
    serializer_class = ProgrammaSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['program', 'sekciya']
    ordering_fields = ['vremya_nachala', 'nomer_v_programme']
    ordering = ['vremya_nachala']


# ========== ДОКЛАДЫ ==========

class DokladViewSet(viewsets.ModelViewSet):
    queryset = Doklad.objects.all()
    serializer_class = DokladSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status_doklada', 'konferentsiya', 'uchastnik', 'sektsiya']
    search_fields = ['nazvanie']


# ========== ОТКАЗЫ ==========

class OtkazViewSet(viewsets.ModelViewSet):
    queryset = Otkaz.objects.all()
    serializer_class = OtkazSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status_otkaza', 'konferentsiya']
    search_fields = ['uchastnik__familiya', 'prichina']


# ========== СВЯЗИ ==========

class UchastnikTransferViewSet(viewsets.ModelViewSet):
    queryset = UchastnikTransfer.objects.all()
    serializer_class = UchastnikTransferSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'transfer']


class ProzhivanieTransferViewSet(viewsets.ModelViewSet):
    queryset = ProzhivanieTransfer.objects.all()
    serializer_class = ProzhivanieTransferSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prozhivanie', 'transfer']


# ========== ФИНАНСОВЫЙ МОДУЛЬ ==========

class TarifViewSet(viewsets.ModelViewSet):
    queryset = Tarif.objects.all()
    serializer_class = TarifSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['konferentsiya']


class PlatezhViewSet(viewsets.ModelViewSet):
    queryset = Platezh.objects.all()
    serializer_class = PlatezhSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'status']


class SchetViewSet(viewsets.ModelViewSet):
    queryset = Schet.objects.all()
    serializer_class = SchetSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'status']


# ========== УВЕДОМЛЕНИЯ ==========

class EmailShablonViewSet(viewsets.ModelViewSet):
    queryset = EmailShablon.objects.all()
    serializer_class = EmailShablonSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tip']


class UvedomlenieLogViewSet(viewsets.ModelViewSet):
    queryset = UvedomlenieLog.objects.all()
    serializer_class = UvedomlenieLogSerializer
    permission_classes = [AllowAnyIfDebug]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'status']


# ========== РОЛИ ==========

class ProfilPolzovatelyaViewSet(viewsets.ModelViewSet):
    queryset = ProfilPolzovatelya.objects.all()
    serializer_class = ProfilPolzovatelyaSerializer
    # permission_classes = [IsAdminOrOrganizer]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rol']


# ========== СТАТИСТИКА И ЛОГИСТИКА ==========

class ProzhivanieStatistikaView(APIView):
    """Статистика по проживанию для конференции"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, konferentsiya_id):
        try:
            konferentsiya = Konferentsiya.objects.get(id=konferentsiya_id)
            
            # Все варианты проживания
            prozhivaniya = Prozhivanie.objects.all()
            
            # Участники, нуждающиеся в проживании (если поле существует)
            try:
                uchastniki_nuzhdayushchiesya = Uchastnik.objects.filter(
                    konferentsiya=konferentsiya,
                    nuzhen_prozhivanie=True
                )
            except:
                uchastniki_nuzhdayushchiesya = Uchastnik.objects.filter(konferentsiya=konferentsiya)
            
            # Заселённые участники
            zaseleniye = UchastnikProzhivanie.objects.filter(
                uchastnik__konferentsiya=konferentsiya
            )
            
            stats = {
                'konferentsiya_id': konferentsiya_id,
                'konferentsiya_nazvanie': konferentsiya.nazvanie,
                
                # Общая статистика
                'total_places': sum(p.vmestimost for p in prozhivaniya),
                'occupied_places': sum(p.mesta_zanyaty for p in prozhivaniya),
                'free_places': sum(p.mesta_svobodnye for p in prozhivaniya),
                
                # Участники
                'participants_need_accommodation': uchastniki_nuzhdayushchiesya.count(),
                'participants_settled': zaseleniye.count(),
                'participants_waiting': uchastniki_nuzhdayushchiesya.count() - zaseleniye.count(),
                
                # Варианты проживания
                'accommodation_options': []
            }
            
            # Процент заполненности
            if stats['total_places'] > 0:
                stats['occupancy_percent'] = round(
                    (stats['occupied_places'] / stats['total_places']) * 100, 1
                )
            else:
                stats['occupancy_percent'] = 0
            
            # Детализация по вариантам проживания
            for proj in prozhivaniya:
                stats['accommodation_options'].append({
                    'id': proj.id,
                    'nazvanie': proj.nazvanie,
                    'tip': proj.kategoriya_nomerov,
                    'vmestimost': proj.vmestimost,
                    'mesta_zanyaty': proj.mesta_zanyaty,
                    'mesta_svobodnye': proj.mesta_svobodnye,
                    'stoimost': str(proj.stoimost),
                    'occupancy_percent': round(
                        (proj.mesta_zanyaty / proj.vmestimost * 100) if proj.vmestimost > 0 else 0, 1
                    )
                })
            
            return Response(stats)
            
        except Konferentsiya.DoesNotExist:
            return Response(
                {'error': 'Конференция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class TransferStatistikaView(APIView):
    """Статистика по трансферу для конференции"""
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, konferentsiya_id):
        try:
            konferentsiya = Konferentsiya.objects.get(id=konferentsiya_id)
            
            transfers = Transfer.objects.all()
            
            stats = {
                'konferentsiya_id': konferentsiya_id,
                'total_capacity': sum(t.vmestimost for t in transfers),
                'occupied_seats': sum(t.mesta_zanyaty for t in transfers),
                'free_seats': sum(t.mesta_svobodnye for t in transfers),
                'transfers': []
            }
            
            if stats['total_capacity'] > 0:
                stats['occupancy_percent'] = round(
                    (stats['occupied_seats'] / stats['total_capacity']) * 100, 1
                )
            else:
                stats['occupancy_percent'] = 0
            
            for transfer in transfers:
                stats['transfers'].append({
                    'id': transfer.id,
                    'tip': transfer.tip_transfera,
                    'mesto_vstrechi': transfer.mesto_vstrechi,
                    'vmestimost': transfer.vmestimost,
                    'mesta_zanyaty': transfer.mesta_zanyaty,
                    'mesta_svobodnye': transfer.mesta_svobodnye,
                    'occupancy_percent': round(
                        (transfer.mesta_zanyaty / transfer.vmestimost * 100) if transfer.vmestimost > 0 else 0, 1
                    )
                })
            
            return Response(stats)
            
        except Konferentsiya.DoesNotExist:
            return Response(
                {'error': 'Конференция не найдена'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class ZaselenieViewSet(viewsets.ViewSet):
    """Управление заселением участников"""
    permission_classes = [permissions.IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def zaselit(self, request):
        """Заселить участника в проживание"""
        uchastnik_id = request.data.get('uchastnik_id')
        prozhivanie_id = request.data.get('prozhivanie_id')
        data_zaseleniya = request.data.get('data_zaseleniya')
        data_vyseleniya = request.data.get('data_vyseleniya')
        nomer_komnaty = request.data.get('nomer_komnaty', '')
        
        try:
            uchastnik = Uchastnik.objects.get(id=uchastnik_id)
            prozhivanie = Prozhivanie.objects.get(id=prozhivanie_id)
            
            # Проверка свободных мест
            if prozhivanie.mesta_svobodnye <= 0:
                return Response(
                    {'error': 'Нет свободных мест в этом варианте проживания'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Проверка, не заселен ли уже участник
            if UchastnikProzhivanie.objects.filter(uchastnik=uchastnik).exists():
                return Response(
                    {'error': 'Участник уже заселен'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            free_places = prozhivanie.obshaya_vmestimost - prozhivanie.mesta_zanyaty
            
            if free_places <= 0:
                return Response(
                    {'error': 'Нет свободных мест'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Создаём связь
            UchastnikProzhivanie.objects.create(
                uchastnik=uchastnik,
                prozhivanie=prozhivanie,
                data_zaseleniya=data_zaseleniya or getattr(uchastnik, 'data_zaseleniya', None),
                data_vyseleniya=data_vyseleniya or getattr(uchastnik, 'data_vyseleniya', None),
                nomer_komnaty=nomer_komnaty
            )
            
            # Обновляем флаг участника (если поле существует)
            if hasattr(uchastnik, 'nuzhen_prozhivanie'):
                uchastnik.nuzhen_prozhivanie = True
                uchastnik.save()
            
            return Response({
                'success': True,
                'message': f'Участник {uchastnik.familiya} заселён в {prozhivanie.nazvanie}'
            })
            
        except Uchastnik.DoesNotExist:
            return Response(
                {'error': 'Участник не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Prozhivanie.DoesNotExist:
            return Response(
                {'error': 'Вариант проживания не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['post'])
    def vyselit(self, request):
        """Выселить участника"""
        uchastnik_id = request.data.get('uchastnik_id')
        
        try:
            uchastnik = Uchastnik.objects.get(id=uchastnik_id)
            svyaz = UchastnikProzhivanie.objects.filter(uchastnik=uchastnik).first()
            
            if not svyaz:
                return Response(
                    {'error': 'Участник не заселен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Связь удалится, освободив место (через model save/delete)
            svyaz.delete()
            
            # Обновляем флаг участника (если поле существует)
            if hasattr(uchastnik, 'nuzhen_prozhivanie'):
                uchastnik.nuzhen_prozhivanie = False
                uchastnik.save()
            
            return Response({
                'success': True,
                'message': f'Участник {uchastnik.familiya} выселен'
            })
            
        except Uchastnik.DoesNotExist:
            return Response(
                {'error': 'Участник не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    @action(detail=False, methods=['get'])
    def nezaseslennye(self, request):
        """Список участников, нуждающихся в проживании, но не заселенных"""
        konferentsiya_id = request.query_params.get('konferentsiya')
        
        try:
            queryset = Uchastnik.objects.filter(
                konferentsiya_id=konferentsiya_id
            ).exclude(
                uchastnikprozhivanie__isnull=False
            )
            
            serializer = UchastnikSerializer(queryset, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

# ========== РАССЕЛЕНИЕ ==========

class SettlementViewSet(viewsets.ViewSet):
    """Управление расселением участников"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['get'])
    def available(self, request):
        """Получить участников без проживания для конференции"""
        konferentsiya_id = request.query_params.get('konferentsiya')
        
        if not konferentsiya_id:
            return Response(
                {'error': 'Требуется параметр konferentsiya'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        participants = Uchastnik.objects.filter(
            konferentsiya_id=konferentsiya_id
        ).select_related('sektsiya')
        
        settled_ids = UchastnikProzhivanie.objects.filter(
            uchastnik__konferentsiya_id=konferentsiya_id
        ).values_list('uchastnik_id', flat=True)
        
        participants = participants.exclude(id__in=settled_ids)
        
        serializer = UchastnikSerializer(participants, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def accommodations(self, request):
        """Получить варианты проживания для конференции с группировкой"""
        konferentsiya_id = request.query_params.get('konferentsiya')
        
        if konferentsiya_id:
            prozhivaniya = Prozhivanie.objects.filter(
                konferentsiya_id=konferentsiya_id
            ).order_by('turbaza_nazvanie', 'kategoriya_nomerov')
        else:
            prozhivaniya = Prozhivanie.objects.all().order_by(
                'turbaza_nazvanie', 'kategoriya_nomerov'
            )
        
        result = {}
        for proj in prozhivaniya:
            turbaza = proj.turbaza_nazvanie or 'Без турбазы'
            if turbaza not in result:
                result[turbaza] = {
                    'name': turbaza,
                    'categories': {}
                }
            
            category = proj.kategoriya_nomerov or 'Стандарт'
            if category not in result[turbaza]['categories']:
                result[turbaza]['categories'][category] = []

            zaselennye = UchastnikProzhivanie.objects.filter(prozhivanie=proj).select_related('uchastnik')
            zaselennye_list = [
                {
                    'id': z.uchastnik.id,
                    'fio': f"{z.uchastnik.familiya} {z.uchastnik.name[0]}."
                }
                for z in zaselennye
            ]
            
            result[turbaza]['categories'][category].append({
                'id': proj.id,
                'nazvanie': proj.nazvanie,
                'vmestimost': proj.obshaya_vmestimost,
                'mesta_zanyaty': proj.mesta_zanyaty,
                'mesta_svobodnye': max(0, proj.obshaya_vmestimost - proj.mesta_zanyaty),
                'stoimost': str(proj.stoimost),
                'kolvo_domikov': proj.kolvo_domikov,
                'zaselennye': zaselennye_list
            })
        
        return Response(result)

    @action(detail=False, methods=['post'])
    def settle(self, request):
            """Заселить участника в проживание"""
            uchastnik_id = request.data.get('uchastnik_id')
            prozhivanie_id = request.data.get('prozhivanie_id')
            
            try:
                uchastnik = Uchastnik.objects.get(id=uchastnik_id)
                prozhivanie = Prozhivanie.objects.get(id=prozhivanie_id)
                
                if UchastnikProzhivanie.objects.filter(uchastnik=uchastnik).exists():
                    return Response(
                        {'error': 'Участник уже заселен'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                # --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
                # Используем obshaya_vmestimost вместо vmestimost
                free_places = prozhivanie.obshaya_vmestimost - prozhivanie.mesta_zanyaty
                
                if free_places <= 0:
                    return Response(
                        {'error': 'Нет свободных мест'},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                # -------------------------
                
                UchastnikProzhivanie.objects.create(
                    uchastnik=uchastnik,
                    prozhivanie=prozhivanie,
                )
                
                prozhivanie.refresh_from_db()
                
                return Response({
                    'success': True,
                    'message': f'{uchastnik.familiya} {uchastnik.name} заселён в {prozhivanie.nazvanie}',
                    'prozhivanie': {
                        'id': prozhivanie.id,
                        'mesta_zanyaty': prozhivanie.mesta_zanyaty,
                        # Тут тоже на всякий случай поправь расчет для ответа фронтенду:
                        'mesta_svobodnye': prozhivanie.obshaya_vmestimost - prozhivanie.mesta_zanyaty
                    }
                })
                
            except Uchastnik.DoesNotExist:
                return Response({'error': 'Участник не найден'}, status=404)
            except Prozhivanie.DoesNotExist:
                return Response({'error': 'Проживание не найдено'}, status=404)
            except Exception as e:
                return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'])
    def vacate(self, request):
        """Выселить участника"""
        uchastnik_id = request.data.get('uchastnik_id')
        
        try:
            uchastnik = Uchastnik.objects.get(id=uchastnik_id)
            svyaz = UchastnikProzhivanie.objects.filter(uchastnik=uchastnik).first()
            
            if not svyaz:
                return Response(
                    {'error': 'Участник не заселен'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            prozhivanie = svyaz.prozhivanie

            svyaz.delete()
            
            prozhivanie.refresh_from_db()
            
            return Response({
                'success': True,
                'message': f'{uchastnik.familiya} {uchastnik.name} выселен',
                'prozhivanie': {
                    'id': prozhivanie.id,
                    'mesta_zanyaty': prozhivanie.mesta_zanyaty,
                    'mesta_svobodnye': prozhivanie.vmestimost - prozhivanie.mesta_zanyaty
                }
            })
            
        except Uchastnik.DoesNotExist:
            return Response({'error': 'Участник не найден'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['get'])
    def transfers_available(self, request):
        """Получить варианты трансфера для конференции"""
        konferentsiya_id = request.query_params.get('konferentsiya')
        
        if not konferentsiya_id:
            return Response(
                {'error': 'Требуется параметр konferentsiya'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        transfers = Transfer.objects.filter(
            konferentsiya_id=konferentsiya_id
        ).order_by('tip_transfera', 'mesto_vstrechi')
        
        result = []
        for transfer in transfers:
             result.append({
                'id': transfer.id,
                'tip_transfera': transfer.tip_transfera,
                'mesto_vstrechi': transfer.mesto_vstrechi,
                
                'vmestimost': transfer.obshaya_vmestimost, 
                'mesta_zanyaty': transfer.mesta_zanyaty,
                'mesta_svobodnye': max(0, transfer.obshaya_vmestimost - transfer.mesta_zanyaty),
                
                'procent_zanyatosti': round(
                    (transfer.mesta_zanyaty / transfer.obshaya_vmestimost * 100)
                    if transfer.obshaya_vmestimost > 0 else 0, 1
                )
            })
        
        return Response(result)

    @action(detail=False, methods=['get'])
    def transfers_assigned(self, request):
        """Получить назначенных участников на трансферы"""
        konferentsiya_id = request.query_params.get('konferentsiya')
        
        if not konferentsiya_id:
            return Response(
                {'error': 'Требуется параметр konferentsiya'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        assigned = UchastnikTransfer.objects.filter(
            uchastnik__konferentsiya_id=konferentsiya_id
        ).select_related('uchastnik', 'transfer')
        
        result = [
            {
                'uchastnik_id': a.uchastnik_id,
                'transfer_id': a.transfer_id,
                'uchastnik_fio': f"{a.uchastnik.familiya} {a.uchastnik.name}",
                'transfer_tip': a.transfer.tip_transfera
            }
            for a in assigned
        ]
        
        return Response(result)

    @action(detail=False, methods=['post'], url_path='assign_transfer')
    def assign_transfer(self, request):
        """Назначить участника на трансфер"""
        uchastnik_id = request.data.get('uchastnik_id')
        transfer_id = request.data.get('transfer_id')
        
        try:
            uchastnik = Uchastnik.objects.get(id=uchastnik_id)
            transfer = Transfer.objects.get(id=transfer_id)
            
            if UchastnikTransfer.objects.filter(
                uchastnik=uchastnik,
                transfer=transfer
            ).exists():
                return Response(
                    {'error': 'Участник уже назначен на этот трансфер'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            free_places = transfer.obshaya_vmestimost - transfer.mesta_zanyaty

            if free_places <= 0:
                return Response(
                    {'error': 'Нет свободных мест в этом трансфере'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            UchastnikTransfer.objects.create(
                uchastnik=uchastnik,
                transfer=transfer
            )
            
            transfer.refresh_from_db()
            
            return Response({
                'success': True,
                'message': f'{uchastnik.familiya} {uchastnik.name} назначен на {transfer.tip_transfera}',
                'transfer': {
                    'id': transfer.id,
                    'mesta_zanyaty': transfer.mesta_zanyaty,
                    'mesta_svobodnye': transfer.obshaya_vmestimost - transfer.mesta_zanyaty
                }
            })
            
        except Uchastnik.DoesNotExist:
            return Response({'error': 'Участник не найден'}, status=404)
        except Transfer.DoesNotExist:
            return Response({'error': 'Трансфер не найден'}, status=404)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    @action(detail=False, methods=['post'], url_path='unassign_transfer')
    def unassign_transfer(self, request):
        """Отменить назначение участника на трансфер"""
        uchastnik_id = request.data.get('uchastnik_id')
        
        try:
            uchastnik = Uchastnik.objects.get(id=uchastnik_id)
            svyaz = UchastnikTransfer.objects.filter(uchastnik=uchastnik).first()
            
            if not svyaz:
                return Response(
                    {'error': 'Участник не назначен на трансфер'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            transfer = svyaz.transfer
            svyaz.delete()
            
            transfer.refresh_from_db() 
            
            return Response({
                'success': True,
                'message': f'{uchastnik.familiya} {uchastnik.name} снят с трансфера'
            })
            
        except Uchastnik.DoesNotExist:
            return Response({'error': 'Участник не найден'}, status=404)
        except Exception as e:
            # ВОТ ЗДЕСЬ БЫЛА ОШИБКА СО СКОБКОЙ:
            return Response({'error': str(e)}, status=500)


# ========== ГЕНЕРАЦИЯ PDF (ОТДЕЛЬНЫЙ КЛАСС) ==========

class ProgramPDFView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, konferentsiya_id):
        try:
            # 1. ОПРЕДЕЛЯЕМ ПУТИ К ШРИФТАМ (Указываем папку static)
            base_fonts_path = os.path.join(settings.BASE_DIR, 'static')
            regular_font = os.path.join(base_fonts_path, 'arial.ttf')
            bold_font = os.path.join(base_fonts_path, 'arialbd.ttf')

            # Проверяем наличие файлов, чтобы не было ошибки 500
            if not os.path.exists(regular_font):
                return Response({'error': f'Файл не найден по пути {regular_font}'}, status=500)

            # Регистрируем шрифты в движке
            pdfmetrics.registerFont(TTFont('ArialCustom', regular_font))
            pdfmetrics.registerFont(TTFont('ArialCustom-Bold', bold_font))

            # 2. РЕГИСТРИРУЕМ ИХ В КЭШЕ REPORTLAB
            # Важно: регистрируем под именами 'Arial' и 'Arial-Bold'
            if os.path.exists(regular_font):
                pdfmetrics.registerFont(TTFont('Arial', regular_font))
            else:
                return Response({'error': f'Файл шрифта не найден по пути {regular_font}'}, status=500)
                
            if os.path.exists(bold_font):
                pdfmetrics.registerFont(TTFont('Arial-Bold', bold_font))

            # --- Логика данных (твоя рабочая часть) ---
            conference = Konferentsiya.objects.get(id=konferentsiya_id)
            from core.models import Programma
            events = Programma.objects.filter(program__konferentsiya=conference).select_related('doklad', 'uchastnik', 'sekciya').order_by('vremya_nachala')
            
            schedule_data = {}
            for event in events:
                date_key = event.vremya_nachala.date()
                if date_key not in schedule_data: schedule_data[date_key] = {}
                sec_name = event.sekciya.nazvanie if event.sekciya else "Общая программа"
                if sec_name not in schedule_data[date_key]: schedule_data[date_key][sec_name] = []
                schedule_data[date_key][sec_name].append({
                    'time_start': event.vremya_nachala,
                    'doklad_nazvanie': event.doklad.nazvanie if event.doklad else "Мероприятие",
                    'uchastnik_fio': f"{event.uchastnik.familiya} {event.uchastnik.name}" if event.uchastnik else "Организатор",
                    'organizatsiya': event.uchastnik.organizatsiya if event.uchastnik else "",
                })

            final_schedule = []
            for date in sorted(schedule_data.keys()):
                days_sections = []
                for sec, reps in schedule_data[date].items():
                    days_sections.append({'nazvanie': sec, 'reports': reps})
                final_schedule.append({'date': date, 'sections': days_sections})

            context = {
                'conference': conference,
                'schedule_by_days': final_schedule,
                'participants_count': Uchastnik.objects.filter(konferentsiya=conference).count(),
                'sections_count': Sekciya.objects.filter(konferentsiya=conference).count(),
                'reports_count': events.count(),
                'generated_at': timezone.now()
            }
            
            # Рендеринг
            html_string = render_to_string('core/program_pdf.html', context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="program_{conference.id}.pdf"'
            
            # ГЕНЕРАЦИЯ
            pisa_status = pisa.CreatePDF(
                html_string,
                dest=response,
                encoding='utf-8'
            )
            
            if pisa_status.err:
                return HttpResponse('Ошибка генерации PDF', status=500)
            return response
            
        except Exception as e:
            import traceback
            print(traceback.format_exc())
            return Response({'error': str(e)}, status=500)