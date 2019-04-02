from flask import render_template, session, flash, request, url_for, redirect

from app import db, app
from app.admin import admin
from app.admin.forms.tag import AddForm,EditForm
from app.models import Role, Admin, Tag
from app.admin.utils import write_adminOplog

@admin.route('/tag/add/',methods=['POST','GET'])
def tag_add():
    form=AddForm()
    if form.validate_on_submit():
        name=form.name.data
        if Tag.query.filter_by(name=name).first():
            flash("标签%s已经存在" %(name))
            return redirect(url_for('admin.tag_add'))
        tag=Tag(name=name)
        db.session.add(tag)
        db.session.commit()
        flash("添加标签%s成功" %(name))
        return redirect(url_for('admin.tag_list'))
    return render_template('admin/tag/add.html',form=form)

@admin.route('/tag/list/')
@admin.route('/tag/list/<int:page>/')
def tag_list(page=1):
    tagsPageObj=Tag.query.paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('admin/tag/list.html',tagsPageObj=tagsPageObj)

@admin.route('/tag/del/<int:id>/')
def tag_del(id=None):
    if id:
        tag=Tag.query.get_or_404(id)
        db.session.delete(tag)
        db.session.commit()
        flash("删除标签%s成功"%(tag.name))
        write_adminOplog("删除标签%s"%(tag.name))
        return redirect(url_for('admin.tag_list'))

@admin.route('/tag/edit/<int:id>',methods=['POST','GET'])
def tag_edit(id):
    form=EditForm()
    tag=Tag.query.get_or_404(id)
    old_name=tag.name
    form.name.data=old_name
    if form.validate_on_submit():
        name=request.form['name']
        print(name,old_name)
        if name!=old_name:
            if Tag.query.filter_by(name=name).count():
                flash("标签%s已经存在")
                return redirect(url_for('admin.tag_edit',id=id))
            tag.name=name
            db.session.add(tag)
            db.session.commit()
            flash("修改标签%s为%s" %(old_name,name))
            write_adminOplog("修改标签%s为%s" %(old_name,name))
        return redirect(url_for('admin.tag_list'))

    return render_template('admin/tag/edit.html',form=form)