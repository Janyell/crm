# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='comment',
            field=models.CharField(max_length=700, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_data',
            field=models.DateField(null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ready_data',
            field=models.IntegerField(null=True),
        ),
    ]
