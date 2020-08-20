# -*- coding: utf-8 -*-
import sys,os
from conf import CONFIG_FILE

def get_database_setting():
    """
    通过外层配置文件获得数据库设置
    """
    import ConfigParser
    config=ConfigParser.ConfigParser()
    with open(CONFIG_FILE,'rb') as cfgfile:
        config.readfp(cfgfile)
        host=config.get('db','host')
        database=config.get('db','database')
        dbuser=config.get('db','dbuser')
        dbpass=config.get('db','dbpass')

    return {
    "default": {
        "ENGINE": "django.db.backends.mysql", # Add "postgresql_psycopg2", "postgresql", "mysql", "sqlite3" or "oracle".
        "NAME": database,                       # Or path to database file if using sqlite3.
        "USER": dbuser,                             # Not used with sqlite3.
        "PASSWORD": dbpass,                         # Not used with sqlite3.
        "HOST": host,                             # Set to empty string for localhost. Not used with sqlite3.
        "PORT": "3306",                             # Set to empty string for default. Not used with sqlite3.
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        },
        'OPTIONS':{
         "init_command":"SET sql_mode='STRICT_TRANS_TABLES'"
        }
        },
    }