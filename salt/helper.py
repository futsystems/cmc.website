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

logger = logging.getLogger(__name__)

opts = salt.config.master_config('/etc/salt/master')
wheel = salt.wheel.WheelClient(opts)
local = salt.client.LocalClient()
runner = salt.runner.RunnerClient(opts)



def highstate(server):
    pillar = server.get_pillar()
    local.cmd(pillar.name, 'state.highstate', kwarg={'pillar': pillar})

def ping(server):
    pillar = server.get_pillar()
    local.cmd(pillar.name, 'test.ping')

def reboot(server):
    pillar = server.get_pillar()
    local.cmd(pillar.name, 'system.reboot')