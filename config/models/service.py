from django.db import models
from .choices import ENV_STAGE
from db_connection import MySqlConnection
from elastic_apm import ElastAPM
from event_bus import EventBus
from consul import Consul


class Service(models.Model):
    """
    service
    """
    name = models.CharField('Service Name', max_length=50, default='Common')

    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')

    used_services = models.ManyToManyField('Service', related_name='used_by_services', verbose_name= 'Used Services', blank=True)

    service_provider = models.ForeignKey(Consul, verbose_name='Consul', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    mysql_connections = models.ManyToManyField(MySqlConnection, verbose_name='DB', default=None,
                                       blank=True, null=True)

    elastic_apm = models.ForeignKey(ElastAPM, verbose_name='ElasticAPM', on_delete=models.SET_NULL,
                                  default=None,
                                  blank=True, null=True)
    event_bus = models.ForeignKey(EventBus, verbose_name='EventBus', on_delete=models.SET_NULL,
                                          default=None,
                                          blank=True, null=True)
    #used in for
    #section_name = models.CharField('Section Name', max_length=50, default=None, blank=True, null=True)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'
        unique_together = ('name', 'env',)

    def __unicode__(self):
        return u'Service-%s' % (self.name)