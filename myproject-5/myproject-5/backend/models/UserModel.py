#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask_login import UserMixin,AnonymousUserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from backend.models import db
from backend.views import login_manager
from flask import current_app
from backend.models.DepartmentModel import Department
from backend.models.MachineModel import Machine
from backend.models.ProductModel import Product
from backend.models.RecordModel import Record
from datetime import datetime

class Permission:
    GENERAL = 0x01
    ADMINISTER = 0xff

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    index = db.Column(db.String(64))
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles = {
            'Worker': (Permission.GENERAL, 'main', True),
            'Administrator': (
                Permission.ADMINISTER,
                'admin',
                False  # grants all permissions
            )
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.index = roles[r][1]
            role.default = roles[r][2]
            db.session.add(role)
        db.session.commit()

    def __repr__(self):
        return '<Role \'%s\'>' % self.name



class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(64))
    lastname = db.Column(db.String(64))
    username = db.Column(db.String(64), index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    # age = db.Column(db.Integer)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    mobile = db.Column(db.String(200))
    # address = db.Column(db.String(200))
    sick_days = db.Column(db.Integer)
    quality_complaints = db.Column(db.Integer)
    bonus = db.Column(db.Integer)
    join_date = db.Column(db.DateTime, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    total_cleanliness_amount = db.Column(db.Integer)
    active = db.Column(db.Boolean)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        print(self)
        if self.role is None:
            if self.username == current_app.config['ADMIN_USER'] or self.email == current_app.config['ADMIN_EMAIL']:
                self.role = Role.query.filter_by(
                    permissions=Permission.ADMINISTER).first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_admin(self):
        return self.can(Permission.ADMINISTER)



    @property
    def password(self):
        raise AttributeError('`password` is not a readable attribute')
    #encryption
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)
    #verify password
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
    #The format returned by the query
    def __repr__(self):
        return '<User \'%s\'>' % self.username

class AnonymousUser(AnonymousUserMixin):
    def can(self, _):
        return False

    def is_admin(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))