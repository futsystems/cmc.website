# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0015_eventbus_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='env',
            field=models.CharField(default=b'Development', max_length=20, choices=[(b'Production', b'Production'), (b'Staging', b'Staging'), (b'Development', b'Development')]),
        ),
        migrations.AlterUniqueTogether(
            name='service',
            unique_together=set([('name', 'env')]),
        ),
    ]
