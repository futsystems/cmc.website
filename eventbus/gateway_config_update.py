# -*- coding: utf-8 -*-

from .message import IntegrationEvent


class CMCGatewayConfigUpdate(IntegrationEvent):
    def __init__(self,gw_type, gw_env):
        """

        :param gw_type: gw.api gw.api.app gw.api.admin and so on
        :param gw_env: Production Stage Development
        """
        super(CMCGatewayConfigUpdate, self).__init__()
        self._gw_type = gw_type
        self._gw_env = gw_env
        self._event_name = 'CMCGatewayConfigUpdateIntegrationEvent'

    @property
    def body(self):
        dict = super(CMCGatewayConfigUpdate, self).body

        dict['type'] = self._gw_type
        dict['env'] = self._gw_env
        return dict


