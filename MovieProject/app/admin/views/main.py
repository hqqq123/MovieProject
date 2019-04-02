from flask import render_template, session, flash, request, url_for, redirect

from app import db
from app.admin import admin
from app.admin.forms.main import LoginForm
from app.admin.utils import is_admin_login
from app.models import Admin, Adminlog


@admin.route('/')
@is_admin_login
def index():
    return redirect(url_for('admin.movie_list'))
@admin.route('/login/',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        admin=Admin.query.filter_by(name=username).first()
        if admin and admin.password_verify(password):
            session['admin_id']=admin.id
            session['admin']=admin.name
            flash('管理员%s登录成功' % (username))
            remote_ip=request.remote_addr
            adminlog=Adminlog(ip=remote_ip,area='陕西 西安 China',admin_id=admin.id)
            db.session.add(adminlog)
            db.session.commit()
            return redirect(url_for('admin.index'))
        else:
            flash("管理员登录失败")
            return redirect(url_for('admin.login'))
    return render_template('admin/login.html',form=form)

@admin.route('/pwd/')
@is_admin_login
def pwd():
    session.pop('admin_id',None)
    session.pop('admin',None)
    flash("退出成功")
    return redirect(url_for('admin.login'))

@admin.route('/pwd/')
@is_admin_login
def logout():
    return 'pwd'







@admin.route('/pwd/')
def collect_list():
    return 'pwd'
@admin.route('/pwd/')
def logs_operate_log():
    return 'pwd'
@admin.route('/pwd/')
def logs_admin_log():
    return 'pwd'
@admin.route('/pwd/')
def logs_user_log():
    return 'pwd'




