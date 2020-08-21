# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0028_logitem'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogItemGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Default', max_length=100, verbose_name=b'Name')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
                ('items', models.ManyToManyField(to='config.LogItem', verbose_name=b'Log Items')),
            ],
        ),
        migrations.AlterField(
            model_name='service',
            name='mysql_connections',
            field=models.ManyToManyField(to='config.MySqlConnection', verbose_name=b'MySql Connections'),
        ),
    ]
