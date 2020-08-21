# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0008_apigatewayconfig_md5'),
    ]

    operations = [
        migrations.AddField(
            model_name='apigatewayconfig',
            name='version_int',
            field=models.IntegerField(default=10, verbose_name=b'Version Int'),
        ),
    ]
