from django.db import models
from .tasks import *


# Нормативно-справочная информация
class nsiOkeiManager(models.Manager):
    def get_from_gov(self):
        get_from_gov_okei.apply_async()


class nsiOkei(models.Model):
    """ ОК единиц измерения """

    class Meta:
        verbose_name = "ОКЕИ"
        verbose_name_plural = "ОКЕИ"
        ordering = ['code']

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
    objects=nsiOkeiManager()

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkpd2Manager(models.Manager):
    def get_from_gov(self):
        get_from_gov_okpd2.apply_async()


class nsiOkpd2(models.Model):
    """ ОК видов экономической деятельности, продукции и услуг """

    class Meta:
        verbose_name = "ОКПД2"
        verbose_name_plural = "ОКПД2"
        ordering = ['code']

    code = models.CharField(
        verbose_name='Код ОКПД2',
        max_length=20,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКПД2',
        max_length=500,
    )
    objects=nsiOkpd2Manager()

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkved2Manager(models.Manager):
    def get_from_gov(self):
        get_from_gov_okved2.apply_async()


class nsiOkved2(models.Model):
    """ ОК видов экономической деятельности """
    class Meta:
        verbose_name = "ОКВЭД2"
        verbose_name_plural = "ОКВЭД2"
        ordering = ['code']

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
    objects=nsiOkved2Manager()

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


class OrganisationManager(models.Manager):
    def get_from_gov(self):
        get_from_gov_organisation.apply_async()

    def get_from_sbis(self):
        get_org_from_sbis.apply_async()


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
    director = models.CharField(
        verbose_name='Руководитель',
        max_length=300,
        null=True,
        blank=True,
    )
    owner = models.CharField(
        verbose_name='Истец (выиграл/проиграл/прочее)',
        max_length=300,
        null=True,
        blank=True,
    )
    defend = models.CharField(
        verbose_name='Ответчик (выиграл/проиграл/прочее)',
        max_length=300,
        null=True,
        blank=True,
    )
    tender = models.CharField(
        verbose_name='Торги (учавствовал/выиграл/госконтракт)',
        max_length=300,
        null=True,
        blank=True,
    )
    info = models.TextField(
        verbose_name='Краткая информация',
        max_length=3000,
        null=True,
        blank=True,
    )
    email = models.EmailField(
        verbose_name='Электронная почта',
        null=True,
        blank=True,
    )
    objects = OrganisationManager()

    def __str__(self):
        return self.short_name

    def get_id(self):
        return self.id

    def get_main_okved2(self):
        try:
            res = self.org_okved.filter(isMain=True)[0].okved2
        except:
            res = 'Не найден'
        return res


class OrganizationOkved2(models.Model):
    class Meta:
        ordering=['okved2']
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
        related_name='org_okved'
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

    def __str__(self):
        return "{} {} {}".format(self.organization, self.type, self.value)

    def get_id(self):
        return self.id


class QueryManager(models.Manager):
    def get_from_rts(self):
        get_query_from_rts.apply_async()


# Основные сущности
class Query(models.Model):
    """ Запросы на цену """
    class Meta:
        verbose_name='Запрос'
        verbose_name_plural='Запросы'
        ordering=['okpd2']

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
    url = models.URLField(
        verbose_name='Детальная информация',
        null=True,
        blank=True,
    )
    objects = QueryManager()

    def __str__(self):
        return f"{self.organizer} {self.okpd2}"

    def find_suppliers(self):
        """ Ищем совпадения ОКПО и ОКВЭД """
        okpd2_code = self.okpd2.code
        suppliers_okveds2 = OrganizationOkved2.objects.filter(okved2__code__contains=okpd2_code[:8])
        if len(suppliers_okveds2) == 0:
            suppliers_okveds2 = OrganizationOkved2.objects.filter(okved2__code__contains=okpd2_code[:5])
        suppliers_ids = []
        for suppliers_okved2 in suppliers_okveds2:
            suppliers_ids.append(suppliers_okved2.organization.id)
        suppliers = Organization.objects.filter(id__in=suppliers_ids)
        return suppliers

    def count_suppliers(self):
        """ Количество найденных поставщиков """
        return len(self.find_suppliers())


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


class QuerySupplier(models.Model):
    supplier = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='query_supplier',
        verbose_name='Поставщик'
    )

    query = models.ForeignKey(
        Query,
        on_delete=models.CASCADE,
        related_name='query_supplier',
        verbose_name='Запрос'
    )

    status = models.CharField(
        verbose_name='Статус',
        max_length=200,
    )
