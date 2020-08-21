# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0020_consul_env'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='service',
            name='elast_apm',
        ),
        migrations.AlterField(
            model_name='elastapm',
            name='default_service_name',
            field=models.CharField(default=b'DefualtService', help_text=b'will be replaced by service name', max_length=50, verbose_name=b'Default Service Name'),
        ),
        migrations.AlterField(
            model_name='eventbus',
            name='default_subscription_client_name',
            field=models.CharField(default=b'SubscriptionClientName', help_text=b'will be replaced by service name', max_length=50, verbose_name=b'ClientName'),
        ),
    ]
