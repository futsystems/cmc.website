# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0030_auto_20200821_1524'),
    ]

    operations = [
        migrations.CreateModel(
            name='Server',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Node1', max_length=100, verbose_name=b'Name')),
                ('location', models.CharField(default=b'hangzhou', max_length=20, choices=[(b'hangzhou', b'hangzhou')])),
                ('ip', models.CharField(default=b'127.0.0.1', max_length=50, verbose_name=b'IP')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
                ('installed_services', models.ManyToManyField(to='config.Service', verbose_name=b'Installed Services', blank=True)),
            ],
        ),
    ]
