# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-11-30 07:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0057_service_production_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='portal',
            name='partion_info_api_domain',
            field=models.CharField(blank=True, default=b'test-www.marvelsystem.net', max_length=1000, verbose_name=b'PartionInfoDomain'),
        ),
    ]