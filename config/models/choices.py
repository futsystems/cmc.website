#!/usr/bin/python
# -*- coding: utf-8 -*-


GATEWAY_TYPE = {
    ('gw.api', 'gw.api'),
    ('gw.api.app', 'gw.api.app'),
    ('gw.api.admin', 'gw.api.admin'),
    ('gw.api.console', 'gw.api.console'),
}

ENV_STAGE = (
    ('Production', 'Production'),
    ('Staging', 'Staging'),
    ('Development', 'Development'),
)

DOWNSTREAM_SCHEME = (
    ('http', 'http'),
    ('https', 'https'),
)

AUTH_SCHEME = (
    ('NoAuth', 'NoAuth'),
    ('Bearer', 'Bearer'),
    ('HMAC', 'HMAC'),
)

LOADBALANCER_SCHEME = (
    ('NoLoadBalancer', 'NoLoadBalancer'),
    ('LeastConnection', 'LeastConnection'),
    ('RoundRobin', 'RoundRobin'),
)
