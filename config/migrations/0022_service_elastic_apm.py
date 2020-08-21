# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0021_auto_20200821_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='elastic_apm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.ElastAPM', null=True, verbose_name=b'ElasticAPM'),
        ),
    ]
