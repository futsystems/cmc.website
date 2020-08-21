# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0014_auto_20200821_1230'),
    ]

    operations = [
        migrations.AddField(
            model_name='eventbus',
            name='description',
            field=models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True),
        ),
    ]
