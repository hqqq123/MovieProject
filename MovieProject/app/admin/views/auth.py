from app import db, app
from app.admin import admin
from app.admin.forms.auth import AddAuthForm, EditAuthForm
from flask import render_template, flash, redirect, url_for, session, request

from app.admin.utils import write_adminOplog, is_admin_login
from app.models import Auth, Admin, Role


@admin.route('/auth/add/',methods=['GET','POST'])
@is_admin_login
def auth_add():
    form=AddAuthForm()
    if form.validate_on_submit():
        name=form.name.data
        if Auth.query.filter_by(name=name).count():
            flash("权限%s已经存在" %(name))
            return redirect(url_for('admin.auth_add'))
        url=form.url.data
        auth=Auth(name=name,url=url)
        db.session.add(auth)
        db.session.commit()
        flash("权限%s添加成功" %(name))
        write_adminOplog("添加权限%s" %(name))
    return render_template('admin/auth/add.html',form=form)

@admin.route('/auth/list/')
@admin.route('/auth/list/<int:page>/')
@is_admin_login
def auth_list(page=1):
    # admin=Admin.query.filter_by(name=session.get('admin')).first()
    # if not admin.is_super:
    #     authsPageObj=Auth.query.filter_by(role_id=admin.role.id).paginate(page,per_page=app.config['PER_PAGE'])
    # else:
    authsPageObj=Auth.query.order_by(Auth.addtime.desc()).paginate(page,per_page=app.config['PER_PAGE'])
    return render_template('admin/auth/list.html',authsPageObj=authsPageObj)

@admin.route('/auth/edit/')
@admin.route('/auth/edit/<int:id>/',methods=['GET','POST'])
@is_admin_login
def auth_edit(id):
    print(request.url_rule,'=============')
    # form = EditAuthForm()
    # auth=Auth.query.filter_by(id=id).first()
    auth=Auth.query.get_or_404(id)
    # form.name.data=auth.name
    # form.url.data=auth.url
    form=EditAuthForm(name=auth.name,url=auth.url)
    if form.validate_on_submit():
        name = form.name.data
        if name!=auth.name and Auth.query.filter_by(name=name).count():
            flash("权限%s已经存在" % (name))
            return redirect(url_for('admin.auth_edit',id=id))
        url=form.url.data
        auth.name=name
        auth.url=url
        db.session.add(auth)
        db.session.commit()
        flash("权限%s修改成功" % (name))
        write_adminOplog("修改权限%s" %auth.name)
        return redirect(url_for('admin.auth_list'))
    return render_template('admin/auth/add.html', form=form)
@admin.route('/auth/del/')
@admin.route('/auth/del/<int:id>',methods=['GET','POST'])
@is_admin_login
def auth_del(id=None):
    if id:
        auth=Auth.query.get_or_404(id)
        Role.query.filter_by()
        db.session.delete(auth)
        db.session.commit()
        flash("权限%s删除成功"%(auth.name),category='ok')
        write_adminOplog("删除权限%s",auth.name)
        return redirect(url_for('admin.auth_list'))