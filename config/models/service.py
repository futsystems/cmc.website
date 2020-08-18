from django.db import models
from .choices import  ENV_STAGE

class Service(models.Model):
    """
    service
    """
    name = models.CharField('Service Name', max_length=50, default='Common')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'Service-%s' % (self.name)