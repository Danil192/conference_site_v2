from django.db import models, transaction
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError

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
    
    # === Логистика ===
    trebuetsya_prozhivanie = models.BooleanField(
        default=False, 
        verbose_name="Требуется проживание",
        help_text="Если отмечено, для конференции организуется проживание"
    )
    mesto_provedeniya = models.CharField(
        max_length=50,
        choices=[
            ('gorod', 'Город (гостиница)'),
            ('turbase', 'Турбаза'),
            ('smeshanno', 'Смешанно'),
        ],
        default='gorod',
        verbose_name="Место проведения"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'konferentsiya'
        ordering = ['-data_nachala']

    def __str__(self):
        return self.nazvanie

    def clean(self):
        if self.data_nachala > self.data_okonchaniya:
            raise ValidationError("Дата начала должна быть раньше даты окончания")


class Sekciya(models.Model):
    nazvanie = models.CharField(max_length=255)
    konferentsiya = models.ForeignKey(
        Konferentsiya,
        on_delete=models.CASCADE,
        related_name='sekciyas'
    )
    opisanie = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sekciya'
        ordering = ['nazvanie']
        unique_together = ('nazvanie', 'konferentsiya')

    def __str__(self):
        return f"{self.nazvanie}"


class Prozhivanie(models.Model):
    nazvanie = models.CharField(max_length=255, default='Проживание')
    kategoriya_nomerov = models.CharField(max_length=100, blank=True)
    stoimost = models.DecimalField(max_digits=10, decimal_places=2)
    vmestimost = models.PositiveIntegerField(default=1)
    mesta_zanyaty = models.PositiveIntegerField(default=0)
    mesta_svobodnye = models.PositiveIntegerField(default=0)
    turbaza_nazvanie = models.CharField(max_length=255, blank=True)
    kolvo_domikov = models.PositiveIntegerField(default=0)
    
    # === Связь с конференцией ===
    konferentsiya = models.ForeignKey(
        Konferentsiya,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='prozhivaniya',
        verbose_name="Конференция"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'prozhivanie'

    def __str__(self):
        return self.nazvanie

    def save(self, *args, **kwargs):
        self.mesta_zanyaty = max(0, self.mesta_zanyaty)
        if self.mesta_zanyaty > self.vmestimost:
            self.mesta_zanyaty = self.vmestimost
        
        self.mesta_svobodnye = self.get_free_places()
        super().save(*args, **kwargs)
    
    @property
    def procent_zanyatosti(self):
        """Процент заполненности"""
        if self.vmestimost == 0:
            return 0
        return round((self.mesta_zanyaty / self.vmestimost) * 100, 1)
    
    def can_accommodate(self, count=1):
        """Проверяет, можно ли заселить указанное количество участников"""
        return (self.vmestimost - self.mesta_zanyaty) >= count
    
    def get_free_places(self):
        """Возвращает количество свободных мест"""
        return max(0, self.vmestimost - self.mesta_zanyaty)


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
    
    # === Связь с конференцией ===
    konferentsiya = models.ForeignKey(
        Konferentsiya,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='transfers',
        verbose_name="Конференция"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'transfer'

    def __str__(self):
        return f"{self.tip_transfera} — {self.mesto_vstrechi}"

    def save(self, *args, **kwargs):

        self.mesta_zanyaty = max(0, self.mesta_zanyaty)
        if self.mesta_zanyaty > self.vmestimost:
            self.mesta_zanyaty = self.vmestimost
        

        self.mesta_svobodnye = max(0, self.vmestimost - self.mesta_zanyaty)
        super().save(*args, **kwargs)
    
    @property
    def procent_zanyatosti(self):
        """Процент заполненности"""
        if self.vmestimost == 0:
            return 0
        return round((self.mesta_zanyaty / self.vmestimost) * 100, 1)



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

    # === Логистика проживания ===
    nuzhen_prozhivanie = models.BooleanField(
        default=False, 
        verbose_name="Нужно проживание"
    )
    tip_prozhivaniya = models.CharField(
        max_length=50,
        choices=[
            ('nomer', 'Номер в гостинице'),
            ('domik', 'Домик на турбазе'),
            ('palatka', 'Палатка'),
            ('ne_nuzhno', 'Не нужно'),
        ],
        default='nomer',
        verbose_name="Тип размещения"
    )
    preferencii = models.TextField(
        blank=True, 
        verbose_name="Предпочтения",
        help_text="Например: не курящие, тихое место, рядом с другом"
    )
    data_zaseleniya = models.DateField(null=True, blank=True, verbose_name="Дата заезда")
    data_vyseleniya = models.DateField(null=True, blank=True, verbose_name="Дата выезда")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'uchastnik'

    def __str__(self):
        return f"{self.familiya} {self.name}"
    
    def doklady_count(self):
        return self.doklad_set.count()
    
    @property
    def has_prozhivanie(self):
        """Проверяет, заселен ли участник"""
        return self.uchastnikprozhivanie_set.exists()


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

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        old_prozhivanie = None
        

        if not is_new:
            old_instance = UchastnikProzhivanie.objects.get(pk=self.pk)
            old_prozhivanie = old_instance.prozhivanie

        if is_new:
            if self.prozhivanie.mesta_zanyaty >= self.prozhivanie.vmestimost:
                raise ValidationError(
                    f"Нет свободных мест в {self.prozhivanie.nazvanie}. "
                    f"Занято: {self.prozhivanie.mesta_zanyaty}, "
                    f"Вместимость: {self.prozhivanie.vmestimost}"
                )
        elif old_prozhivanie and old_prozhivanie.id != self.prozhivanie.id:
            # Переселение: проверяем новое место
            if self.prozhivanie.mesta_zanyaty >= self.prozhivanie.vmestimost:
                raise ValidationError(
                    f"Невозможно переселить: в {self.prozhivanie.nazvanie} нет мест."
                )

        super().save(*args, **kwargs)
        

        with transaction.atomic():
            if is_new:
                # Новое заселение
                self.prozhivanie.mesta_zanyaty += 1
                self.prozhivanie.save()
            elif old_prozhivanie and old_prozhivanie.id != self.prozhivanie.id:
                # Переселение
                old_prozhivanie.mesta_zanyaty = max(0, old_prozhivanie.mesta_zanyaty - 1)
                old_prozhivanie.save()
                
                self.prozhivanie.mesta_zanyaty += 1
                self.prozhivanie.save()

    def delete(self, *args, **kwargs):

        prozhivanie = self.prozhivanie
        
        with transaction.atomic():
            super().delete(*args, **kwargs)
            # Освобождение места
            prozhivanie.mesta_zanyaty = max(0, prozhivanie.mesta_zanyaty - 1)
            prozhivanie.save()


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
    sektsiya = models.ForeignKey(
        'Sekciya', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Секция'
    )

    file = models.FileField(
        upload_to='doklads/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='Файл доклада',
        help_text='PDF, DOC, DOCX, PPT, PPTX (макс. 10MB)'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'doklad'
        ordering = ['nazvanie']

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

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            self.transfer.mesta_zanyaty += 1
            self.transfer.save()
    
    def delete(self, *args, **kwargs):
        transfer = self.transfer
        super().delete(*args, **kwargs)
        transfer.mesta_zanyaty = max(0, transfer.mesta_zanyaty - 1)
        transfer.save()


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
    pomeshchenie = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'programma'
        ordering = ['vremya_nachala']

    def __str__(self):
        title = self.doklad.nazvanie if self.doklad else (str(self.uchastnik) if self.uchastnik else 'Пусто')
        return f"{title} - {self.vremya_nachala.strftime('%d.%m %H:%M')}"


# ========== ФИНАНСОВЫЙ МОДУЛЬ ==========
class Tarif(models.Model):
    """Тарифы для конференции"""
    konferentsiya = models.ForeignKey(Konferentsiya, on_delete=models.CASCADE)
    nazvanie = models.CharField(max_length=100)
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


# ========== МОДУЛЬ УВЕДОМЛЕНИЙ ==========
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


# ========== РОЛИ ПОЛЬЗОВАТЕЛЕЙ ==========
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