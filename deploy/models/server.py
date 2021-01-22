#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.db import models
from config.models import Service, ApiGateway, Portal, AppH5
from choices import LOCATION, NODETYPE
from config.models.choices import ENV_STAGE
from ip_white_list import IP

class ServerManager(models.Manager):

    def in_white_list(self, ip):
        is_server = self.filter(ip=ip).first() is not None
        in_whitelist = IP.objects.filter(ip=ip,is_blocked=False).first() is not None
        return  is_server or in_whitelist




class Server(models.Model):
    """
    server
    """
    name = models.CharField('Name', max_length=100, default='Node1', unique=True)
    location = models.CharField(max_length=20, choices=LOCATION, default='hangzhou')
    ip = models.CharField('IP', max_length=50, default='127.0.0.1')
    node_type = models.CharField(max_length=20, choices=NODETYPE, default='Service')

    deploy = models.ForeignKey('Deploy', verbose_name='Deploy', related_name='servers', default= 1)

    index = models.CharField(max_length=20, default='01')

    # 服务器安装服务
    installed_services = models.ManyToManyField(Service, verbose_name='Installed Services', blank=True)

    # 服务器如果部署网关 则部署绑定的网关设置
    gateway = models.ForeignKey(ApiGateway, verbose_name='Gateway', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    # 服务器部署 portal
    portal = models.ForeignKey(Portal, verbose_name='Portal', on_delete=models.SET_NULL, default=None,
                                         blank=True, null=True)

    app = models.ForeignKey(AppH5, verbose_name='App', on_delete=models.SET_NULL, default=None,
                               blank=True, null=True)


    install_mysql = models.BooleanField('Install MySQL', default=False)
    install_mq = models.BooleanField('Install RabbitMQ', default=False)
    install_consul = models.BooleanField('Install Consul', default=False)
    install_apm = models.BooleanField('Instal APM', default=False)


    #服务器部署portal 绑定的portal设置
    description = models.CharField('Description', max_length=1000, default='', blank=True)

    gitlab_runner_register_token = models.CharField(max_length=100, default='register_token', blank=True)

    gitlab_runner_id = models.IntegerField('Runner Id', default=None, null=True)

    gitlab_runner_auth_token = models.CharField(max_length=100, blank=True, null=True, default=None)

    objects = ServerManager()

    class Meta:
        app_label = 'deploy'

    def __unicode__(self):
        return u'%s-%s' % (self.name, self.ip)


    def save(self, *args, **kwargs):
        if self.deploy is not None:
            self.name = self.host_name

        super(Server, self).save(*args, **kwargs)

    @property
    def host_name(self):
        # 生产环境才通过deploy信息进行host_name生成
        if self.deploy.env == 'Production':
            if self.deploy.env == 'Production':
                return ('%s-%s-%s-%s' % (self.node_type, self.deploy.product_type, self.deploy.suffix, self.index)).lower()

        return self.name

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
            'env': self.deploy.env,
            'node_type': self.node_type,
            'deploy': self.deploy.env,
        }

        if self.deploy is None:
            data['deploy'] = None
        else:
            data['deploy'] = self.deploy.key

        # basic components
        data['components'] = {
            'mq': self.install_mq,
            'mysql': self.install_mysql,
            'consul': self.install_consul,
            'apm': self.install_apm,
            'docker': self.deploy.env == 'Staging',
            'dotnet': self.installed_services.all().count() > 0 or self.gateway is not None,
            'cms_screen_shot': self.installed_services.filter(name='CMS').count() > 0,
        }

        # Gateway Node
        if self.gateway is not None:
            data['gateway'] = self.gateway.get_pillar(self.deploy)

        # Portal
        if self.portal is not None:
            data['portal'] = self.portal.get_pillar(self.deploy)
            #当前安装app在portal服务器 后期迁移到不同的服务器
            data['app'] = self.app.get_pillar(self.deploy)

        # Service Node
        if self.installed_services.all().count() > 0:
            data['services'] = [item.get_pillar(self.deploy) for item in self.installed_services.all()]
            if self.installed_services.filter(name='CMS').count() > 0:
                data['cms_screenshot'] = True

        # development and staging env install gitlab runner
        if self.deploy.env == 'Development' or self.deploy.env == 'Staging':
            if self.gitlab_runner_id is not None:
                runner = {}
                runner['register_url'] = 'https://gitlab.marvelsystem.net/'
                runner['register_token'] = self.gitlab_runner_register_token
                runner['auth_token'] = self.gitlab_runner_auth_token
                if self.deploy.env == 'Development':
                    runner['tags'] = 'development,%s' % self.name
                if self.deploy.env == 'Staging':
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
        if self.deploy.env == 'Development':
            tags.append('development')
        if self.deploy.env == 'Staging':
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








