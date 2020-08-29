# -*- coding: utf-8 -*-
#!/usr/bin/python

import gitlab
from settings import GITLAB_SETTING


class GitlabAPI(object):
    def __init__(self):
        self._gitlab_url = GITLAB_SETTING.get('url', 'http://127.0.0.1')
        self._gitlab_access_token = GITLAB_SETTING.get('access_token', 'register_token')
        self._gl = gitlab.Gitlab(self._gitlab_url, private_token=self._gitlab_access_token)


    def get_runner_by_ip(self, ip):
        for item in self._gl.runners.list():
            if item.ip_address == ip:
                return  item
        return None

    def delete_runner_by_ip(self, ip):
        item = self.get_runner_by_ip(ip)
        if item is not None:
            self._gl.runners.delete(item.id)

    def get_portal_projects(self):
        paths = ['terminal-portal/admin', 'terminal-portal/console']
        return self.get_projects_in_paths(paths)

    def get_gateway_projects(self):
        paths = ['platform/gateway']
        return self.get_projects_in_paths(paths)

    def get_projects_by_service_names(self, services):
        paths = ['platform/%s' % name.lower() for name in services]
        return self.get_projects_in_paths(paths)

    def get_projects_in_paths(self, paths):
        projects = []
        for item in self._gl.projects.list(simple=True,per_page=100):
            if item.path_with_namespace in paths:
                projects.append(item)

        return projects
