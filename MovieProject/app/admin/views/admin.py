from flask import render_template, flash, redirect, url_for, request

from app import db, app
from app.admin import admin
from app.admin.forms.admin import AddForm, EditForm
from app.models import Admin
from werkzeug.security import generate_password_hash
from app.admin.utils import write_adminOplog, is_admin_login, permission_control


@admin.route('/admin/add/',methods=['POST','GET'])
@is_admin_login
def admin_add():
    form =AddForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        is_super=form.is_super.data
        role_id=form.role_id.data
        print(is_super,'----------')
        if Admin.query.filter_by(name=username).count():
            flash("管理员%s已经存在"%(username),category='err')
            return redirect(url_for('admin.admin_add'))
        admin=Admin(name=username,password=generate_password_hash(password),is_super=is_super,role_id=role_id)
        db.session.add(admin)
        db.session.commit()
        flash("管理员%s创建成功" %(username))
        write_adminOplog("管理员%s创建成功" %(username))
        return redirect(url_for('admin.admin_list'))
    return render_template('admin/admin/add.html',form=form)

@admin.route('/admin/list/')
@admin.route('/admin/list/<int:page>/')
@is_admin_login
@permission_control
def admin_list(page=1):
    adminsPageObj=Admin.query.order_by(Admin.addtime.desc()).paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('admin/admin/list.html',adminsPageObj=adminsPageObj)

@admin.route('/admin/edit/<int:id>/',methods=['POST','GET'])
@is_admin_login
@permission_control
def admin_edit(id):
    form=EditForm()
    admin=Admin.query.get_or_404(id)
    old_name=admin.name
    old_is_super=admin.is_super
    old_role_id=admin.role_id
    form=EditForm(username=admin.name,is_super=admin.is_super,role_id=admin.role_id)
    flash_str=''
    if form.validate_on_submit():
        name=request.form['username']
        is_super=int(request.form['is_super'])
        role_id=int(request.form['role_id'])
        print(type(is_super))
        if name==admin.name and is_super==admin.is_super and role_id==admin.role_id:
            flash_str="未做如何修改"
            flash(flash_str)
            return redirect(url_for('admin.admin_edit',id=id))
        if request.form['username']!=admin.name:
            if Admin.query.filter_by(name=name).first():
                flash_str="会员名称已经存在"
                flash(flash_str)
                return redirect(url_for('admin.admin_edit', id=id))
            admin.name=request.form['username']
            flash_str+="管理员 名称%s修改为%s  " %(old_name,admin.name)
        if is_super!=old_is_super:
            admin.is_super=is_super
            if admin.is_super:
                flash_str+="普通管理员修改为超级管理员  "
            else:
                flash_str+="超级管理员修改为普通管理员  "
        if role_id!=old_role_id:
            admin.role_id=role_id
            flash_str+="管理员角色修改成功"
        db.session.add(admin)
        db.session.commit()
        flash(flash_str)
        write_adminOplog(flash_str)
        return redirect(url_for('admin.admin_list'))

    return render_template('admin/admin/edit.html',form=form)
@admin.route('/admin/del/<int:id>/')
@is_admin_login
@permission_control
def admin_del(id):
    admin=Admin.query.get_or_404(id)
    db.session.delete(admin)
    db.session.commit()
    flash("管理员%s删除成功" %(admin.name))
    write_adminOplog("管理员%s删除成功" %(admin.name))
    return redirect(url_for('admin.admin_list'))
