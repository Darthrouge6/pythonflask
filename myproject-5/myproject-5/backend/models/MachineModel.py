#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db
from backend.views import login_manager
from flask import current_app

class Machine(db.Model):
    __tablename__ = 'machines'
    id = db.Column(db.Integer, primary_key=True)
    machine_name = db.Column(db.String(50))
    machine_type = db.Column(db.String(50))
