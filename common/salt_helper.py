# -*- coding: utf-8 -*-
#!/usr/bin/python


import logging


logger = logging.getLogger(__name__)


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
