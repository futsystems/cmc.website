# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-11-03 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0016_permission_sort'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=b'Title', max_length=50, verbose_name=b'Title')),
                ('name', models.CharField(default=b'Name', max_length=50, verbose_name=b'Name')),
                ('env', models.CharField(choices=[(b'Production', b'Production'), (b'Staging', b'Staging'), (b'Development', b'Development')], default=b'Development', max_length=20)),
                ('description', models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Description')),
                ('sort', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
