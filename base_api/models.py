#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from time import strftime
from django.contrib.auth.models import User, UserManager
from djangosphinx.models import SphinxSearch
from media_tree.models import FileNode


class UnixTimestampField(models.DateTimeField):
    """UnixTimestampField: creates a DateTimeField that is represented on the
    database as a TIMESTAMP field rather than the usual DATETIME field.
    """
    def __init__(self, null=False, blank=False, **kwargs):
        super(UnixTimestampField, self).__init__(**kwargs)
        # default for TIMESTAMP is NOT NULL unlike most fields, so we have to
        # cheat a little:
        self.blank, self.isnull = blank, null
        self.null = True  # To prevent the framework from shoving in "not null".

    def db_type(self, connection):
        typ = ['TIMESTAMP']
        # See above!-
        if self.isnull:
            typ += ['NULL']
        if self.auto_created:
            typ += ['default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP']
        return ' '.join(typ)

    def to_python(self, value):
        if isinstance(value, int):
            return datetime.fromtimestamp(value)
        else:
            return models.DateTimeField.to_python(self, value)

    def get_db_prep_value(self, value, connection, prepared=False):
        if value is None:
            return None
        # Use '%Y%m%d%H%M%S' for MySQL < 4.1
        return strftime('%Y-%m-%d %H:%M:%S', value.timetuple())


class Roles(User):
    """User with app settings."""
    # Use UserManager to get the create_user method, etc.
    # login = models.CharField(max_length=15, unique=True)
    # password = models.CharField(max_length=50)
    LEADERSHIP = 0
    MANAGER = 1
    PRODUCTION = 2
    ROLES_CHOICES = (
        (MANAGER, 'Менеджер'),
        (PRODUCTION, 'Производство'),
        (LEADERSHIP, 'Руководство'),
    )
    role = models.IntegerField(choices=ROLES_CHOICES, default=MANAGER)
    name = models.CharField(max_length=25, null=True, blank=True)
    surname = models.CharField(max_length=50, null=True, blank=True)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    is_deleted = models.BooleanField(default=0)

    phone = models.CharField(max_length=50, null=True, blank=True, default='')

    objects = UserManager()

    search = SphinxSearch()


class Clients(models.Model):
    name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    organization = models.CharField(max_length=250, null=True, blank=True)
    organization_phone = models.CharField(max_length=15, null=True, blank=True)
    person_phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_deleted = models.BooleanField(default=0)
    creation_date = UnixTimestampField(auto_created=True)
    is_interested = models.BooleanField(default=0)
    role = models.ForeignKey(Roles, null=True, blank=True)
    organization_type = models.CharField(max_length=255, blank=True, default='')

    search = SphinxSearch()


class Companies(models.Model):
    title = models.CharField(max_length=250)
    name = models.CharField(max_length=25, null=True, blank=True)
    last_name = models.CharField(max_length=50, null=True, blank=True)
    patronymic = models.CharField(max_length=50, null=True, blank=True)
    is_deleted = models.BooleanField(default=0)

    search = SphinxSearch()


# ALL = -1
# EMAIL = 0  # поменять на 8? на 10? 0 ведь нельзя записать в таблицу
# CALL = 1
# SITE = 2
# ZT = 3
# AQB = 4
# HAH = 5
# LAND = 6
# TEND = 7
# ORDER_SOURCE_LIST = [
#     # {'name': 'Все',
#     #  'code': ALL},
#     {'name': 'ЗТ',
#      'code': ZT},
#     {'name': 'AQB',
#      'code': AQB},
#     {'name': 'H-A-H',
#      'code': HAH},
#     {'name': 'Landing',
#      'code': LAND},
#     {'name': 'Тендер',
#      'code': TEND},
#     {'name': 'Электронная почта',
#      'code': EMAIL},
#     {'name': 'Звонок',
#      'code': CALL},
#     {'name': 'Заявка с сайта',
#      'code': SITE}
# ]


class TransportCampaigns(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)


class Sources(models.Model):
    title = models.CharField(max_length=255)
    is_active = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)


class Cities(models.Model):
    name = models.CharField(max_length=255)


class Orders(models.Model):
    role = models.ForeignKey(Roles)
    # EMAIL = 0
    # CALL = 1
    # SITE = 2
    # ZT = 3
    # AQB = 4
    # HAH = 5
    # LAND = 6
    # TEND = 7
    # ORDER_SOURCE_CHOICES = (
    #     (ZT, 'ЗТ'),
    #     (AQB, 'AQB'),
    #     (HAH, 'H-A-H'),
    #     (LAND, 'Landing'),
    #     (TEND, 'Тендер'),
    #     (EMAIL, 'Электронная почта'),
    #     (CALL, 'Звонок'),
    #     (SITE, 'Заявка с сайта'),
    # )
    # source = models.IntegerField(choices=ORDER_SOURCE_CHOICES, default=ZT)
    source = models.ForeignKey(Sources)
    transport_campaign = models.ForeignKey(TransportCampaigns, null=True)
    client = models.ForeignKey(Clients)
    unique_number = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Companies, null=True, blank=True)
    bill = models.IntegerField(null=True, blank=True)
    payment_date = UnixTimestampField(blank=True, null=True)
    IN_PRODUCTION = 0
    SHIPPED = -1
    READY = 2
    ORDER_STATUS_CHOICES = (
        (IN_PRODUCTION, 'В производстве'),
        (SHIPPED, 'Отгружен'),
        (READY, 'Готов'),
    )
    order_status = models.IntegerField(null=True, choices=ORDER_STATUS_CHOICES, blank=True)
    SET = 0
    PAID = 2
    NEED_SURCHARGE = 1
    DELAY = 3
    VERBAL = 4
    SELECTION = 5
    BILL_STATUS_CHOICES = (
        (SET, 'Выставлен'),
        (NEED_SURCHARGE, 'Нужна доплата'),
        (PAID, 'Оплачен'),
        (DELAY, 'Отсрочка платежа'),
        (VERBAL, 'Устно'),
        (SELECTION, 'Подбор'),
    )
    bill_status = models.IntegerField(null=True, blank=True)
    ready_date = UnixTimestampField(blank=True, null=True)
    comment = models.TextField(null=True, blank=True)
    is_deleted = models.BooleanField(default=0)
    order_date = UnixTimestampField(default=datetime.now())
    # order_date = UnixTimestampField(auto_created=True)
    city_old = models.CharField(max_length=256, null=True, blank=True)
    city = models.ForeignKey(Cities, null=True, blank=True)
    in_archive = models.BooleanField(default=0)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    is_claim = models.BooleanField(default=0)
    is_comment_my = models.BooleanField(default=1)
    shipped_date = models.DateField(blank=True, null=True)
    brought_sum = models.IntegerField(null=True, blank=True)

    related_orders = models.ManyToManyField("self", null=True, blank=True)
    related_color = models.IntegerField(null=True, blank=True)

    factory_comment = models.TextField(null=True, blank=True)

    search = SphinxSearch()


class ProductGroups(models.Model):
    title = models.CharField(max_length=255)
    is_deleted = models.BooleanField(default=0)


class Products(models.Model):
    title = models.CharField(max_length=255)
    price = models.IntegerField(default=0, blank=True)
    is_active = models.BooleanField(default=1)
    is_deleted = models.BooleanField(default=0)
    group = models.ForeignKey(ProductGroups, null=True)


class Order_Product(models.Model):
    order = models.ForeignKey(Orders)
    product = models.ForeignKey(Products)
    is_deleted = models.BooleanField(default=0)
    order_date = UnixTimestampField(auto_created=True)
    count_of_products = models.IntegerField(default=0)
    price = models.IntegerField(default=0, blank=True)


class Order_Files(models.Model):
    order = models.ForeignKey(Orders, null=True, blank=True)
    title = models.CharField(max_length=50, null=False, blank=True)
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    file_node = models.ForeignKey(FileNode, null=True, blank=True)


class Client_Files(models.Model):
    client = models.ForeignKey(Clients, null=True, blank=True)
    title = models.CharField(max_length=50, null=False, blank=True)
    file = models.FileField(upload_to="uploads/", null=True, blank=True)
    file_node = models.ForeignKey(FileNode, null=True, blank=True)


class KPTemplates(models.Model):
    html_text = models.TextField()
    html_text_for_kp = models.TextField(default='')
    company = models.ForeignKey(Companies, null=True, blank=True)
    number = models.IntegerField(null=True, blank=True)