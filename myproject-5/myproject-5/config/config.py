#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config(object):
    """Base config class."""
    # 版本
    VERSION = 'beta 0.1'
    # 项目名称
    PROJECTNAME = 'wegu_sql_demo'
    # 端口
    PORT = 8001
    ADMIN_USER = 'admin'
    ADMIN_EMAIL = 'darthrouge6@gmail.com'
    SECRET_KEY = '1234567890!@#$%^&*()'

class ProdConfig(Config):
    """Production config class."""

    # 是否开启调试
    DEBUG = False
    # 主机ip地址
    HOST = '0.0.0.0'

class SitConfig(Config):
    """Development config class."""
    # Open the DEBUG
    # 是否开启调试
    DEBUG = True
    # 主机ip地址
    HOST = '127.0.0.1'
    STATIC_URL = "http://{0}:{1}/static".format(HOST,Config.PORT)

    # # 数据库配置
    MYSQL_HOST = '127.0.0.1'  #此处修改为您的mysql的主机IP
    MYSQL_PORT = 3306         #此处修改为您的mysql的主机端口
    MYSQL_USER = 'root'       #此处修改为您的mysql的用户名称
    MYSQL_PASS = '12345'     #此处修改为您的mysql的用户密码
    MYSQL_DB = 'wegu_demo'    #此处修改为您的mysql的数据库名称

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:12345@localhost:3306/wegu_demo?charset=utf8"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
class DevConfig(Config):
    pass

# Default using Config settings, you can write if/else for different env
config = SitConfig()