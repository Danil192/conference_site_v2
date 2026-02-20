import re
import html
import openpyxl
from django.db import transaction
from rest_framework import viewsets, filters, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

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


class ImportViewSet(viewsets.ViewSet):
    """API для импорта данных из Excel (формат ИСЭМ СО РАН)"""
    
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
                                from django.utils import timezone
                                
                                conf_start_date = data_podachi
                                if hasattr(conf_start_date, 'date'):
                                    conf_start_date = conf_start_date.date()
                                elif isinstance(data_podachi, str) and data_podachi:
                                    try:
                                        from datetime import datetime
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


class KonferentsiyaViewSet(viewsets.ModelViewSet):
    queryset = Konferentsiya.objects.all()
    serializer_class = KonferentsiyaSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['nazvanie']


class SekciyaViewSet(viewsets.ModelViewSet):
    queryset = Sekciya.objects.all()
    serializer_class = SekciyaSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['nazvanie']


class ProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = Prozhivanie.objects.all()
    serializer_class = ProzhivanieSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['kategoriya_nomerov']
    search_fields = ['nazvanie', 'turbaza_nazvanie']


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['tip_transfera']
    search_fields = ['mesto_vstrechi']


class UchastnikViewSet(viewsets.ModelViewSet):
    queryset = Uchastnik.objects.all()
    serializer_class = UchastnikSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status_uchastnika', 'konferentsiya', 'sektsiya']
    search_fields = ['familiya', 'name', 'email', 'organizatsiya']


class UchastnikProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = UchastnikProzhivanie.objects.all()
    serializer_class = UchastnikProzhivanieSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'prozhivanie']


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['konferentsiya']
    search_fields = ['nazvanie']


class DokladViewSet(viewsets.ModelViewSet):
    queryset = Doklad.objects.all()
    serializer_class = DokladSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status_doklada', 'konferentsiya', 'uchastnik']
    search_fields = ['nazvanie']


class OtkazViewSet(viewsets.ModelViewSet):
    queryset = Otkaz.objects.all()
    serializer_class = OtkazSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status_otkaza', 'konferentsiya']
    search_fields = ['uchastnik__familiya', 'prichina']


class UchastnikTransferViewSet(viewsets.ModelViewSet):
    queryset = UchastnikTransfer.objects.all()
    serializer_class = UchastnikTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'transfer']


class ProzhivanieTransferViewSet(viewsets.ModelViewSet):
    queryset = ProzhivanieTransfer.objects.all()
    serializer_class = ProzhivanieTransferSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['prozhivanie', 'transfer']


class ProgrammaViewSet(viewsets.ModelViewSet):
    queryset = Programma.objects.all()
    serializer_class = ProgrammaSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['program', 'sekciya']
    ordering_fields = ['vremya_nachala', 'nomer_v_programme']
    ordering = ['vremya_nachala']


class TarifViewSet(viewsets.ModelViewSet):
    queryset = Tarif.objects.all()
    serializer_class = TarifSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['konferentsiya']


class PlatezhViewSet(viewsets.ModelViewSet):
    queryset = Platezh.objects.all()
    serializer_class = PlatezhSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'status']


class SchetViewSet(viewsets.ModelViewSet):
    queryset = Schet.objects.all()
    serializer_class = SchetSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'status']


class EmailShablonViewSet(viewsets.ModelViewSet):
    queryset = EmailShablon.objects.all()
    serializer_class = EmailShablonSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tip']


class UvedomlenieLogViewSet(viewsets.ModelViewSet):
    queryset = UvedomlenieLog.objects.all()
    serializer_class = UvedomlenieLogSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['uchastnik', 'status']


class ProfilPolzovatelyaViewSet(viewsets.ModelViewSet):
    queryset = ProfilPolzovatelya.objects.all()
    serializer_class = ProfilPolzovatelyaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['rol']