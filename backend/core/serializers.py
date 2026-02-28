from rest_framework import serializers
from .models import (
    Konferentsiya, Uchastnik, Prozhivanie, Transfer, Doklad,
    Otkaz, UchastnikTransfer, ProzhivanieTransfer, Programma, Program, Sekciya,
    UchastnikProzhivanie, Tarif, Platezh, Schet,
    EmailShablon, UvedomlenieLog, ProfilPolzovatelya
)


# ========== КОНФЕРЕНЦИИ ==========
class KonferentsiyaSerializer(serializers.ModelSerializer):
    """Сериализатор конференции с полями логистики"""
    sekciyas_count = serializers.SerializerMethodField()
    uchastniks_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Konferentsiya
        fields = [
            'id', 'nazvanie', 'data_nachala', 'data_okonchaniya', 'status',
            'trebuetsya_prozhivanie', 'mesto_provedeniya',  # НОВЫЕ ПОЛЯ
            'sekciyas_count', 'uchastniks_count',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')
    
    def get_sekciyas_count(self, obj):
        return obj.sekciyas.count()
    
    def get_uchastniks_count(self, obj):
        return obj.uchastnik_set.count()


# ========== СЕКЦИИ ==========
class SekciyaSerializer(serializers.ModelSerializer):
    """Сериализатор секции"""
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    doklady_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Sekciya
        fields = [
            'id', 'nazvanie', 'konferentsiya', 'konferentsiya_nazvanie',
            'opisanie', 'doklady_count', 'created_at'
        ]
        read_only_fields = ('created_at',)
    
    def get_doklady_count(self, obj):
        from .models import Doklad
        return Doklad.objects.filter(uchastnik__sektsiya=obj).count()


# ========== ПРОЖИВАНИЕ ==========
class ProzhivanieSerializer(serializers.ModelSerializer):
    """Сериализатор проживания с расчётом заполненности"""
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    procent_zanyatosti = serializers.SerializerMethodField()
    
    class Meta:
        model = Prozhivanie
        fields = [
            'id', 'nazvanie', 'kategoriya_nomerov', 'stoimost',
            'vmestimost', 'mesta_zanyaty', 'mesta_svobodnye',
            'turbaza_nazvanie', 'kolvo_domikov', 'konferentsiya',
            'konferentsiya_nazvanie', 'procent_zanyatosti',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'mesta_zanyaty', 'mesta_svobodnye')
    
    def get_procent_zanyatosti(self, obj):
        """Расчёт процента заполненности"""
        if obj.vmestimost == 0:
            return 0
        return round((obj.mesta_zanyaty / obj.vmestimost) * 100, 1)
    
    def create(self, validated_data):
        """При создании автоматически устанавливаем свободные места"""
        instance = super().create(validated_data)
        instance.mesta_svobodnye = instance.vmestimost
        instance.save()
        return instance


# ========== ТРАНСФЕР ==========
class TransferSerializer(serializers.ModelSerializer):
    """Сериализатор трансфера с расчётом заполненности"""
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    procent_zanyatosti = serializers.SerializerMethodField()
    
    class Meta:
        model = Transfer
        fields = [
            'id', 'mesto_vstrechi', 'vmestimost', 'tip_transfera',
            'mesta_zanyaty', 'mesta_svobodnye', 'konferentsiya',
            'konferentsiya_nazvanie', 'procent_zanyatosti',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'mesta_zanyaty', 'mesta_svobodnye')
    
    def get_procent_zanyatosti(self, obj):
        """Расчёт процента заполненности"""
        if obj.vmestimost == 0:
            return 0
        return round((obj.mesta_zanyaty / obj.vmestimost) * 100, 1)


# ========== УЧАСТНИКИ ==========
class UchastnikSerializer(serializers.ModelSerializer):
    """Сериализатор участника с полями логистики"""
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    sektsiya_nazvanie = serializers.CharField(source='sektsiya.nazvanie', read_only=True)
    tarif_nazvanie = serializers.CharField(source='tarif.nazvanie', read_only=True)
    has_prozhivanie = serializers.SerializerMethodField()
    
    class Meta:
        model = Uchastnik
        fields = [
            'id', 'familiya', 'name', 'otchestvo', 'email', 'telefon',
            'organizatsiya', 'gorod', 'doljnost', 'uchenaya_stepen',
            'sektsiya', 'sektsiya_nazvanie', 'status_uchastnika',
            'kommentarii', 'konferentsiya', 'konferentsiya_nazvanie',
            'nuzhen_transfer', 'tarif', 'tarif_nazvanie', 'oplata_polnaya',
            # НОВЫЕ ПОЛЯ ЛОГИСТИКИ
            'nuzhen_prozhivanie', 'tip_prozhivaniya', 'preferencii',
            'data_zaseleniya', 'data_vyseleniya', 'has_prozhivanie',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')
    
    def get_has_prozhivanie(self, obj):
        """Проверяет, заселен ли участник"""
        return UchastnikProzhivanie.objects.filter(uchastnik=obj).exists()


# ========== СВЯЗЬ УЧАСТНИК-ПРОЖИВАНИЕ ==========
class UchastnikProzhivanieSerializer(serializers.ModelSerializer):
    """Сериализатор связи участник-проживание"""
    uchastnik_fio = serializers.CharField(source='uchastnik.familiya', read_only=True)
    uchastnik_email = serializers.CharField(source='uchastnik.email', read_only=True)
    prozhivanie_nazvanie = serializers.CharField(source='prozhivanie.nazvanie', read_only=True)
    prozhivanie_tip = serializers.CharField(source='prozhivanie.kategoriya_nomerov', read_only=True)
    
    class Meta:
        model = UchastnikProzhivanie
        fields = [
            'id', 'uchastnik', 'uchastnik_fio', 'uchastnik_email',
            'prozhivanie', 'prozhivanie_nazvanie', 'prozhivanie_tip',
            'data_zaseleniya', 'data_vyseleniya', 'nomer_komnaty',
            'created_at'
        ]
        read_only_fields = ('created_at',)


# ========== СВЯЗЬ УЧАСТНИК-ТРАНСФЕР ==========
class UchastnikTransferSerializer(serializers.ModelSerializer):
    """Сериализатор связи участник-трансфер"""
    uchastnik_fio = serializers.CharField(source='uchastnik.familiya', read_only=True)
    transfer_mesto = serializers.CharField(source='transfer.mesto_vstrechi', read_only=True)
    transfer_tip = serializers.CharField(source='transfer.tip_transfera', read_only=True)
    
    class Meta:
        model = UchastnikTransfer
        fields = [
            'id', 'uchastnik', 'uchastnik_fio',
            'transfer', 'transfer_mesto', 'transfer_tip',
            'pribitye', 'otpravlenie', 'created_at'
        ]
        read_only_fields = ('created_at',)


# ========== ПРОГРАММА ==========
class ProgrammaSerializer(serializers.ModelSerializer):
    """Сериализатор мероприятий программы"""
    program_nazvanie = serializers.CharField(source='program.nazvanie', read_only=True)
    program_konferentsiya = serializers.IntegerField(source='program.konferentsiya.id', read_only=True)
    doklad_nazvanie = serializers.CharField(source='doklad.nazvanie', read_only=True)
    uchastnik_fio = serializers.CharField(source='uchastnik', read_only=True)
    sekciya_nazvanie = serializers.CharField(source='sekciya.nazvanie', read_only=True)
    
    class Meta:
        model = Programma
        fields = [
            'id', 'program', 'program_nazvanie', 'program_konferentsiya',
            'doklad', 'doklad_nazvanie', 'uchastnik', 'uchastnik_fio',
            'sekciya', 'sekciya_nazvanie',
            'vremya_nachala', 'vremya_okonchaniya', 'nomer_v_programme',
            'ne_vystupaet', 'pomeshchenie',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class ProgramSerializer(serializers.ModelSerializer):
    """Сериализатор контейнера программы"""
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    
    class Meta:
        model = Program
        fields = [
            'id', 'nazvanie', 'konferentsiya', 'konferentsiya_nazvanie',
            'opisanie', 'data_sozdaniya'
        ]
        read_only_fields = ('data_sozdaniya',)


# ========== ДОКЛАДЫ ==========
class DokladSerializer(serializers.ModelSerializer):
    uchastnik_fio = serializers.CharField(source='uchastnik', read_only=True)
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    sektsiya_nazvanie = serializers.CharField(source='sektsiya.nazvanie', read_only=True)
    
    class Meta:
        model = Doklad
        fields = [
            'id', 'nazvanie', 'status_doklada', 'data_podachi',
            'uchastnik', 'uchastnik_fio', 'konferentsiya', 'konferentsiya_nazvanie',
            'sektsiya', 'sektsiya_nazvanie',
            'vystupaet',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at', 'data_podachi')
    
    def get_file_url(self, obj):
        """Возвращает полный URL для файла"""
        if obj.file:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.file.url)
            return obj.file.url
        return None


# ========== ОТКАЗЫ ==========
class OtkazSerializer(serializers.ModelSerializer):
    """Сериализатор отказа"""
    uchastnik_fio = serializers.CharField(source='uchastnik', read_only=True)
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    doklad_nazvanie = serializers.CharField(source='doklad.nazvanie', read_only=True)
    
    class Meta:
        model = Otkaz
        fields = [
            'id', 'prichina', 'status_otkaza',
            'uchastnik', 'uchastnik_fio',
            'konferentsiya', 'konferentsiya_nazvanie',
            'doklad', 'doklad_nazvanie',
            'created_at'
        ]
        read_only_fields = ('created_at',)


# ========== СВЯЗЬ ПРОЖИВАНИЕ-ТРАНСФЕР ==========
class ProzhivanieTransferSerializer(serializers.ModelSerializer):
    """Сериализатор связи проживание-трансфер"""
    prozhivanie_nazvanie = serializers.CharField(source='prozhivanie.nazvanie', read_only=True)
    transfer_mesto = serializers.CharField(source='transfer.mesto_vstrechi', read_only=True)
    
    class Meta:
        model = ProzhivanieTransfer
        fields = [
            'id', 'prozhivanie', 'prozhivanie_nazvanie',
            'transfer', 'transfer_mesto',
            'created_at'
        ]
        read_only_fields = ('created_at',)


# ========== ФИНАНСОВЫЙ МОДУЛЬ ==========
class TarifSerializer(serializers.ModelSerializer):
    """Сериализатор тарифа"""
    konferentsiya_nazvanie = serializers.CharField(source='konferentsiya.nazvanie', read_only=True)
    
    class Meta:
        model = Tarif
        fields = [
            'id', 'konferentsiya', 'konferentsiya_nazvanie',
            'nazvanie', 'stoimost', 'opisanie',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')


class PlatezhSerializer(serializers.ModelSerializer):
    """Сериализатор платежа"""
    uchastnik_fio = serializers.CharField(source='uchastnik', read_only=True)
    uchastnik_email = serializers.CharField(source='uchastnik.email', read_only=True)
    
    class Meta:
        model = Platezh
        fields = [
            'id', 'uchastnik', 'uchastnik_fio', 'uchastnik_email',
            'summa', 'data_platezha', 'status', 'kommentarii',
            'created_at'
        ]
        read_only_fields = ('data_platezha', 'created_at')


class SchetSerializer(serializers.ModelSerializer):
    """Сериализатор счёта"""
    uchastnik_fio = serializers.CharField(source='uchastnik', read_only=True)
    uchastnik_email = serializers.CharField(source='uchastnik.email', read_only=True)
    
    class Meta:
        model = Schet
        fields = [
            'id', 'uchastnik', 'uchastnik_fio', 'uchastnik_email',
            'nomer', 'data_vystavleniya', 'summa', 'status',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('data_vystavleniya', 'created_at', 'updated_at')


# ========== МОДУЛЬ УВЕДОМЛЕНИЙ ==========
class EmailShablonSerializer(serializers.ModelSerializer):
    """Сериализатор email-шаблона"""
    class Meta:
        model = EmailShablon
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')


class UvedomlenieLogSerializer(serializers.ModelSerializer):
    """Сериализатор лога уведомлений"""
    uchastnik_fio = serializers.CharField(source='uchastnik', read_only=True)
    
    class Meta:
        model = UvedomlenieLog
        fields = [
            'id', 'uchastnik', 'uchastnik_fio', 'email',
            'tema', 'data_otpravki', 'status'
        ]
        read_only_fields = ('data_otpravki',)


# ========== РОЛИ ПОЛЬЗОВАТЕЛЕЙ ==========
class ProfilPolzovatelyaSerializer(serializers.ModelSerializer):
    """Сериализатор профиля пользователя"""
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    is_superuser = serializers.BooleanField(source='user.is_superuser', read_only=True)
    
    class Meta:
        model = ProfilPolzovatelya
        fields = [
            'id', 'user', 'username', 'email', 'is_superuser',
            'rol', 'telefon', 'konferentsii',
            'created_at', 'updated_at'
        ]
        read_only_fields = ('created_at', 'updated_at')