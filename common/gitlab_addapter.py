# -*- coding: utf-8 -*-
#!/usr/bin/python

import gitlab
from settings import GITLAB_SETTING


class GitlabAPI(object):
    def __init__(self):
        self._gitlab_url = getattr(GITLAB_SETTING, 'url', 'http://127.0.0.1')
        self._gitlab_access_token = getattr(GITLAB_SETTING, 'access_token', 'register_token')
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