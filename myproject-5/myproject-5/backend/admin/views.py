#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Blueprint,render_template
from flask_login import current_user, login_required
from backend.account.views import login_required
from backend.models.RecordModel import Record
from backend.models import db
from utils.layout import layout
admin = Blueprint('admin', __name__)



@admin.route('/index')
def index():
    user = current_user
    records = db.session.query(Record).filter(Record.user_id == user.id).all()
    return layout('base/index.html',records = records)

