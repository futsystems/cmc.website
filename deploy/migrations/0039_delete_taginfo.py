# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-13 04:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0038_taginfo'),
    ]

    operations = [
        migrations.DeleteModel(
            name='TagInfo',
        ),
    ]
