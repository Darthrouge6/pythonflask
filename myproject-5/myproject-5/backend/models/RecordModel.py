#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db
from backend.views import login_manager
from flask import current_app
from backend.models.MachineModel import Machine
from backend.models.ProductModel import Product
from datetime import datetime



class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True)
    record_date = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    machine_id = db.Column(db.Integer, db.ForeignKey('machines.id'))
    part_id = db.Column(db.Integer, db.ForeignKey('products.id'))
    cycle = db.Column(db.Integer)
    furnace_quantity = db.Column(db.Integer)
    machine_downtime = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now)