#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.db import models
from datetime import datetime
from time import strftime


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
        # See above!
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


class Roles(models.Model):
    login = models.CharField(max_length=15, unique=True)
    password = models.CharField(max_length=50)
    LEADERSHIP = 0
    MANAGER = 1
    PRODUCTION = 2
    ROLES_CHOICES = (
        (MANAGER, 'Менеджер'),
        (PRODUCTION, 'Производство'),
    )
    role = models.IntegerField(choices=ROLES_CHOICES, default=MANAGER)
    name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=50, null=True)
    patronymic = models.CharField(max_length=50, null=True)
    is_deleted = models.BooleanField(default=0)


class Clients(models.Model):
    name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=50, null=True)
    patronymic = models.CharField(max_length=50, null=True)
    organization = models.CharField(max_length=250, null=True)
    organization_phone = models.CharField(max_length=15, null=True)
    person_phone = models.CharField(max_length=15, null=True)
    email = models.EmailField(null=True, unique=True)
    is_deleted = models.BooleanField(default=0)
    creation_date = UnixTimestampField(auto_created=True)
    account_number = models.CharField(max_length=50, null=True)
    is_interested = models.BooleanField(default=0)


class Companies(models.Model):
    title = models.CharField(max_length=250, unique=True)
    name = models.CharField(max_length=25, null=True)
    last_name = models.CharField(max_length=50, null=True)
    patronymic = models.CharField(max_length=50, null=True)
    is_deleted = models.BooleanField(default=0)


class Orders(models.Model):
    role = models.ForeignKey(Roles)
    source = models.IntegerField()
    client = models.ForeignKey(Clients)
    unique_number = models.CharField(max_length=50, unique=True)
    company = models.ForeignKey(Companies, null=True)
    bill = models.FloatField(null=True)
    payment_date = UnixTimestampField(auto_created=True)
    IN_PRODUCTION = 0
    NEED_SURCHARGE = 1
    SHIPPED = 2
    READY = 3
    ORDER_STATUS_CHOICES = (
        (IN_PRODUCTION, 'В производстве'),
        (NEED_SURCHARGE, 'Нужна доплата'),
        (SHIPPED, 'Отгружен'),
        (READY, 'Готов'),
    )
    order_status = models.IntegerField(null=True, choices=ORDER_STATUS_CHOICES)
    bill_status = models.IntegerField(null=True)
    ready_date = UnixTimestampField(auto_created=True)
    comment = models.TextField(null=True)
    is_deleted = models.BooleanField(default=0)
    order_date = UnixTimestampField(auto_created=True)
    city = models.CharField(max_length=256, null=True)
    in_archive = models.BooleanField(default=0)


class Products(models.Model):
    title = models.CharField(max_length=500)


class Order_Product(models.Model):
    order = models.ForeignKey(Orders)
    product = models.ForeignKey(Products)
    is_deleted = models.BooleanField(default=0)
    order_date = UnixTimestampField(auto_created=True)
    count_of_products = models.IntegerField(default=0)


# Create your models here.
