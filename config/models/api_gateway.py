from django.db import models

from elastic_apm import ElastAPM
from event_bus import EventBus
from consul import Consul

from choices import ENV_STAGE, GATEWAY_TYPE

import json
from eventbus import EventBublisher
from eventbus import CMCGatewayConfigUpdate
from setting import SettingGroup
from log_item import LogItemGroup
import urlparse
from common import GitlabAPI
import logging
logger = logging.getLogger(__name__)

class ApiGateway(models.Model):
    """
    api gateway
    """

    name = models.CharField('Api Gateway Name', max_length=50, default='ApiGateway')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    gw_type = models.CharField(max_length=20, choices=GATEWAY_TYPE, default='gw.api')
    description = models.CharField('Description', max_length=1000, default='', blank=True)
    date_created = models.DateTimeField('created time', auto_now=True, blank=True, null=True)
    default_config = models.ForeignKey('ApiGatewayConfig', verbose_name='Default Config', on_delete=models.SET_NULL,
                                       default=None, blank=True, null=True)
    services = models.ManyToManyField('Service', verbose_name='Used Services',
                                           blank=True)

    log_level = models.ForeignKey(LogItemGroup, verbose_name='LogLevel', on_delete=models.SET_NULL,default=None,
                                  blank=True, null=True)

    other_settings = models.ManyToManyField(SettingGroup, verbose_name='Other Settings', blank=True)

    pipeline_trigger = models.CharField('Pipeline Trigger', max_length=1000, default='', blank=True)
    merge_success = models.BooleanField('Merge Success', default=True)
    merge_message = models.CharField('Merge Message', max_length=500, default='', blank=True, null=True)

    __original_default_config = None

    def __init__(self, *args, **kwargs):
        super(ApiGateway, self).__init__(*args, **kwargs)
        self.__original_default_config = self.default_config

    def save(self, force_insert=False, force_update=False, *args, **kwargs):
        fire_event = False
        if self.default_config != self.__original_default_config:
            fire_event = True
        super(ApiGateway, self).save(force_insert, force_update, *args, **kwargs)
        self.__original_default_config = self.default_config

        if fire_event:
            ev = CMCGatewayConfigUpdate(self.gw_type, self.env)
            EventBublisher().send_message(ev)

    class Meta:
        unique_together = ('gw_type', 'env',)
        app_label = 'config'

    def get_system_config(self):
        return {
            'Product': 'WeiShop',
            'Service': 'APIGateway',
            'Stage': self.env,
            'Version': '1.0',
        }

    @property
    def gateway_schema(self):
        return u'%s-%s' % (self.gw_type.lower(), self.env.lower())

    def __unicode__(self):
        return u'%s-%s / %s' % (self.gw_type.lower(), self.env.lower(), self.name)

    def merge_project(self):
        if self.env == 'Development':
            path = 'platform/gateway'
            api = GitlabAPI()
            ret = api.merge_project(path)
            self.merge_success = ret[0]
            self.merge_message = ret[1]
            self.save()
        else:
            self.merge_success = True
            self.merge_message = 'Only Development Merge'

    def default_config_title(self):
        if self.default_config is not None:
            return self.default_config.version
        else:
            return ''

    default_config_title.short_description = "Default Config"

    def generate_ocelot_config(self):
        global_cfg = {
            'BaseUrl': 'http://127.0.0.1',
        }

        #if self.service_provider != None:
        global_cfg['ServiceDiscoveryProvider'] = None

        config = {
            'Routes': [item.to_dict() for item in self.routes.all().order_by('name')],
            'GlobalConfiguration': global_cfg
        }

        return config

    def get_ocelot_config(self, server):

        if self.default_config is None:
            cfg = self.generate_ocelot_config()
        else:
            cfg = json.loads(self.default_config.config)

        # use server info to fill ocelot config
        if server is not None:
            cfg['GlobalConfiguration']['ServiceDiscoveryProvider'] = server.deploy.service_provider.to_dict()
            cfg['GlobalConfiguration']['BaseUrl'] = 'https://%s' % server.deploy.gateway_domain_name

        return cfg

    def get_config(self, server):
        dict={}
        deploy = server.deploy
        ext_ip = server.ip

        dict['AllowedHosts'] = "*"
        if self.log_level is not None:
            dict['Logging'] = self.log_level.to_dict()

        # event_bus,elastic_apm,service_provider of deploy
        if deploy is not None:
            if deploy.event_bus is not None:
                dict['EventBus'] = deploy.event_bus.to_dict()
                dict['EventBus']['SubscriptionClientName'] = self.gw_type

            if deploy.elastic_apm is not None:
                apm = deploy.elastic_apm.to_dict()
                apm['ServiceName'] = self.gw_type
                dict['ElasticAPM'] = apm

            if deploy.service_provider is not None:
                dict['ConsulServer'] = deploy.service_provider.to_dict()

        # services
        for service in self.services.all():
            key = 'Srv%sClient' % service.name
            dict[key] = {
                'Name': '%sRPC' % service.name,
                'MaxRetry': 3,
                'Discovery': {
                    'Consul': {
                        'Host': deploy.service_provider.host if deploy.service_provider is not None else 'localhost',
                        'Port': deploy.service_provider.port if deploy.service_provider is not None else 8500
                    }
                }
            }

        # setting
        for setting_group in self.other_settings.all():
            dict[setting_group.group_name] = setting_group.to_dict()

        # cmc gateway
        dict['CMCGatewayConfig'] = {
            "GatewayIP": server.ip if server is not None else 'localhost',
            "Url": "http://cmc.marvelsystem.net",
            "Type": self.gw_type,
            "Env": self.env
        }

        dict['System'] = self.get_system_config()
        return dict

    def get_pillar(self, deploy):
        base_url = 'http://127.0.0.1'
        doamin_name = 'localhost'
        if deploy is not None:
            base_url = 'https://%s' % deploy.gateway_domain_name
            doamin_name = deploy.gateway_domain_name

        return {
            'env': self.env,
            'name': self.name,
            'type': self.gw_type,
            'base_url': base_url,
            'domain_name': doamin_name,
            'pipeline_trigger': self.pipeline_trigger
        }