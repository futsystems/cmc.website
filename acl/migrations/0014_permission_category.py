# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-11-03 07:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0013_permission_relation'),
    ]

    operations = [
        migrations.AddField(
            model_name='permission',
            name='category',
            field=models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Categoy'),
        ),
    ]
