# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-09 09:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0036_auto_20201208_1359'),
    ]

    operations = [
        migrations.AddField(
            model_name='nodeinfo',
            name='node_type',
            field=models.CharField(default=b'Portal', max_length=20),
        ),
    ]
