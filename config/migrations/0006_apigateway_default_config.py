# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0005_apigatewayconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='apigateway',
            name='default_config',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.ApiGatewayConfig', null=True, verbose_name=b'Default Config'),
        ),
    ]
