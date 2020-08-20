# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0003_auto_20200820_1333'),
    ]

    operations = [
        migrations.AddField(
            model_name='apigateway',
            name='date_created',
            field=models.DateTimeField(auto_now=True, verbose_name=b'created time', null=True),
        ),
    ]
