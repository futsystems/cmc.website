# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ApiGateway',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'ApiGateway', max_length=50, verbose_name=b'Api Gateway Name')),
                ('env', models.CharField(default=b'Development', max_length=20, choices=[(b'Production', b'Production'), (b'Staging', b'Staging'), (b'Development', b'Development')])),
                ('gw_type', models.CharField(default=b'gw.api', max_length=20, choices=[(b'gw.api.admin', b'gw.api.admin'), (b'gw.api.app', b'gw.api.app'), (b'gw.api.console', b'gw.api.console'), (b'gw.api', b'gw.api')])),
                ('base_url', models.CharField(default=b'http://127.0.0.1', max_length=100, verbose_name=b'Base Url')),
                ('is_default', models.BooleanField(default=False, verbose_name=b'Is Default')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Consul',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Consul', max_length=50, verbose_name=b'Consul Name')),
                ('host', models.CharField(default=b'test.marvelsystem.net', max_length=50, verbose_name=b'host')),
                ('port', models.IntegerField(default=8500, verbose_name=b'Port')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HeaderTransform',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'HeaderTrannsform', max_length=50, verbose_name=b'Name')),
                ('header_key', models.CharField(default=b'X-Forwarded-For', max_length=50, verbose_name=b'HeaderKey')),
                ('header_value', models.CharField(default=b'{RemoteIpAddress}', max_length=50, verbose_name=b'HeaderValue')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='HttpHandlerOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Default', max_length=50, verbose_name=b'HttpHandlerOption Name')),
                ('allow_auto_redirect', models.BooleanField(default=True, verbose_name=b'AllowAutoRedirect')),
                ('use_cookie_container', models.BooleanField(default=True, verbose_name=b'UseCookieContainer')),
                ('user_tracing', models.BooleanField(default=True, verbose_name=b'UseTracing')),
                ('max_connections_per_server', models.IntegerField(default=500, verbose_name=b'MaxConnectionsPerServer')),
            ],
        ),
        migrations.CreateModel(
            name='HttpMethod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Get', max_length=50, verbose_name=b'Name')),
                ('method', models.CharField(default=b'Get', max_length=50, verbose_name=b'Method')),
            ],
        ),
        migrations.CreateModel(
            name='RateLimitOption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Default', max_length=50, verbose_name=b'RateLimitOption Name')),
                ('client_whitelist', models.CharField(default=b'', max_length=255, verbose_name=b'ClientWhitelist', blank=True)),
                ('enable_rate_limiting', models.BooleanField(default=True, verbose_name=b'EnableRateLimiting')),
                ('period', models.CharField(default=b'', max_length=255, verbose_name=b'Period')),
                ('period_timespan', models.IntegerField(default=0, verbose_name=b'PeriodTimespan')),
                ('limit', models.IntegerField(default=0, verbose_name=b'Limit')),
            ],
        ),
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Route', max_length=50, verbose_name=b'Route Name')),
                ('priority', models.IntegerField(default=0, verbose_name=b'Priority')),
                ('upstream_path_template', models.CharField(default=b'/', max_length=255, verbose_name=b'UpstreamPathTemplate')),
                ('downstream_path_template', models.CharField(default=b'/', max_length=255, verbose_name=b'DownstreamPathTemplate')),
                ('downstream_scheme', models.CharField(default=b'http', max_length=9, choices=[(b'http', b'http'), (b'https', b'https')])),
                ('load_balancer', models.CharField(default=b'LeastConnection', max_length=20, choices=[(b'NoBalancer', b'NoBalancer'), (b'LeastConnection', b'LeastConnection')])),
                ('downstream_host', models.CharField(default=None, max_length=255, null=True, verbose_name=b'DownstreamHost', blank=True)),
                ('downstream_port', models.CharField(default=None, max_length=255, null=True, verbose_name=b'DownstreamPort', blank=True)),
                ('authentication_scheme', models.CharField(default=b'NoAuth', max_length=9, verbose_name=b'AuthenticationProviderKey', choices=[(b'NoAuth', b'NoAuth'), (b'Bearer', b'Bearer'), (b'HMAC', b'HMAC')])),
                ('authorization_scopes', models.CharField(default=b'', max_length=255, verbose_name=b'AllowedScopes', blank=True)),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
                ('api_gateway', models.ForeignKey(related_name='routes', on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.ApiGateway', null=True, verbose_name=b'ApiGateway')),
                ('http_handler_options', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.HttpHandlerOption', null=True, verbose_name=b'HttpHandlerOption')),
                ('rate_limite_options', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.RateLimitOption', null=True, verbose_name=b'RateLimitOption')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(default=b'Common', max_length=50, verbose_name=b'Service Name')),
                ('description', models.CharField(default=b'', max_length=1000, verbose_name=b'Description', blank=True)),
            ],
        ),
        migrations.AddField(
            model_name='route',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.Service', null=True, verbose_name=b'Serice'),
        ),
        migrations.AddField(
            model_name='route',
            name='upstream_header_transform',
            field=models.ManyToManyField(db_constraint=b'HeaderTransform', to='config.HeaderTransform', blank=True),
        ),
        migrations.AddField(
            model_name='route',
            name='upstream_http_method',
            field=models.ManyToManyField(related_name='methodsUpstreamHttpMethod', to='config.HttpMethod', blank=True),
        ),
        migrations.AddField(
            model_name='apigateway',
            name='service_provider',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, default=None, blank=True, to='config.Consul', null=True, verbose_name=b'Consul'),
        ),
    ]
