# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('config', '0002_auto_20200819_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='route',
            name='authentication_scheme',
            field=models.CharField(default=b'NoAuth', max_length=9, verbose_name=b'Auth Schema', choices=[(b'NoAuth', b'NoAuth'), (b'Bearer', b'Bearer'), (b'HMAC', b'HMAC')]),
        ),
        migrations.AlterField(
            model_name='route',
            name='http_handler_options',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.HttpHandlerOption', null=True, verbose_name=b'HttpHandler'),
        ),
        migrations.AlterField(
            model_name='route',
            name='load_balancer',
            field=models.CharField(default=b'LeastConnection', max_length=20, choices=[(b'NoLoadBalancer', b'NoLoadBalancer'), (b'LeastConnection', b'LeastConnection'), (b'RoundRobin', b'RoundRobin')]),
        ),
        migrations.AlterField(
            model_name='route',
            name='rate_limite_options',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.RateLimitOption', null=True, verbose_name=b'RateLimit'),
        ),
        migrations.AlterField(
            model_name='route',
            name='upstream_header_transform',
            field=models.ManyToManyField(db_constraint=b'HeaderTransform', to='config.HeaderTransform', blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='apigateway',
            unique_together=set([('gw_type', 'env')]),
        ),
    ]
