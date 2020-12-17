#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway, Portal
from choices import LOCATION, NODETYPE, PRODUCTTYPE
from config.models.choices import ENV_STAGE
from config.models import Consul
from config.models import EventBus, ElastAPM, LogItemGroup
from config.models import WeiXinMiniprogramTemplate

class Deploy(models.Model):
    """
    Deploy
    """
    name = models.CharField('Name', max_length=100, default='DeployName', unique=True)
    product_type = models.CharField(max_length=20, choices=PRODUCTTYPE, default='WeiShop')
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    suffix = models.CharField('Suffix', max_length=100, default='suffix', unique=True)

    gateway_domain_name = models.CharField('Gateway DomainName', max_length=100, default='gateway.marvelsystem.net')

    portal_domain_name = models.CharField('Portal DomainName', max_length=100, default='portal.marvelsystem.net')

    website_domain_name = models.CharField('Website DomainName', max_length=100, default='portal.marvelsystem.net')

    service_provider = models.ForeignKey(Consul, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    elastic_apm = models.ForeignKey(ElastAPM, verbose_name='ElasticAPM', on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)

    event_bus = models.ForeignKey(EventBus, verbose_name='EventBus', on_delete=models.SET_NULL,
                                          default=None,
                                          blank=True, null=True)

    log_level = models.ForeignKey(LogItemGroup, verbose_name='LogLevel', on_delete=models.SET_NULL, default=None,
                                  blank=True, null=True)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    weixin_miniprogram_template = models.ForeignKey(WeiXinMiniprogramTemplate, verbose_name='WeiXin Miniprogram Template', on_delete=models.SET_NULL, default=None,
                                blank=True, null=True, related_name='deploys')

    key = models.CharField('Key', max_length=100, default='', blank=True)

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.product_type, self.suffix)

    def get_key(self):
        return '%s-%s' % (self.product_type, self.suffix)

    def save(self, *args, **kwargs):
        self.key = self.get_key()
        super(Deploy, self).save(*args, **kwargs)


    def to_info_dict(self):
        dict = {
            'product': self.product_type,
            'deploy': self.key,
            'name': self.name,
            'env': self.env,
        }
        return dict

    def get_version(self, node_type, node_name):
        item = self.versions.filter(project__node_name=node_name, project__node_type=node_type).first()
        if item is None:
            return 'v1.0.0'
        if item.tag is None:
            return 'v1.0.0'
        return item.tag.tag

    def get_version_id(self, node_type, node_name):
        item = self.versions.filter(project__node_name=node_name, project__node_type=node_type).first()
        if item is None:
            return None
        return item.pk




