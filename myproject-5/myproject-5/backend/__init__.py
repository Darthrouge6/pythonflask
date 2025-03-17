#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
from flask import Flask
from config.config import config
from backend.urls import register
from backend.models import db  #第二课增加内容
from backend.views import login_manager #第三课增加内容
from flask_login import current_user

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_TEMPLATE_FOLDER = os.path.join(BASE_DIR,'frontend')

def create_app():
    # initialization
    app = Flask(__name__,template_folder=BASE_TEMPLATE_FOLDER,static_folder=os.path.join(BASE_DIR,'frontend','static'))
    app.secret_key = app.config['SECRET_KEY']

    # Import configuration items
    app.config.from_object(config)
    # register route
    register(app)
    # registration database
    db.init_app(app)
    # Register login component
    login_manager.init_app(app)
    # Register variables to jinja global variables
    app.add_template_global(app.config['PROJECTNAME'], 'PROJECTNAME')
    app.add_template_global(app.config['STATIC_URL'], 'STATIC_URL')


    # hook before request execution
    @app.before_request
    def before_request():
       pass

    return app
