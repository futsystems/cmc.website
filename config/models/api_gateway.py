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
class ApiGateway(models.Model):
    """
    api gateway
    """

    name = models.CharField('Api Gateway Name', max_length=50, default='ApiGateway')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    gw_type = models.CharField(max_length=20, choices=GATEWAY_TYPE, default='gw.api')
    base_url = models.CharField('Base Url', max_length=100, default='http://127.0.0.1')
    service_provider = models.ForeignKey(Consul, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)
    is_default = models.BooleanField('Is Default', default=False)
    description = models.CharField('Description', max_length=1000, default='', blank=True)
    date_created = models.DateTimeField('created time', auto_now=True, blank=True, null=True)
    default_config = models.ForeignKey('ApiGatewayConfig', verbose_name='Default Config', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    elastic_apm = models.ForeignKey(ElastAPM, verbose_name='ElasticAPM', on_delete=models.SET_NULL,
                                    default=None,
                                    blank=True, null=True)
    event_bus = models.ForeignKey(EventBus, verbose_name='EventBus', on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)

    services = models.ManyToManyField('Service', verbose_name='Used Services',
                                           blank=True)
    log_level = models.ForeignKey(LogItemGroup, verbose_name='LogLevel', on_delete=models.SET_NULL,default=None,
                                  blank=True, null=True)

    other_settings = models.ManyToManyField(SettingGroup, verbose_name='Other Settings', blank=True)

    pipeline_trigger = models.CharField('Pipeline Trigger', max_length=1000, default='', blank=True)

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

    @property
    def gateway_schema(self):
        return u'%s-%s' % (self.gw_type.lower(), self.env.lower())

    def __unicode__(self):
        return u'%s-%s / %s' % (self.gw_type.lower(), self.env.lower(), self.name)


    def default_config_title(self):
        if self.default_config is not None:
            return self.default_config.version
        else:
            return ''

    default_config_title.short_description = "Default Config"

    def generate_ocelot_config(self):
        global_cfg = {
            'BaseUrl':self.base_url,
        }

        if self.service_provider != None:
            global_cfg['ServiceDiscoveryProvider'] = self.service_provider.to_dict()

        config = {
            'Routes': [item.to_dict() for item in self.routes.all().order_by('name')],
            'GlobalConfiguration': global_cfg
        }

        return config

    def get_ocelot_config(self):

        if self.default_config is None:
            return  self.generate_ocelot_config()
        else:
            return json.loads(self.default_config.config)

    def get_config(self):
        dict={}
        dict['AllowedHosts'] = "*"
        if self.log_level is not None:
            dict['Logging'] = self.log_level.to_dict()

        if self.event_bus is not None:
            dict['EventBus'] = self.event_bus.to_dict()
            dict['EventBus']['SubscriptionClientName'] = self.gw_type

        if self.elastic_apm is not None:
            apm = self.elastic_apm.to_dict()
            apm['ServiceName'] = self.gw_type
            dict['ElasticAPM'] = apm

        if self.service_provider is not None:
            dict['ConsulServer'] = self.service_provider.to_dict()

        for service in self.services.all():
            key = 'Srv%sClient' % service.name
            dict[key] = {
                'Name': '%sRPC' % service.name,
                'MaxRetry': 3,
                'Discovery': {
                    'Consul': {
                        'Host': service.service_provider.host if service.service_provider is not None else 'localhost',
                        'Port': service.service_provider.port if service.service_provider is not None else 8500
                    }
                }
            }

        for setting_group in self.other_settings.all():
            dict[setting_group.group_name] = setting_group.to_dict()

        return dict

    def get_pillar(self):
        return {
            'env': self.env,
            'name': self.name,
            'pipeline_trigger': self.pipeline_trigger
        }