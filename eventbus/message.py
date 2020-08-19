# -*- coding: utf-8 -*-

import uuid
import datetime

class IntegrationEvent(object):
    def __init__(self):
        self._event_name='IntegrationEvent'
        self._id = str(uuid.uuid1())
        self._creation_date = datetime.datetime.now()

    @property
    def name(self):
        return  self._event_name

    @property
    def body(self):
        dict={}
        dict['eventName'] = self._event_name
        dict['id'] = self._id
        dict['creationDate'] = self._creation_date.strftime('%Y-%m-%d %H:%M:%S')

        return  dict

