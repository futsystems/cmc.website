#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway, Portal
from choices import LOCATION, NODETYPE
from config.models.choices import ENV_STAGE

class ServerManager(models.Manager):

    def in_white_list(self,ip):
        return self.filter(ip=ip).first() is not None


class Server(models.Model):
    """
    server
    """
    name = models.CharField('Name', max_length=100, default='Node1', unique=True)
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    env = models.CharField(max_length=20, choices=ENV_STAGE, default='Development')
    node_type = models.CharField(max_length=20, choices=NODETYPE, default='Service')

    #服务器安装服务
    installed_services = models.ManyToManyField(Service, verbose_name='Installed Services', blank=True)

    #服务器如果部署网关 则部署绑定的网关设置
    gateway = models.ForeignKey(ApiGateway, verbose_name='Gateway', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    portal = models.ForeignKey(Portal, verbose_name='Portal', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)
    #服务器部署portal 绑定的portal设置
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    gitlab_runner_register_token = models.CharField(max_length=100, default='register_token', blank=True)

    gitlab_runner_id = models.IntegerField('Runner Id', default=8080)

    gitlab_runner_auth_token = models.CharField(max_length=100, blank=True, null=True, default=None)

    objects = ServerManager()

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.name, self.ip)


    @property
    def function_title(self):
        items=[]
        if self.installed_services.count()>0:
            items.append('Service')
        if self.gateway is not None:
            items.append('Gateway')
        if self.portal is not None:
            items.append('Portal')
        return ','.join(items)

    def get_pillar(self):
        data = {
            'name': self.name,
            'ip': self.ip,
            'env': self.env,
            'node_type': self.node_type,
        }
        if self.node_type == 'Service':
            data['services'] = [item.get_pillar() for item in self.installed_services.all()]
        if self.node_type == 'Gateway':
            data['gateway'] = None if self.gateway is None else self.gateway.get_pillar()
            if self.installed_services.filter(name='CMS').count() > 0:
                data['cms_screenshot'] = True

        if self.portal is not None:
            data['portal'] = self.portal.get_pillar()

        if self.env == 'Development' or self.env == 'Staging':
            if self.gitlab_runner_id is not None:
                runner = {}
                runner['register_url'] = 'https://gitlab.marvelsystem.net/'
                runner['register_token'] = self.gitlab_runner_register_token
                runner['auth_token'] = self.gitlab_runner_auth_token
                if self.env == 'Development':
                    runner['tags'] = 'development,%s' % self.name
                if self.env == 'Staging':
                    runner['tags'] = 'staging,production,%s' % self.name
                runner['identifier'] = '%s-runner' % self.name

                data['gitlab-runner'] = runner

        return data


    def register_runner(self):
        from common import GitlabAPI
        api = GitlabAPI()

        #如果已经注册过 则直接删除原来的runner并重新注册新的runner
        if self.gitlab_runner_id is not None:
            api.delete_runner(self.gitlab_runner_id)

        #初始化参数
        description = '%s-runner' % self.name
        tags= []
        if self.env == 'Development':
            tags.append('development')
        if self.env == 'Staging':
            tags.append('staging')
            tags.append('production')
        tags.append(self.name)

        runner_id, runner_auth_token = api.create_runner(self.gitlab_runner_register_token,description,tags)
        self.gitlab_runner_id = runner_id
        self.gitlab_runner_auth_token = runner_auth_token
        self.save()

        #将项目注册到runner
        if self.gateway is not None:
            for project in api.get_gateway_projects():
                project.runners.create({'runner_id':runner_id})
        if self.portal is not None:
            for project in api.get_portal_projects():
                project.runners.create({'runner_id': runner_id})

        if self.installed_services.count()>0:
            names = ['srv.%s' % service.name.lower() for service in self.installed_services.all()]
            for project in api.get_projects_by_service_names(names):
                project.runners.create({'runner_id': runner_id})

    def sync_project_runner(self):
        """
        当设定改变后 修改runner中包含的project
        """
        pass








