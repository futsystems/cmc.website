# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0017_auto_20200821_1248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elastapm',
            name='log_level',
            field=models.CharField(default=b'Debug', max_length=20, verbose_name=b'LogLevel', choices=[(b'Error', b'Error'), (b'Debug', b'Debug'), (b'Information', b'Information')]),
        ),
        migrations.AlterField(
            model_name='eventbus',
            name='default_subscription_client_name',
            field=models.CharField(default=b'SubscriptionClientName', max_length=50, verbose_name=b'SubscriptionClientName'),
        ),
    ]
