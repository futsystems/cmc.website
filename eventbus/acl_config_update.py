# -*- coding: utf-8 -*-

from message import IntegrationEvent


class CMCACLPermissionUpdate(IntegrationEvent):
    def __init__(self, env, product='WeiShop', tag=''):
        """

        :param gw_type: gw.api gw.api.app gw.api.admin and so on
        :param gw_env: Production Stage Development
        """
        super(CMCACLPermissionUpdate, self).__init__()
        self._product = product
        self._env = env
        self._tag = tag
        self._event_name = 'CMCACLPermissionnUpdateIntegrationEvent'

    @property
    def body(self):
        dict = super(CMCACLPermissionUpdate, self).body

        dict['product'] = self._product
        dict['tag'] = self._tag
        dict['env'] = self._env
        return dict


