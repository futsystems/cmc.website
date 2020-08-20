from django.db import models

from .consul import Consul

from .choices import ENV_STAGE, GATEWAY_TYPE


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
    class Meta:
        unique_together = ('gw_type', 'env',)
        app_label = 'config'

    def __unicode__(self):
        return u'%s-%s / %s' % (self.gw_type.lower(), self.env.lower(), self.name)


    def default_config_title(self):
        if self.default_config is not None:
            return self.default_config.version
        else:
            return ''

    default_config_title.short_description = "Default Config"

    def get_ocelot_config(self):
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