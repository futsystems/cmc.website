# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-08-26 03:25
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0035_service_other_settings'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='mysql_connections',
            field=models.ManyToManyField(blank=True, to='config.MySqlConnection', verbose_name=b'MySql Connections'),
        ),
        migrations.AlterField(
            model_name='service',
            name='other_settings',
            field=models.ManyToManyField(blank=True, to='config.SettingGroup', verbose_name=b'Other Settings'),
        ),
        migrations.AlterField(
            model_name='settingitem',
            name='setting_group',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='settings', to='config.SettingGroup', verbose_name=b'SettingGroup'),
        ),
    ]