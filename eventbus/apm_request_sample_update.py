# -*- coding: utf-8 -*-

from message import IntegrationEvent


class CMCAPMRequestSampleChange(IntegrationEvent):
    def __init__(self, deploy, service, apm_sample):
        super(CMCAPMRequestSampleChange, self).__init__()
        self._deploy = deploy
        self._service = service
        self._apm_sample = apm_sample
        self._event_name = 'CMCAPMRequestSampleChangeIntegrationEvent'

    @property
    def body(self):
        content = super(CMCAPMRequestSampleChange, self).body
        content['deploy'] = self._deploy
        content['service'] = self._service
        content['requestSample'] = self._apm_sample

        return content


