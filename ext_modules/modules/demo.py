#!/usr/bin/python

import json
import logging
logger = logging.getLogger(__name__)

def __virtual__():
    return 'demo'

def test():
  return 'i am test'

