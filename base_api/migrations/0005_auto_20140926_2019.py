# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import base_api.models


class Migration(migrations.Migration):

    dependencies = [
        ('base_api', '0004_auto_20140926_2000'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=base_api.models.UnixTimestampField(null=True, auto_created=True),
        ),
    ]
