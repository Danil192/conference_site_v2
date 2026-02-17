from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Konferentsiya(models.Model):
    nazvanie = models.CharField(max_length=255)
    data_nachala = models.DateField()
    data_okonchaniya = models.DateField()
    status = models.CharField(
        max_length=50,
        choices=[
            ('планируется', 'Планируется'),
            ('идет', 'Идет'),
            ('завершена', 'Завершена'),
            ('отменена', 'Отменена'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'konferentsiya'
        ordering = ['-data_nachala']
    
    def __str__(self):
        return self.nazvanie
    
    def clean(self):
        from django.core.exceptions import ValidationError
        if self.data_nachala > self.data_okonchaniya:
            raise ValidationError("Дата начала должна быть раньше даты окончания")


class Sekciya(models.Model):
    nazvanie = models.CharField(max_length=255, unique=True)
    opisanie = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'sekciya'
    
    def __str__(self):
        return self.nazvanie


class Prozhivanie(models.Model):
    nazvanie = models.CharField(max_length=255, default='Проживание')
    kategoriya_nomerov = models.CharField(max_length=100, blank=True)
    stoimost = models.DecimalField(max_digits=10, decimal_places=2)
    vmestimost = models.PositiveIntegerField(default=1)
    mesta_zanyaty = models.PositiveIntegerField(default=0)
    mesta_svobodnye = models.PositiveIntegerField(default=0)
    turbaza_nazvanie = models.CharField(max_length=255, blank=True)
    kolvo_domikov = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'prozhivanie'
    
    def __str__(self):
        return self.nazvanie


class Transfer(models.Model):
    mesto_vstrechi = models.CharField(max_length=255)
    vmestimost = models.PositiveIntegerField()
    tip_transfera = models.CharField(
        max_length=50,
        choices=[
            ('автобус', 'Автобус'),
            ('маршрутка', 'Маршрутка'),
            ('такси', 'Такси'),
            ('индивидуально', 'Индивидуально')
        ]
    )
    mesta_zanyaty = models.PositiveIntegerField(default=0)
    mesta_svobodnye = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transfer'
    
    def __str__(self):
        return f"{self.tip_transfera} — {self.mesto_vstrechi}"


class Uchastnik(models.Model):
    familiya = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    otchestvo = models.CharField(max_length=100, blank=True)
    email = models.EmailField(unique=True)
    telefon = models.CharField(max_length=20, blank=True)
    organizatsiya = models.CharField(max_length=255, blank=True)
    gorod = models.CharField(max_length=100, blank=True)
    doljnost = models.CharField(max_length=100, blank=True)
    uchenaya_stepen = models.CharField(max_length=100, blank=True)
    sektsiya = models.ForeignKey('Sekciya', on_delete=models.SET_NULL, null=True, blank=True)
    status_uchastnika = models.CharField(
        max_length=50,
        choices=[
            ('зарегистрирован', 'Зарегистрирован'),
            ('подтвердил участие', 'Подтвердил участие'),
            ('отказался', 'Отказался'),
            ('оплатил', 'Оплатил'),
            ('не оплатил', 'Не оплатил'),
        ],
        default='зарегистрирован'
    )
    kommentarii = models.TextField(blank=True)
    konferentsiya = models.ForeignKey(Konferentsiya, on_delete=models.CASCADE)
    nuzhen_transfer = models.BooleanField(default=False) 
    
    # Финансовый модуль
    tarif = models.ForeignKey('Tarif', on_delete=models.SET_NULL, null=True, blank=True)
    oplata_polnaya = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'uchastnik'
    
    def doklady_count(self):
        return self.doklad_set.count()
    
    def __str__(self):
        return f"{self.familiya} {self.name}"


class UchastnikProzhivanie(models.Model):
    """Связь участников с проживанием (многие-ко-многим)"""
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    prozhivanie = models.ForeignKey(Prozhivanie, on_delete=models.CASCADE)
    data_zaseleniya = models.DateField(blank=True, null=True)
    data_vyseleniya = models.DateField(blank=True, null=True)
    nomer_komnaty = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'uchastnik_prozhivanie'
        unique_together = ('uchastnik', 'prozhivanie')
    
    def __str__(self):
        return f"{self.uchastnik} ↔ {self.prozhivanie}"


class Program(models.Model):
    nazvanie = models.CharField(max_length=255)
    konferentsiya = models.ForeignKey(Konferentsiya, on_delete=models.CASCADE)
    opisanie = models.TextField(blank=True)
    data_sozdaniya = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'program'
    
    def __str__(self):
        return self.nazvanie


class Doklad(models.Model):
    nazvanie = models.CharField(max_length=255, default='Не выступает')
    status_doklada = models.CharField(
        max_length=50,
        choices=[
            ('на рассмотрении', 'На рассмотрении'),
            ('принят', 'Принят'),
            ('отклонен', 'Отклонен'),
            ('отложен', 'Отложен'),
        ],
        default='на рассмотрении'
    )
    data_podachi = models.DateTimeField(auto_now_add=True)
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    konferentsiya = models.ForeignKey(Konferentsiya, on_delete=models.CASCADE)
    vystupaet = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'doklad'
    
    def __str__(self):
        return self.nazvanie


class Otkaz(models.Model):
    prichina = models.TextField(blank=True)
    status_otkaza = models.CharField(
        max_length=50,
        choices=[
            ('запланирован', 'Запланирован'),
            ('подтвержден', 'Подтвержден'),
        ],
        default='запланирован'
    )
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    konferentsiya = models.ForeignKey(Konferentsiya, on_delete=models.CASCADE)
    doklad = models.ForeignKey(Doklad, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'otkaz'
    
    def __str__(self):
        return f"Отказ: {self.uchastnik}"


class UchastnikTransfer(models.Model):
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    pribitye = models.DateTimeField(blank=True, null=True)
    otpravlenie = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'uchastnik_transfer'
        unique_together = ('uchastnik', 'transfer')
    
    def __str__(self):
        return f"{self.uchastnik} ↔ {self.transfer}"


class ProzhivanieTransfer(models.Model):
    prozhivanie = models.ForeignKey(Prozhivanie, on_delete=models.CASCADE)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'prozhivanie_transfer'
        unique_together = ('prozhivanie', 'transfer')
    
    def __str__(self):
        return f"{self.prozhivanie} ↔ {self.transfer}"


class Programma(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    doklad = models.ForeignKey(Doklad, on_delete=models.SET_NULL, null=True, blank=True)
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.SET_NULL, null=True, blank=True)
    sekciya = models.ForeignKey(Sekciya, on_delete=models.SET_NULL, null=True, blank=True)
    vremya_nachala = models.DateTimeField()
    vremya_okonchaniya = models.DateTimeField()
    nomer_v_programme = models.PositiveIntegerField(default=1)
    ne_vystupaet = models.BooleanField(default=False)
    pomeshchenie = models.CharField(max_length=100, blank=True)  # ДОБАВЛЕНО
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'programma'
        ordering = ['vremya_nachala']
    
    def __str__(self):
        title = self.doklad.nazvanie if self.doklad else (str(self.uchastnik) if self.uchastnik else 'Пусто')
        return f"{title} - {self.vremya_nachala.strftime('%d.%m %H:%M')}"


# ========== ФИНАНСОВЫЙ МОДУЛЬ (НОВОЕ) ==========

class Tarif(models.Model):
    """Тарифы для конференции"""
    konferentsiya = models.ForeignKey(Konferentsiya, on_delete=models.CASCADE)
    nazvanie = models.CharField(max_length=100)  # "Студент", "Преподаватель", "Иностранный"
    stoimost = models.DecimalField(max_digits=10, decimal_places=2)
    opisanie = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'tarif'
        unique_together = ('konferentsiya', 'nazvanie')
    
    def __str__(self):
        return f"{self.nazvanie} - {self.stoimost} ₽"


class Platezh(models.Model):
    """Платежи участников"""
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    summa = models.DecimalField(max_digits=10, decimal_places=2)
    data_platezha = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('ожидаемый', 'Ожидаемый'),
            ('подтверждён', 'Подтверждён'),
            ('возврат', 'Возврат'),
        ],
        default='ожидаемый'
    )
    kommentarii = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'platezh'
        ordering = ['-data_platezha']
    
    def __str__(self):
        return f"{self.uchastnik} - {self.summa} ₽ ({self.status})"


class Schet(models.Model):
    """Счета для участников"""
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    nomer = models.CharField(max_length=50, unique=True)
    data_vystavleniya = models.DateTimeField(auto_now_add=True)
    summa = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=50,
        choices=[
            ('выставлен', 'Выставлен'),
            ('оплачен', 'Оплачен'),
            ('аннулирован', 'Аннулирован'),
        ],
        default='выставлен'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'schet'
        ordering = ['-data_vystavleniya']
    
    def __str__(self):
        return f"Счёт №{self.nomer} - {self.uchastnik}"


# ========== МОДУЛЬ УВЕДОМЛЕНИЙ (НОВОЕ) ==========

class EmailShablon(models.Model):
    """Шаблоны email уведомлений"""
    nazvanie = models.CharField(max_length=100)
    tema = models.CharField(max_length=255)
    tekst = models.TextField()
    tip = models.CharField(
        max_length=50,
        choices=[
            ('подтверждение', 'Подтверждение регистрации'),
            ('programma', 'Изменение программы'),
            ('platezh', 'Подтверждение оплаты'),
            ('napominanie', 'Напоминание'),
        ]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'email_shablon'
    
    def __str__(self):
        return self.nazvanie


class UvedomlenieLog(models.Model):
    """Лог отправленных уведомлений"""
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    email = models.EmailField()
    tema = models.CharField(max_length=255)
    data_otpravki = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=50,
        choices=[
            ('отправлено', 'Отправлено'),
            ('ошибка', 'Ошибка'),
            ('открыто', 'Открыто'),
        ]
    )
    
    class Meta:
        db_table = 'uvedomlenie_log'
        ordering = ['-data_otpravki']
    
    def __str__(self):
        return f"{self.email} - {self.tema} ({self.status})"


# ========== РОЛИ ПОЛЬЗОВАТЕЛЕЙ (НОВОЕ) ==========

class ProfilPolzovatelya(models.Model):
    """Расширение профиля пользователя Django"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Администратор'),
            ('organizer', 'Организатор'),
            ('viewer', 'Наблюдатель'),
        ],
        default='viewer'
    )
    konferentsii = models.ManyToManyField(Konferentsiya, blank=True)
    telefon = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'profil_polzovatelya'
    
    def __str__(self):
        return f"{self.user.username} ({self.rol})"