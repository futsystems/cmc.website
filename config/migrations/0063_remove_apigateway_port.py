# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-04 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0062_auto_20201204_2237'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='apigateway',
            name='port',
        ),
    ]