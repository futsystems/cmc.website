# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0029_auto_20200821_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='log_level',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.LogItemGroup', null=True, verbose_name=b'LogLevel'),
        ),
        migrations.AlterField(
            model_name='elastapm',
            name='log_level',
            field=models.CharField(default=b'Debug', max_length=20, verbose_name=b'LogLevel', choices=[(b'None', b'None'), (b'Critical', b'Critical'), (b'Error', b'Error'), (b'Warning', b'Warning'), (b'Information', b'Information'), (b'Debug', b'Debug'), (b'Trace', b'Trace')]),
        ),
        migrations.AlterField(
            model_name='logitem',
            name='level',
            field=models.CharField(default=b'Information', max_length=20, choices=[(b'None', b'None'), (b'Critical', b'Critical'), (b'Error', b'Error'), (b'Warning', b'Warning'), (b'Information', b'Information'), (b'Debug', b'Debug'), (b'Trace', b'Trace')]),
        ),
    ]
