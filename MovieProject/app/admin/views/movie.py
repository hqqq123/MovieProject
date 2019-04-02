import os

from flask import render_template, session, flash, request, url_for, redirect

from app import db, app
from app.admin import admin
from app.admin.forms.movie import AddForm,EditForm
from app.home import change_filename
from app.models import Preview, Movie
from app.admin.utils import write_adminOplog, is_admin_login, permission_control


@admin.route('/movie/add/',methods=['GET','POST'])
def movie_add():
    form=AddForm()
    if form.validate_on_submit():
        name=form.name.data
        if Movie.query.filter_by(name=name).count():
            flash("电影%s已经存在"%(name))
            return redirect(url_for('admin.movie_add'))
        urlfile=form.url.data
        urlname=None
        logofile=form.logo.data
        logoname=None
        if urlfile:
            url_save_path=app.config['MOVIE_DIR']
            if not os.path.exists(url_save_path):
                os.makedirs(url_save_path)
            urlname=urlfile.filename
            urlfile.save(os.path.join(url_save_path,urlfile.filename))
        if logofile:
            logo_save_path = app.config['MOVIE_LOGO_DIR']
            if not os.path.exists(logo_save_path):
                os.makedirs(logo_save_path)
                logoname=logofile.filename
            logofile.save(os.path.join(logo_save_path, logofile.filename))
        area=form.area.data
        length=form.length.data
        release_time=form.release_time.data
        print(release_time)
        info=form.info.data
        tag_id=form.tag_id.data
        movie=Movie(name=name,area=area,length=length,release_time=release_time,url=urlname,logo=logoname,
                    info=info,tag_id=tag_id)
        db.session.add(movie)
        db.session.commit()
        flash("影片%s添加成功"%(name))
        write_adminOplog("影片%s添加成功"%(name))
        return redirect(url_for('admin.movie_add'))
    return render_template('admin/movie/add.html',form=form)

@admin.route('/movie/list/')
@admin.route('/movie/list/<int:page>/')
@is_admin_login
@permission_control
def movie_list(page=1):
    moviesPageObj=Movie.query.paginate(page=page,per_page=app.config['PER_PAGE'])
    return render_template('admin/movie/list.html',moviesPageObj=moviesPageObj,app=app)

@admin.route('/movie/edit/<int:id>/',methods=['GET','POST'])
@permission_control
def movie_edit(id):
    form = EditForm()
    movie=Movie.query.get_or_404(id)
    form.name.data=movie.name
    # form.star.data=movie.star
    form.area.data=movie.area
    form.length.data=movie.length
    form.release_time.data=movie.release_time
    form.info.data=movie.info
    form.tag_id.data=movie.tag_id
    if form.validate_on_submit():
        name = request.form['name']
        print('-------------')
        if name!=movie.name:
            if Movie.query.filter_by(name=name).count():
                flash("电影%s已经存在" % (name))
                return redirect(url_for('admin.movie_edit'))
            movie.name=name
        print('==============')
        urlfile = form.url.data
        urlname = None
        logofile = form.logo.data
        logoname = None
        if urlfile:
            url_save_path = app.config['MOVIE_DIR']
            if not os.path.exists(url_save_path):
                os.makedirs(url_save_path)
            urlname = urlfile.filename
            urlfile.save(os.path.join(url_save_path, urlfile.filename))
            movie.url=urlname
        if logofile:
            logo_save_path = app.config['MOVIE_LOGO_DIR']
            if not os.path.exists(logo_save_path):
                os.makedirs(logo_save_path)
                logoname = logofile.filename
            logofile.save(os.path.join(logo_save_path, logofile.filename))
            movie.logo=logoname
        print('==============')

        movie.area = request.form['area']
        movie.length = request.form['length']
        movie.release_time = request.form['release_time']
        movie.star=request.form['star']
        movie.info = request.form['info']
        movie.tag_id = request.form['tag_id']
        print('==============')

        db.session.add(movie)
        db.session.commit()
        flash("影片%s修改成功" % (name))
        write_adminOplog("影片%s修改成功" % (name))
        return redirect(url_for('admin.movie_list'))
    return render_template('admin/movie/edit.html', form=form)

@admin.route('/movie/del/<int:id>/')
def movie_del(id):
    movie=Movie.query.get_or_404(id)
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影%s成功"%(movie.name))
    write_adminOplog("删除电影%s成功"%(movie.name))
    return redirect(url_for('admin.movie_list'))