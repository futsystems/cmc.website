# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0022_service_elastic_apm'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='mysql_connections',
        ),
    ]
