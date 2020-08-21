# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0023_remove_service_mysql_connections'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='mysql_connections',
            field=models.ManyToManyField(default=None, to='config.MySqlConnection', null=True, verbose_name=b'DB', blank=True),
        ),
    ]
