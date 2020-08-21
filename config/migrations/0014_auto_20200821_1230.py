# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0013_auto_20200821_1215'),
    ]

    operations = [
        migrations.CreateModel(
            name='ElastAPM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_service_name', models.CharField(default=b'DefualtService', max_length=50, verbose_name=b'Default Service Name')),
                ('service_urls', models.CharField(default=b'http://apm.marvelsystem.net:8200', max_length=50, verbose_name=b'Host')),
                ('log_level', models.CharField(default=b'Debug', max_length=20, choices=[(b'Error', b'Error'), (b'Debug', b'Debug'), (b'Information', b'Information')])),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='EventBus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_subscription_client_name', models.CharField(default=b'SubscriptionClientName', max_length=50, verbose_name=b'Host')),
                ('retry_count', models.IntegerField(default=5, verbose_name=b'Retry Count')),
                ('host', models.CharField(default=b'test.marvelsystem.net', max_length=50, verbose_name=b'Host')),
                ('user_name', models.CharField(default=b'user', max_length=50, verbose_name=b'UserName')),
                ('password', models.CharField(default=b'user', max_length=50, verbose_name=b'Password')),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='elast_apm',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.ElastAPM', null=True, verbose_name=b'ElastAPM'),
        ),
        migrations.AddField(
            model_name='service',
            name='event_bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.EventBus', null=True, verbose_name=b'EventBus'),
        ),
    ]
