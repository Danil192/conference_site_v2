from rest_framework import serializers
from .models import (
    Konferentsiya, Uchastnik, Prozhivanie, Transfer, Doklad,
    Otkaz, UchastnikTransfer, ProzhivanieTransfer, Programma, Program, Sekciya
)


class KonferentsiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konferentsiya
        fields = '__all__'


class SekciyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sekciya
        fields = '__all__'


class ProzhivanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prozhivanie
        fields = '__all__'


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'


class UchastnikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uchastnik
        fields = '__all__'


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class DokladSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doklad
        fields = '__all__'


class OtkazSerializer(serializers.ModelSerializer):
    class Meta:
        model = Otkaz
        fields = '__all__'


class UchastnikTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = UchastnikTransfer
        fields = '__all__'


class ProzhivanieTransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProzhivanieTransfer
        fields = '__all__'


class ProgrammaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programma
        fields = '__all__'