from django.db import models

from config.models.choices import ENV_STAGE


class PermissionConfig(models.Model):
    """
    api gateway config file
    """
    version = models.CharField(verbose_name='Version', max_length=20, default='1.0')
    config = models.TextField(verbose_name='config')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    description = models.TextField('Description',default='', blank=True)
    md5 = models.CharField(verbose_name='Md5', max_length=50, default='NotSet')
    date_created = models.DateTimeField('created time', auto_now_add=True, blank=True)

    class Meta:
        app_label = 'acl'

    def __unicode__(self):
        return u'Permission-[%s]-%s' % (self.env, self.version)
