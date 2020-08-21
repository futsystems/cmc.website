# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0018_auto_20200821_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventbus',
            name='default_subscription_client_name',
            field=models.CharField(default=b'SubscriptionClientName', max_length=50, verbose_name=b'ClientName'),
        ),
    ]
