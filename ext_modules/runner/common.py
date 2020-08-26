# -*- coding: utf-8 -*-
#!/usr/bin/python

import salt
import salt.client
import salt.config
import salt.wheel
import salt.runner
import logging
import urllib2
import json

logger = logging.getLogger(__name__)

opts = salt.config.master_config('/etc/salt/master')
wheel = salt.wheel.WheelClient(opts)
local = salt.client.LocalClient()
runner = salt.runner.RunnerClient(opts)


def get_pillar(minion_id):
    """
    获得某个minion的pillar信息
    """
    pillar_url = "%s?minion_id=%s" % ('http://127.0.0.1/deploy/server/pillar/', minion_id)
    logger.info("Querying NMS system Pillar for %r via url:%s" % (minion_id, pillar_url))
    try:
        response = urllib2.urlopen(pillar_url).read()
        result = json.loads(response)
        logger.info('Result:%s' % result)
        return result
    except Exception, e:
        logger.exception(
            'Query NMS system failed! Error: %s' %(e)
        )
        return None

def console(data):
    """
    输出数据
    """
    print "runner console data:%s" % data


def auth_minion(minion_id='minion'):
    """
    通过Minion_ID来验证节点合法性
    """
    api_url = 'http://127.0.0.1/nmscfg/api/minion/valid/%s' % minion_id
    logger.info('Try to valid minion:%s via url:%s' % (minion_id, api_url))

    try:
        response = urllib2.urlopen(api_url).read()
        result = json.loads(response)
        logger.info('Result:%s' % result)
        if result['error_code'] == 0:
            logger.info('Accept Minion:%s' % minion_id )
            wheel.cmd('key.accept',[minion_id])
        else:
            logger.warn('Reject Minion:%s' % minion_id )
            wheel.cmd('key.reject',[minion_id])
        return result['error_code'] == 0
    except Exception, e:
        logger.exception(
            'Valid Minion Error: %s' %(e)
        )
        return False