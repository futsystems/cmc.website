# -*- coding: utf-8 -*-
#!/usr/bin/python

import salt
from salt import client
#import salt.client
#import salt.config
#import salt.wheel
#import salt.runner
import logging
import urllib2
import json

import os.path

logger = logging.getLogger(__name__)

#if os.path.isfile('/etc/salt/master'):
#    opts = salt.config.master_config('/etc/salt/master')
#else:
#    opts = None
#wheel = salt.wheel.WheelClient(opts)

#runner = salt.runner.RunnerClient(opts)



def highstate(server):
    pillar = server.get_pillar()
    local = client.LocalClient()
    local.cmd(pillar.name, 'state.highstate', kwarg={'pillar': pillar})
    pass

def ping(server):
    pillar = server.get_pillar()
    local = client.LocalClient()
    local.cmd(pillar.name, 'test.ping')


def reboot(server):
    pillar = server.get_pillar()
    local = client.LocalClient()
    local.cmd(pillar.name, 'system.reboot')
