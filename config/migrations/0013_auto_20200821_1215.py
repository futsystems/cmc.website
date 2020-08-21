# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0012_service_used_services'),
    ]

    operations = [
        migrations.CreateModel(
            name='MySqlConnection',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Default', max_length=50, verbose_name=b'DB Connection Name')),
                ('host', models.CharField(default=b'test.marvelsystem.net', max_length=50, verbose_name=b'Host')),
                ('port', models.IntegerField(default=8500, verbose_name=b'Port')),
                ('user', models.CharField(default=b'user', max_length=50, verbose_name=b'User')),
                ('password', models.CharField(default=b'password', max_length=50, verbose_name=b'Password')),
                ('database', models.CharField(default=b'platform', max_length=50, verbose_name=b'Database')),
                ('charset', models.CharField(default=b'utf8mb4', max_length=20, choices=[(b'utf8mb4', b'utf8mb4'), (b'utf8', b'utf8')])),
                ('is_tracer', models.BooleanField(default=True, verbose_name=b'Is Tracer')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='service',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.Consul', null=True, verbose_name=b'Consul'),
        ),
        migrations.AddField(
            model_name='service',
            name='mysql_connections',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.MySqlConnection', null=True, verbose_name=b'DB Connnections'),
        ),
    ]
