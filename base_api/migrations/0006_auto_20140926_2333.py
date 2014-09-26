# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('base_api', '0005_auto_20140926_2019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='creation_date',
            field=base_api.models.UnixTimestampField(null=True, auto_created=True),
        ),
        migrations.AlterField(
            model_name='order_product',
            name='order_date',
            field=base_api.models.UnixTimestampField(null=True, auto_created=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='payment_date',
            field=base_api.models.UnixTimestampField(null=True, auto_created=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='ready_date',
            field=base_api.models.UnixTimestampField(null=True, auto_created=True),
        ),
    ]
