# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-09-01 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0049_auto_20200901_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='discovery_scheme',
            field=models.CharField(choices=[(b'Consul', b'Consul'), (b'EndPoints', b'EndPoints')], default=b'Consul', max_length=20, verbose_name=b'Discovery Scheme'),
        ),
        migrations.AddField(
            model_name='service',
            name='host',
            field=models.CharField(blank=True, default=b'dev-api.marvelsystem.net', max_length=255, null=True, verbose_name=b'Host'),
        ),
        migrations.AddField(
            model_name='service',
            name='port',
            field=models.IntegerField(default=80, verbose_name=b'Port'),
        ),
    ]