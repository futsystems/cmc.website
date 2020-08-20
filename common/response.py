#!/usr/bin/python
# -*- coding: utf-8 -*-


class Response(object):
    def __init__(self, code, msg, data):
        self._code = code
        self._msg = msg
        self._data = data

    def to_dict(self):
        dict = {}
        dict['code']= self._code
        dict['msg'] = self._msg
        dict['data'] = self._data
        print dict

        return dict


class Error(Response):
    def __init__(self, msg, code=1):
        super(Error, self).__init__(code, msg, None)


class Success(Response):
    def __init__(self, data=None, msg='success',):
        super(Success, self).__init__(0, msg, data)