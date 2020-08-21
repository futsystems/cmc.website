# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0009_apigatewayconfig_version_int'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apigatewayconfig',
            name='version_int',
            field=models.IntegerField(default=10, verbose_name=b'Version Int', auto_created=True),
        ),
    ]
