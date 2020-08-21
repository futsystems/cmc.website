# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0026_auto_20200821_1448'),
    ]

    operations = [
        migrations.RenameField(
            model_name='service',
            old_name='support_http',
            new_name='support_api',
        ),
    ]
