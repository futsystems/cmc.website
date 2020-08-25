# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0030_auto_20200821_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='api_port',
            field=models.IntegerField(default=91, verbose_name=b'Http Port'),
        ),
        migrations.AddField(
            model_name='service',
            name='rpc_port',
            field=models.IntegerField(default=91, verbose_name=b'RPC Port'),
        ),
    ]
