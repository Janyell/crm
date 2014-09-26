# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_api', '0003_auto_20140926_1740'),
    ]

    operations = [
        migrations.RenameField(
            model_name='orders',
            old_name='sourse',
            new_name='source',
        ),
        migrations.AddField(
            model_name='order_product',
            name='count_of_products',
            field=models.IntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clients',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='clients',
            name='email',
            field=models.EmailField(max_length=75, unique=True, null=True),
        ),
        migrations.AlterField(
            model_name='companies',
            name='title',
            field=models.CharField(unique=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='order_product',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='city',
            field=models.CharField(max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='comment',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ready_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='unique_number',
            field=models.CharField(unique=True, max_length=50),
        ),
        migrations.AlterField(
            model_name='roles',
            name='login',
            field=models.CharField(unique=True, max_length=15),
        ),
        migrations.AlterField(
            model_name='roles',
            name='password',
            field=models.CharField(max_length=50),
        ),
    ]
