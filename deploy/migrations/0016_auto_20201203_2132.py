# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-03 13:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0015_nodeinfo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='nodeinfo',
            name='node_type',
        ),
        migrations.AddField(
            model_name='deploy',
            name='key',
            field=models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Key'),
        ),
        migrations.AddField(
            model_name='nodeinfo',
            name='node_service',
            field=models.CharField(default=b'Gateway', max_length=20),
        ),
    ]
