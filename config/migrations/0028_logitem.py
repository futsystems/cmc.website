# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0027_auto_20200821_1451'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('prefix', models.CharField(default=b'Microsoft', max_length=100, verbose_name=b'Prefix')),
                ('level', models.CharField(default=b'Information', max_length=20, choices=[(b'Error', b'Error'), (b'Debug', b'Debug'), (b'Information', b'Information')])),
            ],
        ),
    ]
