# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(max_length=50)),
                ('organization', models.CharField(max_length=250)),
                ('organization_phone', models.CharField(max_length=15)),
                ('person_phone', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=75)),
                ('is_deleted', models.BooleanField(default=0)),
                ('creation_data', models.DateField()),
                ('account_number', models.CharField(max_length=50)),
                ('is_interested', models.BooleanField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Companies',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=250)),
                ('name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Order_Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_deleted', models.BooleanField(default=0)),
                ('order_data', models.DateField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sourse', models.IntegerField()),
                ('unique_number', models.CharField(max_length=50)),
                ('bill', models.FloatField()),
                ('payment_data', models.DateField()),
                ('order_status', models.IntegerField()),
                ('bill_status', models.IntegerField()),
                ('ready_data', models.IntegerField()),
                ('comment', models.CharField(max_length=700)),
                ('is_deleted', models.BooleanField(default=0)),
                ('order_data', models.DateField()),
                ('city', models.CharField(max_length=50)),
                ('in_archive', models.BooleanField(default=0)),
                ('client', models.ForeignKey(to='base_api.Clients')),
                ('company', models.ForeignKey(to='base_api.Companies')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=500)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Roles',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login', models.CharField(max_length=15)),
                ('password', models.CharField(max_length=25)),
                ('role', models.IntegerField()),
                ('name', models.CharField(max_length=25)),
                ('last_name', models.CharField(max_length=50)),
                ('patronymic', models.CharField(max_length=50)),
                ('is_deleted', models.BooleanField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='orders',
            name='role',
            field=models.ForeignKey(to='base_api.Roles'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order_product',
            name='order',
            field=models.ForeignKey(to='base_api.Orders'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='order_product',
            name='product',
            field=models.ForeignKey(to='base_api.Products'),
            preserve_default=True,
        ),
    ]
