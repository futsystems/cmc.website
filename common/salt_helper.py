# -*- coding: utf-8 -*-
#!/usr/bin/python

import salt

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
    from salt import client
    pillar = server.get_pillar()
    local = client.LocalClient()
    local.cmd(server.name, 'state.highstate', kwarg={'pillar': pillar})
    pass

def ping(server):
    from salt import client
    pillar = server.get_pillar()
    local = client.LocalClient()
    local.cmd(server.name, 'test.ping')


def reboot(server):
    from salt import client
    pillar = server.get_pillar()
    local = client.LocalClient()
    local.cmd(server.name, 'system.reboot')
