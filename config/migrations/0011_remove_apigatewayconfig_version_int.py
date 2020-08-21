# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0010_auto_20200821_0939'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apigatewayconfig',
            name='version_int',
        ),
    ]
