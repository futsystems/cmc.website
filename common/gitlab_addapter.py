# -*- coding: utf-8 -*-
#!/usr/bin/python

import gitlab
from gitlab import GitlabCreateError, GitlabMRClosedError, GitlabGetError

from settings import GITLAB_SETTING

import datetime
import time
import logging, traceback
logger = logging.getLogger(__name__)

class GitlabAPI(object):
    def __init__(self):
        self._gitlab_url = GITLAB_SETTING.get('url', 'http://127.0.0.1')
        self._gitlab_access_token = GITLAB_SETTING.get('access_token', 'register_token')
        self._gl = gitlab.Gitlab(self._gitlab_url, private_token=self._gitlab_access_token)


    def get_runner_by_ip(self, ip):
        for item in self._gl.runners.list():
            if item.ip_address == ip:
                return item
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

    def get_project_by_path(self, path):
        for item in self._gl.projects.list(simple=True, per_page=100):
            if item.path_with_namespace == path:
                return item

        return None

    def compare_repository(self, path, source, target):
        project = self.get_project_by_path(path)
        if project is None:
            return None
        logger.info('path:%s source:%s taget:%s' % (path, source, target))

        try:
            diff = project.repository_compare(source, target)
            #if path=='platform/srv.order':
            #    logger.info(diff)
            data = {
                'compare_timeout': diff['compare_timeout'],
                'compare_same_ref': diff['compare_same_ref'],
                'commits': []
            }
            if diff['compare_same_ref'] == False:
                for commit in diff['commits']:
                    data['commits'].append(
                        {
                            'author_name': commit['author_name'],
                            'author_email': commit['author_email'],
                            'title': commit['title'],
                            'web_url': commit['web_url'],
                            'created_at': commit['created_at'],
                            'short_id': commit['short_id'],
                        }
                    )
            data['commits'] = data['commits'][::-1]
            return data
        except GitlabGetError as e:
            return e.message

    def merge_project(self, path):
        project = self.get_project_by_path(path)
        if project is None:
            return [True, 'Project do not exist']

        diff = project.repository_compare('master', 'develop')
        if diff['commit'] is None:
            return [True, "No Commit"]


        mr_title = 'Merge:' + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            mr = project.mergerequests.create({'source_branch': 'develop', 'target_branch': 'master', 'title': mr_title})
        except GitlabCreateError as e:
            return [False, e.message]

        try:
            time.sleep(1)
            mr.approve()
            time.sleep(1)
            mr.merge()
            return [True, "Merge Success"]
        except GitlabMRClosedError as e:
            return [False, e.message]

    def create_runner(self, token, description, tags):
        """
        register a gitlab runner for server
        """
        runner = self._gl.runners.create(
            {'token': token, 'description': description, 'locked': False, 'run_untagged': False,
             'tag_list': ','.join(tags)})

        return (runner.attributes['id'], runner.attributes['token'])

    def delete_runner(self, runner_id):
        try:
            runner = self._gl.runners.get(str(runner_id))
            runner.delete()
        except Exception ,e:
            logging.error(traceback.format_exc())

