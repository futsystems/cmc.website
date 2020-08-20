from django.db import models

from api_gateway import ApiGateway


class ApiGatewayConfig(models.Model):
    """
    api gateway config file
    """
    version = models.CharField(verbose_name='Version', max_length=20, default='1.0')
    config = models.TextField(verbose_name='config')
    gateway = models.ForeignKey(ApiGateway, verbose_name='ApiGateway',related_name='configs')
    #is_default = models.BooleanField('Is Default', default=False)
    description = models.TextField('Description',default='', blank=True)
    date_created = models.DateTimeField('created time', auto_now_add=True, blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'[%s]-%s' % (self.gateway, self.version)
