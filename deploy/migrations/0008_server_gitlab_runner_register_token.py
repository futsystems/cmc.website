# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-08-29 03:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0007_auto_20200828_2355'),
    ]

    operations = [
        migrations.AddField(
            model_name='server',
            name='gitlab_runner_register_token',
            field=models.CharField(choices=[(b'Production', b'Production'), (b'Staging', b'Staging'), (b'Development', b'Development')], default=b'register_token', max_length=100),
        ),
    ]
