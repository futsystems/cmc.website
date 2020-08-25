# -*- coding: utf-8 -*-

'''
author: qianbo
A module to pull data from NMS system via its API into the Pillar dictionary


Configuring the Wolf system ext_pillar
==================================

.. code-block:: yaml

  ext_pillar:
  - oms:
      api: http://oms.example.com/api/pillar/

Module Documentation
====================
'''

# Import python libs
import logging
import logging.config


import urllib2
import json

# Set up logging
logger = logging.getLogger(__name__)

def ext_pillar(minion_id, pillar,api):
    """
    Read pillar data from cmc system via its API.
    """
    info = 'minion_id:%s pillar:%s api:%s' % (minion_id, pillar, api)
    print info
    logger.info(info)
    api_url = api.get('api', 'http://127.0.0.1/nmscfg/api/pillar/query/')
    pillar_url = "%s%s" % (api_url,minion_id)

    return {
        'env': 'Development',

    }

    #logger.info("Querying NMS system Pillar for %r via url:%s" % ( minion_id,pillar_url))
    #try:
    #    response = urllib2.urlopen(pillar_url).read()
    #    result = json.loads(response)
    #    logger.info('Result:%s' % result)
    #except Exception, e:
    #    logger.exception(
    #        'Query NMS system failed! Error: %s' %(e)
    #    )
    #    return {}

    #return result


if __name__ == '__main__':
    ret = ext_pillar('host20-logic.deskhosted.com', 2 , api={'api':'http://salt.futsystems.com/nmscfg/api/'})
    logger.info('got ret:%s' % ret)


