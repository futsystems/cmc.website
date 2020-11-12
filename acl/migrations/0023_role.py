# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-11-04 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0022_group_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=b'Name', max_length=50, verbose_name=b'Name')),
                ('key', models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Key')),
                ('description', models.CharField(blank=True, default=b'', max_length=100, verbose_name=b'Description')),
                ('env', models.CharField(choices=[(b'Production', b'Production'), (b'Staging', b'Staging'), (b'Development', b'Development')], default=b'Development', max_length=20)),
                ('sort', models.PositiveIntegerField(default=0)),
                ('permissions', models.ManyToManyField(blank=True, to='acl.Permission', verbose_name=b'Permissions')),
            ],
            options={
                'ordering': ['sort'],
            },
        ),
    ]