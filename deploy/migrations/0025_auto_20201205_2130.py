# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-05 13:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0024_auto_20201205_1730'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='install_apm',
            field=models.BooleanField(default=True, verbose_name=b'Instal APM'),
        ),
        migrations.AddField(
            model_name='server',
            name='install_consul',
            field=models.BooleanField(default=True, verbose_name=b'Install Consul'),
        ),
        migrations.AddField(
            model_name='server',
            name='install_mq',
            field=models.BooleanField(default=True, verbose_name=b'Install RabbitMQ'),
        ),
        migrations.AddField(
            model_name='server',
            name='install_mysql',
            field=models.BooleanField(default=True, verbose_name=b'Install MySQL'),
        ),
    ]
