# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-08-19 03:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='upstream_header_transform',
            field=models.ManyToManyField(blank=True, related_name='HeaderTransform', to='config.HeaderTransform'),
        ),
    ]
