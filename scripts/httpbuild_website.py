#!/usr/bin/python
# -*- coding: utf-8 -*-

import os,thread,time
from flask import Flask,jsonify,request
import logging

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

@app.route('/build',methods=['POST','GET'])
def build_default():
    logging.info('start pull latest source')
    os.chdir("/opt/cmc.website/deploy")
    os.system("/opt/cmc.website/deploy/pull.sh")
    os.system('supervisorctl  restart django_cmc')
    return jsonify({'Code': 0, 'Message': 'restart success'})


if __name__ == '__main__':
    app.run('0.0.0.0', 8090,debug=False)
