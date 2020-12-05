# -*- coding: utf-8 -*-

from message import IntegrationEvent


class CMCGatewayConfigUpdate(IntegrationEvent):
    def __init__(self, deploy, tag=''):
        super(CMCGatewayConfigUpdate, self).__init__()
        self._deploy = deploy
        self._tag = tag
        self._event_name = 'CMCGatewayConfigUpdateIntegrationEvent'

    @property
    def body(self):
        content = super(CMCGatewayConfigUpdate, self).body
        content['deploy'] = self._deploy
        content['tag'] = self._tag

        return content


