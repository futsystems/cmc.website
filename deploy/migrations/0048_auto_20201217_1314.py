# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-17 05:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0047_deploy_enable_node_info_filter'),
    ]

    operations = [
        migrations.AlterField(
            model_name='server',
            name='deploy',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='servers', to='deploy.Deploy', verbose_name=b'Deploy'),
        ),
    ]