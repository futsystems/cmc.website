#!/usr/bin/python
# -*- coding: utf-8 -*-

from server import Server
from deploy import Deploy
from node_info import NodeInfo
from ip_white_list import IP
from version import Version



from django.db.models.signals import post_save
from django.dispatch import receiver
from config.models import Service
from eventbus import EventBublisher, CMCAPMRequestSampleChange

import logging
logger = logging.getLogger(__name__)

# method for send event if service's apm sample changed
@receiver(post_save, sender=Service, dispatch_uid="update_stock_count")
def send_amp_sample_change_event(sender, instance, **kwargs):
    logger.info('service is chagned,env:%s' % instance.env)
    from deploy import Deploy
    for item in Deploy.objects.filter(env=instance.env).all():
        ev = CMCAPMRequestSampleChange(item.key, instance.name, instance.apm_sample)
        if item.event_bus is not None:
            EventBublisher(item.event_bus).send_message(ev)