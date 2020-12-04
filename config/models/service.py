from django.db import models

from db_connection import MySqlConnection
from elastic_apm import ElastAPM
from event_bus import EventBus
from consul import Consul
from log_item import LogItemGroup
from setting import SettingGroup
from choices import ENV_STAGE, SERVICE_DISCOVERY_SCHEME
from common import GitlabAPI

class Service(models.Model):
    """
    service
    """
    name = models.CharField('Service Name', max_length=50, default='Common',
                            help_text="no need RPC API,Common etc.,")

    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    used_services = models.ManyToManyField('Service', related_name='used_by_services', verbose_name='Used Services',
                                           blank=True)

    #service_provider = models.ForeignKey(Consul, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
    #                                     blank=True, null=True)
    discovery_scheme = models.CharField('Discovery Scheme', max_length=20, choices=SERVICE_DISCOVERY_SCHEME, default='Consul')

    host = models.CharField('Host', max_length=255, default='dev-api.marvelsystem.net', blank=True, null=True)
    #port = models.IntegerField('Port', default=80)

    mysql_connections = models.ManyToManyField(MySqlConnection, verbose_name='MySql Connections', blank=True)

    #elastic_apm = models.ForeignKey(ElastAPM, verbose_name='ElasticAPM', on_delete=models.SET_NULL,
    #                              default=None,
    #                              blank=True, null=True)
    #event_bus = models.ForeignKey(EventBus, verbose_name='EventBus', on_delete=models.SET_NULL,
    #                                      default=None,
    #                                      blank=True, null=True)

    support_rpc = models.BooleanField('RPC Support', default=True)
    rpc_port = models.IntegerField('RPC Port', default=91)

    support_api = models.BooleanField('HTTP Support', default=True)
    api_port = models.IntegerField('Http Port', default=90)

    production_tag = models.CharField(max_length=20, default='v1.0.0')
    log_level = models.ForeignKey(LogItemGroup, verbose_name='LogLevel', on_delete=models.SET_NULL,default=None,
                                  blank=True, null=True)

    other_settings = models.ManyToManyField(SettingGroup, verbose_name='Other Settings', blank=True)
    #used in for
    #section_name = models.CharField('Section Name', max_length=50, default=None, blank=True, null=True)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    pipeline_trigger = models.CharField('Pipeline Trigger', max_length=1000, default='', blank=True)

    merge_success = models.BooleanField('Merge Success', default=True)
    merge_message = models.CharField('Merge Message', max_length=500, default='', blank=True, null=True)


    class Meta:
        app_label = 'config'
        unique_together = ('name', 'env',)

    def __unicode__(self):
        return u'Service-%s' % (self.name)

    @property
    def has_other_settings(self):
        return self.other_settings.all().count() > 0

    def copy_to_env(self,env):
        service = Service()
        service.name = self.name
        service.env = env
        service.support_rpc = self.support_rpc
        service.rpc_port = self.rpc_port
        service.support_api = self.support_api
        service.api_port = self.api_port
        service.pipeline_trigger = self.pipeline_trigger
        service.save()

    def get_config(self, server):
        dict={}
        deploy = server.deploy
        ext_ip = server.ip
        # allowed hosts
        dict['AllowedHosts'] = "*"

        # log
        if self.log_level is not None:
            dict['Logging'] = self.log_level.to_dict()

        dict['System'] = self.get_system_config()

        if deploy is not None:
            dict['System']['Deploy'] = deploy.key
            dict['System']['Product'] = deploy.product_type

            # append event_bus,elastic_apm,service_provider of deploy
            if deploy.event_bus is not None:
                dict['EventBus'] = deploy.event_bus.to_dict()
                dict['EventBus']['SubscriptionClientName'] = self.name

            if deploy.elastic_apm is not None:
                apm = deploy.elastic_apm.to_dict()
                apm['ServiceName'] = self.name
                dict['ElasticAPM'] = apm

            if deploy.service_provider is not None:
                dict['ConsulServer'] = deploy.service_provider.to_dict()

        # mysql connection
        if self.mysql_connections.all().count() > 0:
            dict['DBConfig'] = [item.to_dict() for item in self.mysql_connections.all()]

        # used services
        for service in self.used_services.all():
            key = 'Srv%sClient' % service.name
            dict[key] = service.get_rpc_discovery_config(deploy)

        # api,rpc support
        if self.support_api:
            dict['APIServer'] ={
                'Name': '%sAPI' % self.name,
                'Host': ext_ip,
                'Protocol': 0,
                'Port': self.api_port
            }

        if self.support_rpc:
            dict['RPCServer'] = {
                'Name': '%sRPC' % self.name,
                'Host': ext_ip,
                'Protocol': 1,
                'Port': self.rpc_port
            }

        # setting
        for setting_group in self.other_settings.all():
            dict[setting_group.group_name] = setting_group.to_dict()
        return dict

    def get_system_config(self):
        return {

            'Product': 'NotSet',
            'Service': self.name,
            'Env': self.env,
            #'Version': '1.0',
        }

    def get_rpc_discovery_config(self, deploy):
        if self.discovery_scheme == 'Consul':
            return {
                'Name': '%sRPC' % self.name,
                'MaxRetry': 3,
                'Discovery': {
                    'Consul': {
                        'Host': deploy.service_provider.host if deploy.service_provider is not None else 'localhost',
                        'Port': deploy.service_provider.port if deploy.service_provider is not None else 8500
                    }
                }
            }
        elif self.discovery_scheme == 'EndPoints':
            return {
                'Name': '%sRPC' % self.name,
                'MaxRetry': 3,
                'Discovery': {
                    'EndPoints': [
                        {
                            'Host': self.host,
                            'Port': self.rpc_port
                        }
                    ]
                }
            }
        return {}

    def merge_project(self):
        if self.env == 'Development':
            path = 'platform/srv.%s' % self.name.lower()
            api = GitlabAPI()
            ret = api.merge_project(path)
            self.merge_success = ret[0]
            self.merge_message = ret[1]
            self.save()
        else:
            self.merge_success = True
            self.merge_message = 'Only Development Merge'

    def get_pillar(self):
        pillar = {
            'env': self.env,
            'name': self.name,
            'service_name': 'srv.%s' % self.name.lower(),
            'pipeline_trigger': self.pipeline_trigger,
        }

        pillar['api_port'] = self.api_port if self.support_api else 0
        pillar['rpc_port'] = self.rpc_port if self.support_rpc else 0
        pillar['tag'] = self.production_tag
        return pillar



