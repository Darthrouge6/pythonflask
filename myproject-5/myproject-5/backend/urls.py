#!/usr/bin/python
# -*- coding: UTF-8 -*-
from backend.account.views import account
from backend.admin.views import admin

# Blueprint Registration
def register(app):
    app.register_blueprint(account, url_prefix='/account', strict_slashes=False)
    app.register_blueprint(admin, url_prefix='/admin', strict_slashes=False)