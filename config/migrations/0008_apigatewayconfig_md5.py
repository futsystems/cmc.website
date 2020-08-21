# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0007_remove_apigatewayconfig_is_default'),
    ]

    operations = [
        migrations.AddField(
            model_name='apigatewayconfig',
            name='md5',
            field=models.CharField(default=b'NotSet', max_length=50, verbose_name=b'Md5'),
        ),
    ]
