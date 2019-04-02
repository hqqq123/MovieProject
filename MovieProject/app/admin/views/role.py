from flask import render_template, session, flash, request, url_for, redirect

from app import db, app
from app.admin import admin
from app.admin.forms.role import AddForm,EditForm
from app.models import Role, Admin
from app.admin.utils import write_adminOplog
@admin.route('/role/add/',methods=['GET','POST'])
def role_add():
    form=AddForm()
    if form.validate_on_submit():
        name=form.name.data
        if Role.query.filter_by(name=name).count():
            flash("角色%s已经添加")
            return redirect(url_for('admin.role_add'))
        auths=form.auths.data

        # auths=",".join(list(map(str,auths)))
        auths=",".join(auths)
        print(auths)
        role=Role(name=name,auths=auths)
        db.session.add(role)
        db.session.commit()
        flash("角色%s添加成功" %(name))
        write_adminOplog("添加角色%s成功" %(name))
        return redirect(url_for('admin.role_list'))
    return render_template('admin/role/add.html',form=form)

@admin.route('/role/list/')
@admin.route('/role/list/<int:page>/')
def role_list(page=1):

    rolesPageObj=Role.query.order_by(Role.addtime.desc()).paginate(page,per_page=app.config['PER_PAGE'])

    return render_template('admin/role/list.html',rolesPageObj=rolesPageObj)
@admin.route('/role/edit/')
@admin.route('/role/edit/<int:id>/',methods=['GET','POST'])
def role_edit(id):
    form=EditForm()
    role=Role.query.get_or_404(id)
    form.name.data=role.name
    form.old_auths.data=role.auths
    if form.validate_on_submit():
        data=form.data
        if role.name!=data['name'] and Role.query.filter_by(name=data['name']).count():
            flash("角色%s已经存在" %(data['name']))
            return redirect(url_for('admin.role_edit',id=id))
        role.name=data['name']
        role.auths=",".join(data['auths'])
        
        db.session.add(role)
        db.session.commit()
        flash("角色%s修改成功" %(role.name))
        write_adminOplog("角色%s修改成功" %(role.name))
        return redirect(url_for('admin.role_list'))
    return render_template('admin/role/edit.html',form=form)

@admin.route('/role/del/<int:id>/')
def role_del(id=None):
    if id:
        role=Role.query.get_or_404(id)
        db.session.delete(role)
        db.session.commit()
        flash("删除角色%s成功" %(role.name))
        write_adminOplog("删除角色%s成功" %(role.name))
        return redirect(url_for('admin.role_list'))


