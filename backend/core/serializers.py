from rest_framework import serializers
from .models import (
    Konferentsiya, Uchastnik, Prozhivanie, Transfer, Doklad,
    Otkaz, UchastnikTransfer, ProzhivanieTransfer, Programma, Program, Sekciya,
    UchastnikProzhivanie, Tarif, Platezh, Schet,
    EmailShablon, UvedomlenieLog, ProfilPolzovatelya
)


class KonferentsiyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Konferentsiya
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class SekciyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sekciya
        fields = '__all__'


class ProzhivanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prozhivanie
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UchastnikProzhivanieSerializer(serializers.ModelSerializer):
    class Meta:
        model = UchastnikProzhivanie
        fields = '__all__'


class UchastnikSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uchastnik
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'


class DokladSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doklad
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


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
        read_only_fields = ('created_at', 'updated_at')


# ========== ФИНАНСОВЫЙ МОДУЛЬ ==========

class TarifSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tarif
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class PlatezhSerializer(serializers.ModelSerializer):
    class Meta:
        model = Platezh
        fields = '__all__'
        read_only_fields = ('data_platezha', 'created_at')


class SchetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schet
        fields = '__all__'
        read_only_fields = ('data_vystavleniya', 'created_at', 'updated_at')


# ========== УВЕДОМЛЕНИЯ ==========

class EmailShablonSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmailShablon
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UvedomlenieLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = UvedomlenieLog
        fields = '__all__'


# ========== РОЛИ ==========

class ProfilPolzovatelyaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilPolzovatelya
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')