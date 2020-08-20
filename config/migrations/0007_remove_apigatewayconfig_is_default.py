# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0006_apigateway_default_config'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apigatewayconfig',
            name='is_default',
        ),
    ]
