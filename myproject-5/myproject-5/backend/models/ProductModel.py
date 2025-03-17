#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db
from backend.views import login_manager
from flask import current_app


class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    max_capacity = db.Column(db.Integer)
    per_furnace_time = db.Column(db.Integer)
    machine_nr = db.Column(db.Integer)
    serial_number = db.Column(db.Integer)
