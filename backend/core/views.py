from rest_framework import viewsets, permissions
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


class KonferentsiyaViewSet(viewsets.ModelViewSet):
    queryset = Konferentsiya.objects.all()
    serializer_class = KonferentsiyaSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.SearchFilter']
    filterset_fields = ['status']
    search_fields = ['nazvanie']


class SekciyaViewSet(viewsets.ModelViewSet):
    queryset = Sekciya.objects.all()
    serializer_class = SekciyaSerializer
    search_fields = ['nazvanie']


class ProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = Prozhivanie.objects.all()
    serializer_class = ProzhivanieSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.SearchFilter']
    filterset_fields = ['kategoriya_nomerov']
    search_fields = ['nazvanie', 'turbaza_nazvanie']


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.SearchFilter']
    filterset_fields = ['tip_transfera']
    search_fields = ['mesto_vstrechi']


class UchastnikViewSet(viewsets.ModelViewSet):
    queryset = Uchastnik.objects.all()
    serializer_class = UchastnikSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.SearchFilter']
    filterset_fields = ['status_uchastnika', 'konferentsiya', 'sektsiya']
    search_fields = ['familiya', 'name', 'email', 'organizatsiya']


class UchastnikProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = UchastnikProzhivanie.objects.all()
    serializer_class = UchastnikProzhivanieSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['uchastnik', 'prozhivanie']


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.SearchFilter']
    filterset_fields = ['konferentsiya']
    search_fields = ['nazvanie']


class DokladViewSet(viewsets.ModelViewSet):
    queryset = Doklad.objects.all()
    serializer_class = DokladSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.SearchFilter']
    filterset_fields = ['status_doklada', 'konferentsiya', 'uchastnik']
    search_fields = ['nazvanie']


class OtkazViewSet(viewsets.ModelViewSet):
    queryset = Otkaz.objects.all()
    serializer_class = OtkazSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['status_otkaza', 'konferentsiya']
    search_fields = ['uchastnik__familiya', 'prichina']


class UchastnikTransferViewSet(viewsets.ModelViewSet):
    queryset = UchastnikTransfer.objects.all()
    serializer_class = UchastnikTransferSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['uchastnik', 'transfer']


class ProzhivanieTransferViewSet(viewsets.ModelViewSet):
    queryset = ProzhivanieTransfer.objects.all()
    serializer_class = ProzhivanieTransferSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['prozhivanie', 'transfer']


class ProgrammaViewSet(viewsets.ModelViewSet):
    queryset = Programma.objects.all()
    serializer_class = ProgrammaSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend', 
                       'rest_framework.filters.OrderingFilter']
    filterset_fields = ['program', 'sekciya']
    ordering_fields = ['vremya_nachala', 'nomer_v_programme']
    ordering = ['vremya_nachala']


# ========== ФИНАНСОВЫЙ МОДУЛЬ ==========

class TarifViewSet(viewsets.ModelViewSet):
    queryset = Tarif.objects.all()
    serializer_class = TarifSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['konferentsiya']


class PlatezhViewSet(viewsets.ModelViewSet):
    queryset = Platezh.objects.all()
    serializer_class = PlatezhSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['uchastnik', 'status']


class SchetViewSet(viewsets.ModelViewSet):
    queryset = Schet.objects.all()
    serializer_class = SchetSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['uchastnik', 'status']


# ========== УВЕДОМЛЕНИЯ ==========

class EmailShablonViewSet(viewsets.ModelViewSet):
    queryset = EmailShablon.objects.all()
    serializer_class = EmailShablonSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['tip']


class UvedomlenieLogViewSet(viewsets.ModelViewSet):
    queryset = UvedomlenieLog.objects.all()
    serializer_class = UvedomlenieLogSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['uchastnik', 'status']


# ========== РОЛИ ==========

class ProfilPolzovatelyaViewSet(viewsets.ModelViewSet):
    queryset = ProfilPolzovatelya.objects.all()
    serializer_class = ProfilPolzovatelyaSerializer
    filter_backends = ['django_filters.rest_framework.DjangoFilterBackend']
    filterset_fields = ['rol']