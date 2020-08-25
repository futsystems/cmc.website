# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0031_auto_20200825_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='service',
            name='api_port',
            field=models.IntegerField(default=90, verbose_name=b'Http Port'),
        ),
    ]
