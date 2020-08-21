# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0011_remove_apigatewayconfig_version_int'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='used_services',
            field=models.ManyToManyField(related_name='used_by_services', verbose_name=b'Used Services', to='config.Service', blank=True),
        ),
    ]
