# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0004_apigateway_date_created'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApiGatewayConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.CharField(default=b'1.0', max_length=20, verbose_name=b'Version')),
                ('config', models.TextField(verbose_name=b'config')),
                ('is_default', models.BooleanField(default=False, verbose_name=b'Is Default')),
                ('description', models.TextField(default=b'', verbose_name=b'Description', blank=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name=b'created time')),
                ('gateway', models.ForeignKey(related_name='configs', verbose_name=b'ApiGateway', to='config.ApiGateway')),
            ],
        ),
    ]
