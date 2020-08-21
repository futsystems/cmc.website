# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0019_auto_20200821_1250'),
    ]

    operations = [
        migrations.AddField(
            model_name='consul',
            name='env',
            field=models.CharField(default=b'Development', max_length=20, choices=[(b'Production', b'Production'), (b'Staging', b'Staging'), (b'Development', b'Development')]),
        ),
    ]
