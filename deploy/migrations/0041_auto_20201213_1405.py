# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-13 06:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0040_auto_20201213_1221'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='version',
            unique_together=set([]),
        ),
        migrations.RemoveField(
            model_name='version',
            name='node_name',
        ),
        migrations.RemoveField(
            model_name='version',
            name='node_type',
        ),
        migrations.RemoveField(
            model_name='version',
            name='version',
        ),
    ]
