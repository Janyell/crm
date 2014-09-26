# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_api', '0002_auto_20140926_1616'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clients',
            old_name='creation_data',
            new_name='creation_date',
        ),
        migrations.RenameField(
            model_name='order_product',
            old_name='order_data',
            new_name='order_date',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='order_data',
            new_name='order_date',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='payment_data',
            new_name='payment_date',
        ),
        migrations.RenameField(
            model_name='orders',
            old_name='ready_data',
            new_name='ready_date',
        ),
        migrations.AlterField(
            model_name='clients',
            name='account_number',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(max_length=75, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='name',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='organization',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='organization_phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='patronymic',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='person_phone',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='companies',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='companies',
            name='name',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='companies',
            name='patronymic',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='bill',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='bill_status',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='city',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='company',
            field=models.ForeignKey(to='base_api.Companies', null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_status',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='roles',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='roles',
            name='name',
            field=models.CharField(max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='roles',
            name='patronymic',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
