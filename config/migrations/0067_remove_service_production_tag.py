# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-08 03:31
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0066_auto_20201205_1735'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='production_tag',
        ),
    ]