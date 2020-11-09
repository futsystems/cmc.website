# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-11-09 06:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('basic', '0002_deliverycompany'),
    ]

    operations = [
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region_name', models.CharField(default=b'Name', max_length=50, verbose_name=b'CompanyName')),
                ('region_code', models.CharField(default=b'Code', max_length=50, verbose_name=b'CompanyCode')),
                ('description', models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Description')),
                ('parent', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='children', to='basic.Region', verbose_name=b'Parent')),
            ],
        ),
    ]
