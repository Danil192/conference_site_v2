from django.contrib import admin
from .models import (
    Konferentsiya, Uchastnik, Prozhivanie, Transfer, 
    Doklad, Otkaz, Sekciya, Program, Programma,
    UchastnikTransfer, ProzhivanieTransfer, UchastnikProzhivanie,
    Tarif, Platezh, Schet,
    EmailShablon, UvedomlenieLog,
    ProfilPolzovatelya
)


@admin.register(Konferentsiya)
class KonferentsiyaAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'data_nachala', 'data_okonchaniya', 'status', 'created_at')
    list_filter = ('status', 'data_nachala')
    search_fields = ('nazvanie',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Sekciya)
class SekciyaAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'created_at')
    search_fields = ('nazvanie',)


@admin.register(Prozhivanie)
class ProzhivanieAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'turbaza_nazvanie', 'kolvo_domikov', 'kategoriya_nomerov', 
                    'stoimost', 'vmestimost', 'mesta_zanyaty', 'mesta_svobodnye')
    list_filter = ('kategoriya_nomerov',)
    search_fields = ('nazvanie',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('tip_transfera', 'mesto_vstrechi', 'vmestimost', 'mesta_zanyaty', 'mesta_svobodnye')
    list_filter = ('tip_transfera',)
    search_fields = ('mesto_vstrechi',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Uchastnik)
class UchastnikAdmin(admin.ModelAdmin):
    list_display = ('familiya', 'name', 'email', 'status_uchastnika', 'konferentsiya', 
                    'sektsiya', 'nuzhen_transfer', 'tarif', 'oplata_polnaya') 
    list_filter = ('status_uchastnika', 'konferentsiya', 'organizatsiya', 'sektsiya')
    search_fields = ('familiya', 'name', 'email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('ФИО и контакты', {
            'fields': ('familiya', 'name', 'otchestvo', 'email', 'telefon')
        }),
        ('Организационные данные', {
            'fields': ('organizatsiya', 'gorod', 'doljnost', 'uchenaya_stepen', 'sektsiya', 'nuzhen_transfer')
        }),
        ('Участие в конференции', {
            'fields': ('konferentsiya', 'status_uchastnika', 'kommentarii')
        }),
        ('Финансы', {
            'fields': ('tarif', 'oplata_polnaya'),
            'classes': ('collapse',)
        }),
        ('Мета', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(UchastnikProzhivanie)
class UchastnikProzhivanieAdmin(admin.ModelAdmin):
    list_display = ('uchastnik', 'prozhivanie', 'nomer_komnaty', 'data_zaseleniya', 'data_vyseleniya')
    list_filter = ('prozhivanie',)
    search_fields = ('uchastnik__familiya', 'uchastnik__name')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'konferentsiya', 'data_sozdaniya')
    list_filter = ('konferentsiya',)
    search_fields = ('nazvanie', 'opisanie')


@admin.register(Doklad)
class DokladAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'status_doklada', 'uchastnik', 'data_podachi', 'konferentsiya')
    list_filter = ('status_doklada', 'konferentsiya', 'data_podachi')
    search_fields = ('nazvanie', 'uchastnik__familiya')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Otkaz)
class OtkazAdmin(admin.ModelAdmin):
    list_display = ('uchastnik', 'doklad', 'status_otkaza', 'konferentsiya', 'created_at')
    list_filter = ('status_otkaza', 'konferentsiya')
    search_fields = ('uchastnik__familiya', 'doklad__nazvanie')


@admin.register(UchastnikTransfer)
class UchastnikTransferAdmin(admin.ModelAdmin):
    list_display = ('uchastnik', 'transfer', 'pribitye', 'otpravlenie')
    list_filter = ('transfer',)
    search_fields = ('uchastnik__familiya',)


@admin.register(ProzhivanieTransfer)
class ProzhivanieTransferAdmin(admin.ModelAdmin):
    list_display = ('prozhivanie', 'transfer')
    search_fields = ('prozhivanie__nazvanie',)


@admin.register(Programma)
class ProgrammaAdmin(admin.ModelAdmin):
    list_display = ('program', 'uchastnik', 'doklad', 'sekciya', 'ne_vystupaet', 
                    'vremya_nachala', 'vremya_okonchaniya', 'pomeshchenie')
    list_filter = ('program', 'vremya_nachala', 'sekciya')
    search_fields = ('doklad__nazvanie', 'uchastnik__familiya', 'sekciya__nazvanie')
    ordering = ('vremya_nachala',)
    readonly_fields = ('created_at', 'updated_at')


# ========== ФИНАНСОВЫЙ МОДУЛЬ ==========

@admin.register(Tarif)
class TarifAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'konferentsiya', 'stoimost', 'created_at')
    list_filter = ('konferentsiya',)
    search_fields = ('nazvanie', 'opisanie')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Platezh)
class PlatezhAdmin(admin.ModelAdmin):
    list_display = ('uchastnik', 'summa', 'data_platezha', 'status')
    list_filter = ('status', 'data_platezha')
    search_fields = ('uchastnik__familiya', 'uchastnik__email')
    readonly_fields = ('data_platezha', 'created_at')


@admin.register(Schet)
class SchetAdmin(admin.ModelAdmin):
    list_display = ('nomer', 'uchastnik', 'summa', 'data_vystavleniya', 'status')
    list_filter = ('status', 'data_vystavleniya')
    search_fields = ('nomer', 'uchastnik__familiya')
    readonly_fields = ('data_vystavleniya', 'created_at', 'updated_at')


# ========== УВЕДОМЛЕНИЯ ==========

@admin.register(EmailShablon)
class EmailShablonAdmin(admin.ModelAdmin):
    list_display = ('nazvanie', 'tip', 'created_at')
    list_filter = ('tip',)
    search_fields = ('nazvanie', 'tema')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(UvedomlenieLog)
class UvedomlenieLogAdmin(admin.ModelAdmin):
    list_display = ('uchastnik', 'email', 'tema', 'data_otpravki', 'status')
    list_filter = ('status', 'data_otpravki')
    search_fields = ('email', 'tema', 'uchastnik__familiya')
    readonly_fields = ('data_otpravki',)


# ========== РОЛИ ==========

@admin.register(ProfilPolzovatelya)
class ProfilPolzovatelyaAdmin(admin.ModelAdmin):
    list_display = ('user', 'rol', 'telefon', 'created_at')
    list_filter = ('rol',)
    search_fields = ('user__username', 'user__email', 'telefon')
    filter_horizontal = ('konferentsii',)
    readonly_fields = ('created_at', 'updated_at')