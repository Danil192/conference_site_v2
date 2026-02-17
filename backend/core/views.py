from rest_framework import viewsets
from .models import (
    Konferentsiya, Uchastnik, Prozhivanie, Transfer, Doklad,
    Otkaz, UchastnikTransfer, ProzhivanieTransfer, Programma, Program, Sekciya
)
from .serializers import (
    KonferentsiyaSerializer, UchastnikSerializer, ProzhivanieSerializer,
    TransferSerializer, DokladSerializer, OtkazSerializer,
    UchastnikTransferSerializer, ProzhivanieTransferSerializer, 
    ProgrammaSerializer, ProgramSerializer, SekciyaSerializer
)


class KonferentsiyaViewSet(viewsets.ModelViewSet):
    queryset = Konferentsiya.objects.all()
    serializer_class = KonferentsiyaSerializer


class SekciyaViewSet(viewsets.ModelViewSet):
    queryset = Sekciya.objects.all()
    serializer_class = SekciyaSerializer


class ProzhivanieViewSet(viewsets.ModelViewSet):
    queryset = Prozhivanie.objects.all()
    serializer_class = ProzhivanieSerializer


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer


class UchastnikViewSet(viewsets.ModelViewSet):
    queryset = Uchastnik.objects.all()
    serializer_class = UchastnikSerializer


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = Program.objects.all()
    serializer_class = ProgramSerializer


class DokladViewSet(viewsets.ModelViewSet):
    queryset = Doklad.objects.all()
    serializer_class = DokladSerializer


class OtkazViewSet(viewsets.ModelViewSet):
    queryset = Otkaz.objects.all()
    serializer_class = OtkazSerializer


class UchastnikTransferViewSet(viewsets.ModelViewSet):
    queryset = UchastnikTransfer.objects.all()
    serializer_class = UchastnikTransferSerializer


class ProzhivanieTransferViewSet(viewsets.ModelViewSet):
    queryset = ProzhivanieTransfer.objects.all()
    serializer_class = ProzhivanieTransferSerializer


class ProgrammaViewSet(viewsets.ModelViewSet):
    queryset = Programma.objects.all()
    serializer_class = ProgrammaSerializer