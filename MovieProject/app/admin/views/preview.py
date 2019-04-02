import os

from flask import render_template, session, flash, request, url_for, redirect

from app import db, app
from app.admin import admin
from app.admin.forms.preview import AddForm,EditForm
from app.home import change_filename
from app.models import Preview
from app.admin.utils import write_adminOplog

@admin.route('/preview/add',methods=['POST','GET'])
def preview_add():
    form=AddForm()

    if form.validate_on_submit():
        data=form.data
        if Preview.query.filter_by(name=data['name']).count():
            flash("预告%s已经存在" %(data['name']))
            return redirect(url_for('admin.preview_add'))
        logofile=data['logo']
        logo_save_path=app.config['PREVIEW_LOGO_DIR']
        if not os.path.exists(logo_save_path):
            os.makedirs(logo_save_path)
        logo=change_filename(logofile.filename)
        logofile.save(os.path.join(logo_save_path,logo))
        preview=Preview(name=data['name'],logo=logo)
        db.session.add(preview)
        db.session.commit()
        flash("添加预告%s成功" %(data['name']))
        return redirect(url_for('admin.preview_list'))
    return render_template('admin/preview/add.html',form=form)
@admin.route('/preview/edit/<int:id>/',methods=['POST','GET'])
def preview_edit(id=None):
    form=EditForm()
    preview=Preview.query.filter_by(id=id).first()
    old_name=preview.name
    form.name.data=old_name
    flash_str=''
    if form.validate_on_submit():
        name=request.form['name']
        logofile=form.logo.data
        print(name,old_name)
        if name==old_name and not logofile:
            flash_str="未做任何修改"
            flash(flash_str)
            return redirect(url_for('admin.preview_edit', id=id))
        if name!=old_name:
            if Preview.query.filter_by(name=name).first():
                flash("预告%s已经存在" %(name))
                return redirect(url_for('admin.preview_edit',id=id))
            print('----------------')
            preview.name=name
            flash_str="预告名称%s修改为%s " %(old_name,name)
        if logofile:
            logo_save_path = app.config['PREVIEW_LOGO_DIR']
            if not os.path.exists(logo_save_path):
                os.makedirs(logo_save_path)
            if os.path.exists(os.path.join(logo_save_path,preview.logo)):
                os.remove(os.path.join(logo_save_path,preview.logo))
            logo=change_filename(logofile.filename)
            logofile.save(os.path.join(logo_save_path,logo))
            preview.logo=logo
            flash_str+="封面修改成功"
        db.session.add(preview)
        db.session.commit()
        flash(flash_str)
        write_adminOplog(flash_str)
        return redirect(url_for('admin.preview_list'))
    return render_template('admin/preview/edit.html',form=form)
@admin.route('/preview/list')
@admin.route('/preview/list/<int:page>/')
def preview_list(page=1):
    previewsPageObj=Preview.query.paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('admin/preview/list.html',previewsPageObj=previewsPageObj)
@admin.route('/preview/del/<int:id>/')
def preview_del(id=None):
    if id:
        preview=Preview.query.get_or_404(id)
        db.session.delete(preview)
        db.session.commit()
        flash("删除预告%s成功" %(preview.name))
        write_adminOplog("删除预告%s成功" %(preview.name))
        return redirect(url_for('admin.preview_list'))
