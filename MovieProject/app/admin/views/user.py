from flask import render_template, flash, redirect, url_for, request

from app import db, app
from app.admin import admin
from app.models import Admin, User
from werkzeug.security import generate_password_hash
from app.admin.utils import write_adminOplog
@admin.route('/user/list/')
@admin.route('/user/list/<int:page>/',methods=['GET','POST'])
def user_list(page=1):
    usersPageObj=User.query.paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('admin/user/list.html',usersPageObj=usersPageObj,app=app)
@admin.route('/user/view/<int:id>/')
def user_view(id):
    user=User.query.get_or_404(id)

    return render_template('admin/user/view.html',user=user,app=app)
@admin.route('/user/del/<int:id>/')
def user_del(id):
    user=User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    flash("删除用户%s成功"%(user.name))
    return redirect(url_for('admin.user_list'))
