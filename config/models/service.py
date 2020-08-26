from django.db import models
from .choices import ENV_STAGE
from db_connection import MySqlConnection
from elastic_apm import ElastAPM
from event_bus import EventBus
from consul import Consul
from log_item import LogItemGroup
from setting import SettingGroup
from choices import ENV_STAGE
class Service(models.Model):
    """
    service
    """
    name = models.CharField('Service Name', max_length=50, default='Common',
                            help_text="no need RPC API,Common etc.,")

    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    used_services = models.ManyToManyField('Service', related_name='used_by_services', verbose_name='Used Services',
                                           blank=True)

    service_provider = models.ForeignKey(Consul, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    mysql_connections = models.ManyToManyField(MySqlConnection, verbose_name='MySql Connections', blank=True)

    elastic_apm = models.ForeignKey(ElastAPM, verbose_name='ElasticAPM', on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)
    event_bus = models.ForeignKey(EventBus, verbose_name='EventBus', on_delete=models.SET_NULL,
                                          default=None,
                                          blank=True, null=True)

    support_rpc = models.BooleanField('RPC Support', default=True)
    rpc_port = models.IntegerField('RPC Port', default=91)

    support_api = models.BooleanField('HTTP Support', default=True)
    api_port = models.IntegerField('Http Port', default=90)

    log_level = models.ForeignKey(LogItemGroup, verbose_name='LogLevel', on_delete=models.SET_NULL,default=None,
                                  blank=True, null=True)

    other_settings = models.ManyToManyField(SettingGroup, verbose_name='Other Settings', blank=True)
    #used in for
    #section_name = models.CharField('Section Name', max_length=50, default=None, blank=True, null=True)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    pipeline_trigger = models.CharField('Pipeline Trigger', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'
        unique_together = ('name', 'env',)

    def __unicode__(self):
        return u'Service-%s' % (self.name)

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

    def get_config(self):
        dict={}

        if self.log_level is not None:
            dict['Logging'] = self.log_level.to_dict()

        if self.event_bus is not None:
            dict['EventBus'] = self.event_bus.to_dict()

        if self.elastic_apm is not None:
            apm = self.elastic_apm.to_dict()
            apm['ServiceName'] = self.name
            dict['ElasticAPM'] = apm

        if self.mysql_connections.all().count()>0:
            dict['DBConfig']= [item.to_dict() for item in self.mysql_connections.all()]

        if self.service_provider is not None:
            dict['ConsulServer'] = self.service_provider.to_dict()

        for service in self.used_services.all():
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

        if self.support_api:
            dict['APIServer'] ={
                'Name': '%sAPI' % self.name,
                'Host': 'localhost',
                'Protocol': 0,
                'Port': self.api_port
            }

        if self.support_rpc:
            dict['RPCServer'] = {
                'Name': '%sRPC' % self.name,
                'Host': 'localhost',
                'Protocol': 1,
                'Port': self.rpc_port
            }

        for setting_group in self.other_settings.all():
            dict[setting_group.group_name] = setting_group.to_dict()
        return dict


    def get_pillar(self):
        return {
            'env': self.env,
            'name': self.name,
            'service_name': 'srv.%s' % self.name.lower(),
            'pipeline_trigger': self.pipeline_trigger
        }


