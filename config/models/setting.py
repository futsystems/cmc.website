#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models

class SettingGroup(models.Model):
    """
    Setting Group
    """
    group_name = models.CharField('GroupName', max_length=50, default='GroupName')
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'SettingGroup-%s' % self.group_name

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


