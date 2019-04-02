from flask import session, render_template

from app import app
from app.admin import admin
from app.models import Adminlog, Userlog, AdminOplog


@admin.route('/adminlog/list/')
@admin.route('/adminlog/list/<int:page>/')
def log_admin_list(page=1):
    adminlogPageObj=Adminlog.query.filter_by(admin_id=session.get('admin_id')).paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('admin/logs/admin_log.html',adminlogPageObj=adminlogPageObj)


@admin.route('/userlog/list/')
@admin.route('/userlog/list/<int:page>/')
def log_user_list(page=1):
    userlogPageObj=Userlog.query.filter_by().paginate(page,per_page=app.config['PER_PAGE'])

    return render_template('admin/logs/user_log.html',userlogsPageObj=userlogPageObj)
@admin.route('/adminOplog/list/')
@admin.route('/adminOplog/list/<int:page>/')
def oplog_admin_list(page=1):
    adminOplogPageObj=AdminOplog.query.filter_by(admin_id=session.get('admin_id')).paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('admin/logs/operate_log.html',adminOplogPageObj=adminOplogPageObj)