#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models
from choices import ENV_STAGE

class SettingGroup(models.Model):
    """
    Setting Group
    """
    group_name = models.CharField('GroupName', max_length=50, default='GroupName')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'%s-%s' % (self.group_name, self.env)

    def copy_to_env(self,env):
        group = SettingGroup()
        group.group_name = self.group_name
        group.env = env
        group.description = self.description
        group.save()
        for item in self.settings.all():
            setting = SettingItem()
            setting.setting_key = item.setting_key
            setting.setting_value = item.setting_value
            setting.is_array = item.is_array
            setting.setting_group = group
            setting.description = item.description
            setting.save()



    def to_dict(self):
        dict={}
        for setting in self.settings.all():
            dict[setting.setting_key] = setting.get_setting_value()

        return dict


class SettingItem(models.Model):
    """
    Setting Item
    """
    setting_key = models.CharField('SettingKey', max_length=50, default='SettingKey')
    setting_value = models.CharField('SettingValue', max_length=1000, default='SettingValue')
    is_array = models.BooleanField('Is Array', default=False)
    setting_group = models.ForeignKey(SettingGroup, verbose_name='SettingGroup', related_name='settings',  on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'Setting-%s' % self.setting_key

    def get_setting_value(self):
        if self.is_array:
            return self.setting_value.split(',')
        else:
            return self.setting_value


