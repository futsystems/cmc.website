#!/usr/bin/python

import json
import logging
logger = logging.getLogger(__name__)

def __virtual__():
    return 'demo'

def test(minion_id):
    logging.info('demo.test is called')
    return (False, 'minion do not exist')

