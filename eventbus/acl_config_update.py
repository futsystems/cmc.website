# -*- coding: utf-8 -*-

from message import IntegrationEvent


class CMCACLPermissionUpdate(IntegrationEvent):
    def __init__(self, deploy, tag=''):
        super(CMCACLPermissionUpdate, self).__init__()
        self._deploy = deploy
        self._tag = tag
        self._event_name = 'CMCACLPermissionnUpdateIntegrationEvent'

    @property
    def body(self):
        content = super(CMCACLPermissionUpdate, self).body
        content['deploy'] = self._deploy
        content['tag'] = self._tag
        return content


class CMCACLRoleUpdate(IntegrationEvent):
    def __init__(self, deploy, tag=''):
        super(CMCACLRoleUpdate, self).__init__()
        self._deploy = deploy
        self._tag = tag
        self._event_name = 'CMCACLRoleUpdateIntegrationEvent'

    @property
    def body(self):
        content = super(CMCACLRoleUpdate, self).body
        content['deploy'] = self._deploy
        content['tag'] = self._tag
        return content


