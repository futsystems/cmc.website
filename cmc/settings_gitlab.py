# -*- coding: utf-8 -*-
import sys,os
from conf import CONFIG_FILE

def get_gitlab_setting():
    import ConfigParser
    config=ConfigParser.ConfigParser()
    with open(CONFIG_FILE,'rb') as cfgfile:
        config.readfp(cfgfile)
        gitlab_url=config.get('gitlab', 'gitlab_url')
        gitlab_access_token=config.get('gitlab', 'gitlab_access_token')

    return {
        "url": gitlab_url,
        "access_token": gitlab_access_token
    }