#!/usr/bin/python
# -*- coding: UTF-8 -*-

from flask import Blueprint,request,render_template,jsonify,flash
from flask import redirect,url_for,abort
from sqlalchemy import func
from backend.models.UserModel import User,Role
from backend.models.RecordModel import Record
from backend.models.ProductModel import Product
from backend.models import db
from flask_login import login_user,login_required,logout_user,current_user
from functools import wraps
from backend.models.UserModel import Permission
from utils.layout import layout
from datetime import datetime
from backend.account.cal_bonus import calculate_monthly_bonus,calculate_work_days

#Account blueprint Visit http://host:port/account The sub-links of this link will jump here
account = Blueprint('account', __name__)


def permission_required(permission):
    """Restrict a view to users with the given permission."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


# Admin access required
def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)

# Visit http://host:port/account/register This link will jump here
@account.route('/register',methods=(["GET","POST"]))
#The above link is bound to this method, we request a return in json format to the browser or interface
def register():
    if request.method == 'POST':
        try:
            form = request.form
            user = User(firstname=form['firstname'], lastname=form['lastname'],username=form['username'],email=form['email'],password=form['password'],department_id=form['departmentId'],mobile=form['mobile'])
            db.session.add(user)
            db.session.commit()
            return redirect(url_for(request.args.get('next') or 'account.login'))
        except Exception as e:
            print(e)
            abort(403)
    return render_template('/account/register.html')

@account.route('/login',methods=(["GET","POST"]))
def login():
    if request.method == "POST":
        form = request.form #Get login form
        user = User.query.filter_by(username=form['username']).first()  #Find user information
        if user is not None and user.password_hash is not None and user.verify_password(form['password']):  #Check if the password is correct
            login_user(user,True)  #login operation
            flash('You are now logged in. Welcome back!', 'success')
            return redirect( url_for(request.args.get('next') or 'admin.index'))
        else:
            flash('Invalid email or password.', 'error')
    return render_template('/account/login.html')

@account.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('admin.index'))


@account.route('/users')
@login_required
def user_list():
    Role.insert_roles()
    user_list = User.query.outerjoin(Role, User.role_id == Role.id).all()
    return layout('/account/users.html',users=user_list)


@account.route('/edituser',methods=(["GET","POST"]))
@login_required
def user_edit():
    if request.method == 'POST':
        try:
            form = request.form
            use_info = User.query.filter(User.id == form['id']).first()
            use_info.email = form['email']
            use_info.role_id = form['role_id']
            db.session.commit()
            flash('Modified!', 'success')
        except Exception as e:
            print(e)
            flash('Fail！', 'error')
        return redirect(url_for(request.args.get('next') or 'account.user_list'))

    id = request.values.get('id')
    user_info = User.query.filter_by(id=id).first()
    return layout('/account/edituser.html', user_info=user_info)

@account.route('/deluser')
@login_required
def user_del():
    try:
        id = request.values.get('id')
        user = User.query.filter(User.id == id).first()
        db.session.delete(user)
        db.session.commit()
        flash('Deleted', 'success')
    except Exception as e:
        print(e)
        flash('Fail', 'error')

    return redirect(url_for(request.args.get('next') or 'account.user_list'))

@account.route('/bouns_update')
@login_required
def bouns_update():

    def get_all_cycles(employee_id):
        # Use filter to apply conditions and all() to get a list of results
        cycles_list = db.session.query(Record.cycle).filter(Record.user_id == employee_id).all()
        return [cycle[0] for cycle in cycles_list]

    def get_all_max_capacities(records):
        max_capacities_list = []
        for record in records:
            max_capacities_list.append(db.session.query(Product.max_capacity).filter(Product.id == record.part_id).all())

        return[max_capacity[0][0] for max_capacity in max_capacities_list]

    def get_all_machine_down_time(employee_id):
        # Use filter to apply conditions and all() to get a list of results
        machine_down_time_list = db.session.query(Record.machine_downtime).filter(Record.user_id == employee_id).all()
        return [machine_down_time[0] for machine_down_time in machine_down_time_list]

    try:
        id = request.values.get('id')
        user = User.query.filter(User.id == id).first()
        print(user.username)
        records = db.session.query(Record).filter(Record.user_id == id).all()
        print(records)

        cycles = get_all_cycles(id)
        print(cycles)
        max_capacities = get_all_max_capacities(records)
        print(max_capacities)

        # max_capacities = []
        # for record in records:
        #     max_capacities.append(db.session.query(Product.max_capacity).order_by(record.part_id).all())
        # print('max_capacities = ' + max_capacities)
        machine_down_time = get_all_machine_down_time(id)
        print(machine_down_time)
        # # machine_down_time = db.session.query(Record.machine_downtime).order_by(Record.user_id == id).all()
        work_days = db.session.query(Record).filter(Record.user_id == id).count()
        print(work_days)
        sick_days = user.sick_days
        print(sick_days)
        quality_complaints = user.quality_complaints
        print(quality_complaints)
        total_cleanliness_amount = user.total_cleanliness_amount
        print(total_cleanliness_amount)
        #
        # today = datetime.date.today()
        months = 12
        print(months)
        bonus_info = calculate_monthly_bonus(cycles, max_capacities, machine_down_time, work_days, sick_days, total_cleanliness_amount, quality_complaints, months)
        print(bonus_info['total_bonus'])
        user.bonus = bonus_info['total_bonus']
        db.session.commit()
        flash('success', 'success')
    except Exception as e:
        print(e)
        flash('Fail', 'error')



    return redirect(url_for(request.args.get('next') or 'account.user_list'))

@account.route('/update_user',methods=(["GET","POST"]))
@login_required
def user_update():
    if request.method == 'POST':
        try:
            form = request.form
            user_bounus_info = User.query.filter(User.id == form['id']).first()
            user_bounus_info.sick_days = form['sick_days']
            user_bounus_info.quality_complaints = form['quality_complaints']
            user_bounus_info.total_cleanliness_amount = form['total_cleanliness_amount']
            db.session.commit()
            flash('weekly updated', 'success')
        except Exception as e:
            print(e)
            print('.........................................................................................')
            flash('weekly update fail', 'error')

        return redirect(url_for(request.args.get('next') or 'account.user_list'))
    id = request.values.get('id')
    user_bounus_info = User.query.filter_by(id=id).first()
    return layout('/account/update_user.html', user_bounus_info=user_bounus_info)

@account.route('/update_record',methods=(["GET","POST"]))
@login_required
def record_upload():
    if request.method == 'POST':
        try:
            form = request.form
            records = Record(user_id=current_user.id, machine_id=form['machine_id'], part_id=form['part_id'], cycle=form['cycle'],
                        machine_downtime=form['machine_downtime'])
            print(records.user_id)
            print('..........................................')
            db.session.add(records)
            db.session.commit()
            return redirect(url_for(request.args.get('next') or 'account.user_list'))
        except Exception as e:

            print(e)
            abort(403)
    return render_template('/account/record_upload.html')