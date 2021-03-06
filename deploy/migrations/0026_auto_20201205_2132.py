# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-05 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0025_auto_20201205_2130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='install_apm',
            field=models.BooleanField(default=False, verbose_name=b'Instal APM'),
        ),
        migrations.AlterField(
            model_name='server',
            name='install_consul',
            field=models.BooleanField(default=False, verbose_name=b'Install Consul'),
        ),
        migrations.AlterField(
            model_name='server',
            name='install_mq',
            field=models.BooleanField(default=False, verbose_name=b'Install RabbitMQ'),
        ),
        migrations.AlterField(
            model_name='server',
            name='install_mysql',
            field=models.BooleanField(default=False, verbose_name=b'Install MySQL'),
        ),
    ]
