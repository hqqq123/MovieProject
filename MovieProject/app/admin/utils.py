from functools import wraps

from flask import request, session, flash, redirect, url_for, abort

from app import db
from app.models import AdminOplog, Admin, Auth


def write_adminOplog(content):
    adminOplog=AdminOplog(ip=request.remote_addr,area="陕西 西安 China",content=content,admin_id=session.get('admin_id'))
    db.session.add(adminOplog)
    db.session.commit()

def is_admin_login(fun):
    @wraps(fun)
    def wrapper(*args,**kwargs):
        if session.get('admin',None):
            return fun(*args,**kwargs)
        else:
            flash("管理员必须登录后才能访问")
            return redirect(url_for('admin.login'))
    return wrapper

def permission_control(fun):
    @wraps(fun)
    def wrapper(*args,**kwargs):
        admin=Admin.query.get_or_404(session.get('admin_id'))
        if not admin.is_super:
            admin_auths_str=admin.role.auths
            print(admin_auths_str)
            admin_auths_list=list(map(str,admin_auths_str.split(',')))
            print(admin_auths_list)
            admin_urls=[]
            for auth_name in admin_auths_list:
                admin_urls+=Auth.query.filter_by(name=auth_name).first().url.split(',')

            print('管理员的访问地址',admin_urls)
            print('正在访问的地址',request.url_rule)
            if str(request.url_rule) not in admin_urls:
                # flash("没有权限访问")
                abort(403)
                # return redirect(url_for('admin.index'))

        return fun(*args,**kwargs)
    return wrapper
