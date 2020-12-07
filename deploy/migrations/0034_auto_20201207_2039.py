# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2020-12-07 12:39
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0033_version'),
    ]

    operations = [
        migrations.AlterField(
            model_name='version',
            name='deploy',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='versions', to='deploy.Deploy', verbose_name=b'Deploy'),
        ),
        migrations.AlterField(
            model_name='version',
            name='node_name',
            field=models.CharField(choices=[(b'APIGateway', b'Gateway_APIGateway'), ('ActionLog', 'Service_ActionLog'), ('Aggregate', 'Service_Aggregate'), ('CMS', 'Service_CMS'), ('Comment', 'Service_Comment'), ('Common', 'Service_Common'), ('Favorite', 'Service_Favorite'), ('Logistics', 'Service_Logistics'), ('Manager', 'Service_Manager'), ('Market', 'Service_Market'), ('Media', 'Service_Media'), ('Member', 'Service_Member'), ('Merchant', 'Service_Merchant'), ('Notification', 'Service_Notification'), ('Open', 'Service_Open'), ('Order', 'Service_Order'), ('Partion', 'Service_Partion'), ('Payment', 'Service_Payment'), ('Points', 'Service_Points'), ('Product', 'Service_Product'), ('ShoppingCart', 'Service_ShoppingCart'), ('WeiXin', 'Service_WeiXin')], default=b'APIGateway', max_length=20, verbose_name=b'Node Name'),
        ),
        migrations.AlterField(
            model_name='version',
            name='node_type',
            field=models.CharField(choices=[(b'Portal', b'Portal'), (b'Gateway', b'Gateway'), (b'Service', b'Service')], default=b'Service', max_length=20, verbose_name=b'Node Type'),
        ),
    ]