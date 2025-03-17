#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_login import LoginManager



# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'

