from django.db import models


# Нормативно-справочная информация
class nsiOkfs(models.Model):
    """ ОК форм собственности """

    class Meta:
        verbose_name = "ОКФС"
        verbose_name_plural = "ОКФС"

    code = models.CharField(
        verbose_name='Код ОКФС',
        max_length=2,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКФС',
        max_length=250,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOktmo(models.Model):
    """ ОК территорий муниципальных образований """

    class Meta:
        verbose_name = "ОКТМО"
        verbose_name_plural = "ОКТМО"

    code = models.CharField(
        verbose_name='Код ОКФС',
        max_length=11,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКФС',
        max_length=250,
    )
    parent = models.CharField(
        max_length=11,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkogu(models.Model):
    """ ОК органов государственной власти и управления """

    class Meta:
        verbose_name = "ОКОГУ"
        verbose_name_plural = "ОКОГУ"

    code = models.CharField(
        verbose_name='Код ОКОГУ',
        max_length=7,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКОГУ',
        max_length=250,
    )
    parent = models.CharField(
        max_length=7,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkopf(models.Model):
    """ ОК организационно-правовых форм """

    class Meta:
        verbose_name = "ОКОПФ"
        verbose_name_plural = "ОКОПФ"

    code = models.CharField(
        verbose_name='Код ОКОПФ',
        max_length=5,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКОГУ',
        max_length=250,
    )
    parent = models.CharField(
        max_length=5,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkato(models.Model):
    """ ОК объектов административно-территориального деления """

    class Meta:
        verbose_name = "ОКАТО"
        verbose_name_plural = "ОКАТО"

    code = models.CharField(
        verbose_name='Код ОКАТО',
        max_length=11,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКАТО',
        max_length=250,
    )
    parent = models.CharField(
        max_length=11,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkeiSection(models.Model):
    code = models.CharField(
        verbose_name='Код раздела',
        max_length=5,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование раздела',
        max_length=1000,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkeiGroup(models.Model):
    code = models.IntegerField(
        verbose_name='Код группы',
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование группы',
        max_length=1000,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkei(models.Model):
    """ ОК единиц измерения """

    class Meta:
        verbose_name = "ОКЕИ"
        verbose_name_plural = "ОКЕИ"

    code = models.CharField(
        verbose_name='Код ОКЕИ',
        max_length=5,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКЕИ',
        max_length=250,
    )
    symbol = models.CharField(
        max_length=30,
        null=True,
    )
    section = models.ForeignKey(
        nsiOkeiSection,
        verbose_name='Раздел',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        nsiOkeiGroup,
        verbose_name='Группа',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkpd(models.Model):
    """ ОК видов экономической деятельности, продукции и услуг """

    class Meta:
        verbose_name = "ОКПД"
        verbose_name_plural = "ОКПД"

    code = models.CharField(
        verbose_name='Код ОКПД',
        max_length=8,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКПД',
        max_length=500,
    )
    parent = models.CharField(
        max_length=8,
        null=True,
    )
    section = models.CharField(
        max_length=1,
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
        max_length=8,
        unique=True,
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


class nsiOkved(models.Model):
    """ ОК видов экономической деятельности """

    class Meta:
        verbose_name = "ОКВЭД"
        verbose_name_plural = "ОКВЭД"

    code = models.CharField(
        verbose_name='Код ОКВЕД',
        max_length=15,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование по ОКВЕД',
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
    subsection = models.CharField(
        verbose_name='Подраздел',
        max_length=2,
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


class nsiOkpo(models.Model):
    """ ОК предприятий и организаций """

    class Meta:
        verbose_name = "ОКПО"
        verbose_name_plural = "ОКПО"

    code = models.CharField(
        verbose_name='Код ОКПО',
        max_length=10,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование ОКПО',
        max_length=500,
        null=True,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

    def get_id(self):
        return self.id


class nsiOkv(models.Model):
    """ ОК валют """

    class Meta:
        verbose_name = "ОК валют"
        verbose_name_plural = "ОК валют"

    code = models.CharField(
        verbose_name='Код валюты',
        max_length=3,
        unique=True,
    )
    digitalCode = models.CharField(
        verbose_name='Цифровой код валюты',
        max_length=100,
    )
    name = models.CharField(
        verbose_name='Наименование валюты',
        max_length=500,
    )
    shortName = models.CharField(
        verbose_name='Наименование валюты',
        max_length=500,
        null=True,
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


class nsiIkul(models.Model):
    """ Идентификационные коды юридического лица """

    class Meta:
        verbose_name = "ИКЮЛ"
        verbose_name_plural = "ИКЮЛ"

    code = models.CharField(
        verbose_name='Код ИКЮЛ',
        max_length=100,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименвоание вида юридического лица',
        max_length=255,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

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


class nsiPPO(models.Model):
    class Meta:
        verbose_name = "ППО"
        verbose_name_plural = "ППО"

    code = models.CharField(
        verbose_name='Код ППО',
        max_length=11,
        unique=True,
    )
    name = models.CharField(
        verbose_name='Наименование ППО',
        max_length=2000,
    )

    def __str__(self):
        return "{} {}".format(self.code, self.name)

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
    )
    ogrn = models.CharField(
        verbose_name='ОГРН',
        max_length=13,
    )
    inn = models.CharField(
        verbose_name='ИНН',
        max_length=12,
        unique=True,
    )
    kpp = models.CharField(
        verbose_name='КПП',
        max_length=9
    )
    legalAddress = models.TextField(
        verbose_name='Юридический адрес',
        max_length=2000,
        null=True,
    )
    postalAddress = models.TextField(
        verbose_name='Почтовый адрес',
        max_length=2000,
        null=True,
    )

    timeZone = models.ForeignKey(
        nsiTimeZone,
        verbose_name='Временная зона',
        on_delete=models.CASCADE,
        null=True,
        related_name="org_timeZone"
    )
    okpo = models.ForeignKey(
        nsiOkpo,
        verbose_name='ОКПО',
        on_delete=models.CASCADE,
        null=True,
        related_name="org_okpo"
    )
    okato = models.ForeignKey(
        nsiOkato,
        verbose_name='ОКАТО',
        on_delete=models.CASCADE,
        null=True,
        related_name="org_nsiOkato",
    )
    oktmo = models.ForeignKey(
        nsiOktmo,
        verbose_name='ОКТМО',
        on_delete=models.CASCADE,
        null=True,
        related_name="org_oktmo",
    )
    okfs = models.ForeignKey(
        nsiOkfs,
        verbose_name='ОКФС',
        on_delete=models.CASCADE,
        null=True,
        related_name="org_okfs",
    )
    okopf = models.ForeignKey(
        nsiOkopf,
        verbose_name='ОКОПФ',
        on_delete=models.CASCADE,
        null=True,
        related_name="org_okopf",
    )

    def __str__(self):
        return self.short_name

    def get_id(self):
        return self.id


class OrganizationOkved(models.Model):
    organization = models.ForeignKey(
        Organization,
        verbose_name='Организация',
        on_delete=models.CASCADE,
    )
    okved = models.ForeignKey(
        nsiOkved,
        verbose_name='ОКВЭД',
        on_delete=models.CASCADE,
    )
    isMain = models.BooleanField(
        verbose_name='Основной',
        default=False,
    )

    def __str__(self):
        return "{} {}".format(self.organization, self.okved)

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


# Основные сущности
class Query(models.Model):
    """ Запросы на цену """
    okpd2 = models.ForeignKey(
        nsiOkpd2,
        verbose_name='ОКПД2',
        on_delete=models.CASCADE,
        related_name='query',
    )
    organizer = models.ForeignKey(
        Organization,
        verbose_name='ОКПД2',
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


class QueryNomenclature(models.Model):
    """ Строка номеклатуры """
    nomenclature = models.ForeignKey(
        "Nomenclature",
        on_delete=models.CASCADE,
        verbose_name='Номенклатура',
        related_name='query_nomenclature',
    )
    count = models.FloatField(
        verbose_name='Количество',
        default=0.0,
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
    )
    description = models.TextField(
        verbose_name='Описание',
        blank=True,
        null=True,
    )
