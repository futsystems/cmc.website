# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0025_auto_20200821_1422'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='support_http',
            field=models.BooleanField(default=True, verbose_name=b'HTTP Support'),
        ),
        migrations.AddField(
            model_name='service',
            name='support_rpc',
            field=models.BooleanField(default=True, verbose_name=b'RPC Support'),
        ),
        migrations.AlterField(
            model_name='service',
            name='name',
            field=models.CharField(default=b'Common', help_text=b'no need RPC API,Common etc.,', max_length=50, verbose_name=b'Service Name'),
        ),
    ]
