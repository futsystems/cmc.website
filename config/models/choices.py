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

ROUTE_SCHEME = (
    ('Consul', 'Consul'),
    ('Host', 'Host'),
    ('HostGroup', 'HostGroup'),
)

SERVICE_DISCOVERY_SCHEME = (
    ('Consul', 'Consul'),
    ('EndPoints', 'EndPoints'),
)

MYSQL_CHARSET= (
    ('utf8mb4', 'utf8mb4'),
    ('utf8', 'utf8'),
)


LOG_LEVEL_NET_CORE= (
    ('None', 'None'),
    ('Critical', 'Critical'),
    ('Error', 'Error'),
    ('Warning', 'Warning'),
    ('Information', 'Information'),
    ('Debug', 'Debug'),
    ('Trace', 'Trace'),
)

PRODUCT=(
    ('WeiSite', 'WeiSite'),
    ('WeiShop', 'WeiShop'),
)
