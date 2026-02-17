from django.db import models


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
    
    class Meta:
        db_table = 'konferentsiya'
        ordering = ['-data_nachala']
    
    def __str__(self):
        return self.nazvanie


class Sekciya(models.Model):
    nazvanie = models.CharField(max_length=255, unique=True)
    opisanie = models.TextField(blank=True)
    
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
    prozhivanie = models.ForeignKey(Prozhivanie, on_delete=models.SET_NULL, null=True, blank=True)
    nuzhen_transfer = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'uchastnik'
    
    def doklady_count(self):
        return self.doklad_set.count()
    
    def __str__(self):
        return f"{self.familiya} {self.name}"


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
    
    class Meta:
        db_table = 'otkaz'
    
    def __str__(self):
        return f"Отказ: {self.uchastnik}"


class UchastnikTransfer(models.Model):
    uchastnik = models.ForeignKey(Uchastnik, on_delete=models.CASCADE)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    pribitye = models.DateTimeField(blank=True, null=True)
    otpravlenie = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        db_table = 'uchastnik_transfer'
        unique_together = ('uchastnik', 'transfer')
    
    def __str__(self):
        return f"{self.uchastnik} ↔ {self.transfer}"


class ProzhivanieTransfer(models.Model):
    prozhivanie = models.ForeignKey(Prozhivanie, on_delete=models.CASCADE)
    transfer = models.ForeignKey(Transfer, on_delete=models.CASCADE)
    
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
    
    class Meta:
        db_table = 'programma'
        ordering = ['vremya_nachala']
    
    def __str__(self):
        title = self.doklad.nazvanie if self.doklad else (str(self.uchastnik) if self.uchastnik else 'Пусто')
        return f"{title} - {self.vremya_nachala.strftime('%d.%m %H:%M')}"