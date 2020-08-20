#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,thread,time
from flask import Flask,jsonify,request
import logging
import  time

def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    # create console handler and set level to info
    handler = logging.StreamHandler()
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('[%(name)s:%(lineno)d %(funcName)s] [%(levelname)s]- %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create error file handler and set level to error
    handler = logging.FileHandler(os.path.join(output_dir, "error.log"), "w", encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    formatter = logging.Formatter('[%(name)s:%(lineno)d %(funcName)s] [%(levelname)s]- %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    handler = logging.FileHandler(os.path.join(output_dir, "all.log"), "w")
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(name)s:%(lineno)d %(funcName)s] [%(levelname)s]- %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


initialize_logger('../../logs/')



app = Flask(__name__)

@app.route('/ms/build',methods=['POST','GET'])
def build_default():
    service = request.args.get('service')

    logging.info('start build service:%s' % service)

    os.environ['DOTNET_CLI_HOME'] = "/opt/%s" % service
    os.chdir("/opt/%s" % service)
    os.system("/opt/%s/build.sh" % service)
    os.chdir("/opt/%s/bin" % service)

    time.sleep(3)
    os.system('supervisorctl  restart %s' % service)

    return jsonify({'Code': 0, 'Message': 'build %s success' % service})

if __name__ == '__main__':
    app.run('0.0.0.0', 8099, debug=False)
