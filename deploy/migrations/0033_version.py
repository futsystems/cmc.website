# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-07 12:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0032_nodeinfo_health_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('node_type', models.CharField(choices=[(b'Portal', b'Portal'), (b'Gateway', b'Gateway'), (b'Service', b'Service')], default=b'Service', max_length=20)),
                ('node_name', models.CharField(default=b'APIGateway', max_length=20)),
                ('version', models.CharField(default=b'v1.0.0', max_length=50, verbose_name=b'Version')),
                ('deploy', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='versions', to='deploy.Deploy', verbose_name=b'Consul')),
            ],
        ),
    ]