#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.db import models



from service import  Service
from option_http_handler import HttpHandlerOption
from option_rate_limit import RateLimitOption
from http_method import HttpMethod
from header_transform import HeaderTransform
from api_gateway import  ApiGateway


from .choices import DOWNSTREAM_SCHEME, AUTH_SCHEME, LOADBALANCER_SCHEME, ROUTE_SCHEME

class Route(models.Model):
    """
    route item
    """
    name = models.CharField('Route Name', max_length=50, default='Route')
    priority = models.IntegerField('Priority', default=0)
    api_gateway = models.ForeignKey(ApiGateway,related_name='routes', verbose_name='ApiGateway', on_delete=models.SET_NULL,
                                            default=None, blank=True, null=True)

    upstream_path_template = models.CharField('UpstreamPathTemplate', max_length=255, default='/')
    upstream_http_method = models.ManyToManyField(HttpMethod, related_name='methods' 'UpstreamHttpMethod', blank=True)
    upstream_header_transform = models.ManyToManyField(HeaderTransform, 'HeaderTransform', blank=True)

    downstream_path_template = models.CharField('DownstreamPathTemplate', max_length=255, default='/')
    downstream_scheme = models.CharField(max_length=9, choices=DOWNSTREAM_SCHEME, default='http')

    service = models.ForeignKey(Service, verbose_name='Serice', on_delete=models.SET_NULL, default=None, blank=True, null=True)
    load_balancer = models.CharField(max_length=20, choices=LOADBALANCER_SCHEME, default='LeastConnection')

    #route_scheme = models.CharField('Route Scheme', max_length=20, choices=ROUTE_SCHEME, default='Consul')

    #downstream_host = models.CharField('DownstreamHost', max_length=255, default='dev-api.marvelsystem.net', blank=True, null=True)
    #downstream_port = models.CharField('DownstreamPort', max_length=255, default=80, blank=True, null=True)

    authentication_scheme = models.CharField('Auth Schema',max_length=9, choices=AUTH_SCHEME, default='NoAuth')
    authorization_scopes = models.CharField('AllowedScopes', max_length=255, blank=True, default='')


    rate_limite_options = models.ForeignKey(RateLimitOption, verbose_name='RateLimit', on_delete=models.SET_NULL, default=None, blank=True, null=True)
    http_handler_options= models.ForeignKey(HttpHandlerOption, verbose_name='HttpHandler', on_delete=models.SET_NULL, default=None, blank=True, null=True)

    description = models.CharField('Description', max_length=1000, default='', blank=True)

    class Meta:
        app_label = 'config'

    def __unicode__(self):
        return u'Route-%s' % self.name

    @property
    def env(self):
        if self.api_gateway is None:
            return  None
        else:
            return self.api_gateway.env

    def copy_to_gateway(self, gateway):
        route = Route()
        route.name = self.name
        route.api_gateway = gateway
        route.priority = self.priority
        route.upstream_path_template = self.upstream_path_template

        route.downstream_path_template = self.downstream_path_template
        route.downstream_scheme = self.downstream_scheme

        route.load_balancer = self.load_balancer
        route.authentication_scheme = self.authentication_scheme
        route.authorization_scopes = self.authorization_scopes
        route.rate_limite_options = self.rate_limite_options
        route.http_handler_options = self.http_handler_options
        route.description = self.description
        route.save()

        for item in self.upstream_http_method.all():
            route.upstream_http_method.add(item)

        for item in self.upstream_header_transform.all():
            route.upstream_header_transform.add(item)

        route.save()



    @property
    def route_target(self):
        if self.service is not None:
            if self.service.discovery_scheme == 'Consul':
                return 'Consul [%sAPI-%s]' % (self.service.name, self.short_load_balancer())
            elif self.service.discovery_scheme == 'EndPoints':
                return 'EndPoints [%s:%s]' % (self.service.host, self.service.api_port)
        else:
            return "No Service"

    def short_load_balancer(self):
        if self.load_balancer == 'NoLoadBalancer':
            return 'No'
        elif self.load_balancer == 'LeastConnection':
            return 'Least'
        elif self.load_balancer == 'RoundRobin':
            return 'Round'

    short_load_balancer.short_description = "BALANCER"

    def http_handler_options_title(self):
        if self.http_handler_options is None:
            return 'default'
        else:
            return  self.http_handler_options

    http_handler_options_title.short_description = "HttpHandler"

    @property
    def is_consul(self):
        return self.service is not None

    def get_upstream_header_transform(self):
        dict = {}
        for item in self.upstream_header_transform.all():
            dict[item.header_key] = item.header_value
        return dict

    def to_dict(self):
        """
        generate route config
        """
        dict = {}
        dict['Priority'] = self.priority
        dict['UpstreamPathTemplate'] = self.upstream_path_template
        dict['UpstreamHttpMethod'] = [method.method for method in self.upstream_http_method.all()]
        dict['UpstreamHeaderTransform'] = self.get_upstream_header_transform()

        dict['DownstreamPathTemplate'] = self.downstream_path_template
        dict['DownstreamScheme'] = self.downstream_scheme

        if self.service is not None:
            if self.service.discovery_scheme == 'Consul':
                dict['ServiceName'] = '%sAPI' % self.service.name
                dict['LoadBalancerOptions'] = {'Type':self.load_balancer}
            elif self.service.discovery_scheme == 'EndPoints':
                dict['DownstreamHostAndPorts'] = [{'Host': self.service.host, "Port": self.service.api_port}]

        if self.authentication_scheme != 'NoAuth':
            auth_dict = {'AuthenticationProviderKey': self.authentication_scheme}
            if self.authorization_scopes != '':
                auth_dict['AllowedScopes'] = self.authorization_scopes.split(',')
            dict['AuthenticationOptions'] = auth_dict

        if self.rate_limite_options is not None:
            dict['RateLimitOptions'] = self.rate_limite_options.to_dict()

        if self.http_handler_options is not None:
            dict['HttpHandlerOptions'] = self.http_handler_options.to_dict()

        return dict
