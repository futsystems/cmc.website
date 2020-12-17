# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-16 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0041_auto_20201213_1405'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeiXinMiniprogramTemplate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'App', max_length=100, unique=True, verbose_name=b'Name')),
                ('app_id', models.CharField(default=b'wx000000000000', max_length=20, unique=True)),
                ('web_hook', models.CharField(default=b'', max_length=255)),
                ('description', models.CharField(blank=True, default=b'', max_length=1000, verbose_name=b'Description')),
            ],
        ),
    ]