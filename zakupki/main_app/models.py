from django.db import models
from .tasks import *

# Нормативно-справочная информация
class nsiOkei(models.Model):
    """ ОК единиц измерения """

    class Meta:
        verbose_name = "ОКЕИ"
        verbose_name_plural = "ОКЕИ"

    code = models.CharField(
        verbose_name='Код ОКЕИ',
        max_length=5,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКЕИ',
        max_length=250,
    )
    symbol = models.CharField(
        max_length=30,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkpd2(models.Model):
    """ ОК видов экономической деятельности, продукции и услуг """

    class Meta:
        verbose_name = "ОКПД2"
        verbose_name_plural = "ОКПД2"

    code = models.CharField(
        verbose_name='Код ОКПД2',
        max_length=20,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКПД2',
        max_length=500,
    )
    parent = models.CharField(
        max_length=8,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkved2(models.Model):
    """ ОК видов экономической деятельности """

    class Meta:
        verbose_name = "ОКВЭД2"
        verbose_name_plural = "ОКВЭД2"

    code = models.CharField(
        verbose_name='Код ОКВЕД2',
        max_length=15,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКВЕД2',
        max_length=500,
    )
    parent = models.CharField(
        max_length=15,
        null=True,
    )
    section = models.CharField(
        verbose_name='Раздел',
        max_length=1,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiTimeZone(models.Model):
    """ Временная зона """

    class Meta:
        verbose_name = "Временная зона"
        verbose_name_plural = "Временные зоны"

    offset = models.IntegerField(
        default=0,
        verbose_name='Смещение отностельно MSK'
    )

    name = models.CharField(
        verbose_name='Название временной зоны',
        max_length=100,
    )

    def __str__(self):
        return "{} (MCK{}{})".format(self.name, "+" if self.offset >= 0 else "", self.offset)

    def get_id(self):
        return self.id


class nsiTypeContact(models.Model):
    class Meta:
        verbose_name = "Тип контакта"
        verbose_name_plural = "Типы контактов"

    name = models.CharField(
        verbose_name='Тип контакта',
        max_length=30,
    )

    def __str__(self):
        return self.name

    def get_id(self):
        return self.id


# Юридические и физические лица
class Organization(models.Model):
    class Meta:
        verbose_name = "Организация"
        verbose_name_plural = "Организации"

    types_org = [
        ('L', 'Юридическое лицо'),
        ('P', 'Физическое лицо'),
    ]

    type_org = models.CharField(
        verbose_name='Тип органзиации',
        choices=types_org,
        max_length=1,
        default='L',
    )
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=300,
    )
    short_name = models.CharField(
        verbose_name='Сокращенное наименвоание',
        max_length=100,
    )
    registration_date = models.DateTimeField(
        verbose_name='Дата постановки на учет',
        null=True,
        blank=True,
    )
    ogrn = models.CharField(
        verbose_name='ОГРН',
        max_length=13,
        null=True,
        blank=True,
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=20,
    )
    kpp = models.CharField(
        verbose_name='КПП',
        max_length=20,
        null=True,
        blank=True,
    )
    legalAddress = models.TextField(
        verbose_name='Юридический адрес',
        max_length=2000,
        null=True,
        blank=True,
    )
    postalAddress = models.TextField(
        verbose_name='Почтовый адрес',
        max_length=2000,
        null=True,
        blank=True,
    )

    timeZone = models.ForeignKey(
        nsiTimeZone,
        verbose_name='Временная зона',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="org_timeZone"
    )

    def __str__(self):
        return self.short_name

    def get_id(self):
        return self.id


class OrganizationOkved2(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
    )
    okved2 = models.ForeignKey(
        nsiOkved2,
        verbose_name='ОКВЭД2',
        on_delete=models.CASCADE,
    )
    isMain = models.BooleanField(
        verbose_name='Основной',
        default=False,
    )

    def __str__(self):
        return "{} {}".format(self.organization, self.okved2)

    def get_id(self):
        return self.id


class OrganizationContacts(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        nsiTypeContact,
        verbose_name='Тип контакта',
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=300,
    )
    person = models.ForeignKey(
        "Person",
        verbose_name='Физическое лицо',
        on_delete=models.CASCADE,
        related_name="organization_contact"
    )

    def __str__(self):
        return "{} {} {}".format(self.organization, self.type, self.value)

    def get_id(self):
        return self.id


class Person(models.Model):
    class Meta:
        verbose_name = "Физическое лицо"
        verbose_name_plural = "Физические лица"

    firstName = models.CharField(
        verbose_name='Имя',
        max_length=300,
        null=True,
    )
    middleName = models.CharField(
        verbose_name='Отчество',
        max_length=300,
        null=True,
    )
    lastName = models.CharField(
        verbose_name='Фамилия',
        max_length=300,
        null=True,
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        null=True,
    )

    def __str__(self):
        return "{} {}. {}.".format(self.lastName, self.firstName[0], self.middleName[0])

    def get_id(self):
        return self.id


class PersonContacts(models.Model):
    person = models.ForeignKey(
        Person,
        verbose_name='Физическое лицо',
        on_delete=models.CASCADE,
    )
    type = models.ForeignKey(
        nsiTypeContact,
        verbose_name='Тип контакта',
        on_delete=models.CASCADE,
    )
    value = models.CharField(
        verbose_name='Значение',
        max_length=300,
    )

    def __str__(self):
        return "{} {} {}".format(self.person, self.type, self.value)

    def get_id(self):
        return self.id


class QueryManager(models.Manager):
    def get_from_rts(self):
        get_query_from_rts.apply_async()

# Основные сущности
class Query(models.Model):
    """ Запросы на цену """
    num = models.CharField(
        verbose_name='Номер запроса',
        max_length=200,
        null=True,
        blank=True,
    )
    description = models.CharField(
        verbose_name='Описание',
        max_length=2000,
        null=True,
        blank=True,
    )
    okpd2 = models.ForeignKey(
        nsiOkpd2,
        verbose_name='ОКПД2',
        on_delete=models.CASCADE,
        related_name='query',
    )
    organizer = models.ForeignKey(
        Organization,
        verbose_name='Организатор',
        on_delete=models.CASCADE,
        related_name='query',
    )
    date_begin = models.DateField(
        verbose_name='Дата публикации',
        null=True,
        blank=True,
    )
    date_end = models.DateField(
        verbose_name='Дата окончания',
        null=True,
        blank=True,
    )
    link_to_doc = models.URLField(
        verbose_name='Ссылка на документацию',
    )
    objects = QueryManager()

    def __str__(self):
        return f"{self.organizer} {self.okpd2}"


class QueryNomenclature(models.Model):
    """ Строка номеклатуры """
    nomenclature = models.ForeignKey(
        "Nomenclature",
        on_delete=models.CASCADE,
        verbose_name='Номенклатура',
        related_name='query_nomenclature',
    )
    count = models.CharField(
        verbose_name='Количество',
        max_length=50,
    )
    ei = models.ForeignKey(
        "nsiOkei",
        on_delete=models.CASCADE,
        verbose_name='Единица измерения',
        related_name='query_nomenclature',
    )
    query = models.ForeignKey(
        Query,
        verbose_name='Запрос',
        on_delete=models.CASCADE,
        related_name='query_nomenclature',
    )

    def __str__(self):
        return f"{self.nomenclature} {self.count}"


class Nomenclature(models.Model):
    """ Номенклатура для закупки """
    TYPES = (
        (0, 'Товар'),
        (1, 'Услуга')
    )
    name = models.CharField(
        verbose_name='Номеклатура',
        max_length=1000,
    )
    type = models.IntegerField(
        verbose_name='Тип',
        default=0,
        choices=TYPES,
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )

    def __str__(self):
        return self.name
