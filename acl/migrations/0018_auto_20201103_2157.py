# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-11-03 13:57
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('acl', '0017_group'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Permission',
            new_name='Page',
        ),
    ]
