import os
from app import app, db
from flask import render_template, flash, redirect, url_for, session, request

from app.home import home
from app.home.forms import RegisteForm, LoginForm, EditUserForm, PwdForm, CommentAddForm
from app.home.utils import change_filename
from app.models import User, Userlog, Comment, MovieCollect, Movie
from werkzeug.security import generate_password_hash

@home.route('/')
def index():
    return redirect(url_for('home.movie_list'))
@home.route('/login/',methods=['GET','POST'])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        user=User.query.filter_by(name=username).first()
        if user and user.password_verify(password):
            session['user_id']=user.id
            session['user']=user.name
            flash('用户%s登录成功' % (username))
            remote_ip=request.remote_addr
            userlog=Userlog(ip=remote_ip,area='陕西 西安 China',user_id=user.id)
            db.session.add(userlog)
            db.session.commit()
            return redirect(url_for('home.index'))
        else:
            flash("用户登录失败")
            return redirect(url_for('home.login'))
    return render_template('home/login.html',form=form)
@home.route('/register/',methods=['GET','POST'])
def register():
    form=RegisteForm()
    if form.validate_on_submit():
        username=form.username.data
        password=form.password.data
        email=form.email.data
        phone=form.phone.data
        gender=form.gender.data
        faceFile=form.face.data
        info=form.info.data
        if User.query.filter_by(name=username).first():
            flash("用户名%s已经注册" %(username))
            # print(form.username.validators[0].message)
            return redirect(url_for('home.register'))

        if User.query.filter_by(email=email).first():
            flash("邮箱%s已经注册" %(email))
            # form.email.validators[0].message="该邮箱已经注册"
            return redirect(url_for('home.register'))

        if User.query.filter_by(phone=phone).first():
            flash("手机号%s已经注册" %(phone))
            return redirect(url_for('home.register'))

        password_hash = generate_password_hash(password)
        face_save_path = app.config['USER_FACE_DIR']
        if not os.path.exists(face_save_path):
            os.makedirs(face_save_path)
        face = change_filename(faceFile.filename)
        faceFile.save(os.path.join(face_save_path, face))
        user = User(name=username, password=password_hash, email=email, phone=phone, face=face, gender=gender,
                    info=info)
        db.session.add(user)
        db.session.commit()
        flash('用户%s注册成功' % (username))
        return redirect(url_for('home.login'))
    return render_template('home/register.html',form=form)
@home.route('/logout/',methods=['GET','POST'])
def logout():

    session.pop('user_id',None)
    session.pop('user',None)
    flash("用户退出成功")
    return redirect(url_for('home.login'))

@home.route('/user/',methods=['GET','POST'])
def user():
    form=EditUserForm()
    user=User.query.filter_by(name=session.get('user')).first()
    form.username.data=user.name
    form.email.data=user.email
    form.phone.data=user.phone
    form.gender.data=user.gender
    print(form.gender.data,'==============')
    form.info.data=user.info
    if form.validate_on_submit():
        username = request.form['username']
        email = request.form['email']
        phone = request.form['phone']
        # gender = form.gender.data
        gender=bool(request.form['gender'])
        print(gender,'--------------')
        faceFile = form.face.data
        info = request.form['info']
        if username!=user.name and User.query.filter_by(name=username).first():
            flash("用户名%s已经注册" % (username))
            # print(form.username.validators[0].message)
            return redirect(url_for('home.user'))

        if email!=user.email and User.query.filter_by(email=email).first():
            flash("邮箱%s已经注册" % (email))
            # form.email.validators[0].message="该邮箱已经注册"
            return redirect(url_for('home.user'))

        if phone!=user.phone and User.query.filter_by(phone=phone).first():
            flash("手机号%s已经注册" % (phone))
            return redirect(url_for('home.user'))

        face_save_path = app.config['USER_FACE_DIR']
        if not os.path.exists(face_save_path):
            os.makedirs(face_save_path)
        if faceFile:
            if user.face and os.path.exists(os.path.join(face_save_path, user.face)):
                os.remove(os.path.join(face_save_path, user.face))

            face = change_filename(faceFile.filename)
            faceFile.save(os.path.join(face_save_path, face))
            user.face = face
        user.name = username
        user.phone = phone
        user.email = email
        user.info = info
        user.gender = gender
        db.session.add(user)
        db.session.commit()
        session['user_id'] = user.id
        session['user'] = user.name
        flash('修改信息成功')

        return redirect(url_for('home.index'))



    return render_template('home/user.html',form=form)

@home.route('/pwd/',methods=['GET','POST'])
def pwd():
    form=PwdForm()
    if form.validate_on_submit():
        user=User.query.filter_by(name=session.get('user')).first()
        if user.password_verify(form.old_pwd.data):
            if user.password_verify(form.new_pwd.data):
                flash("旧密码不能和新密码相同")
                return redirect(url_for('home.pwd'))
            user.password=generate_password_hash(form.new_pwd.data)
            db.session.add(user)
            db.session.commit()
            flash("密码修改成功")
            session.pop('user',None)
            session.pop('user_id',None)
            return redirect(url_for('home.login'))
        else:
            flash("密旧码错误")
            return redirect(url_for('home.pwd'))
    return render_template('home/pwd.html',form=form)

@home.route('/comments/')
@home.route('/comments/<int:page>/')
def comments(page=1):
    commentsPageObj=Comment.query.filter_by(user_id=session.get('user_id')).paginate(page,per_page=app.config['PER_PAGE'])

    return render_template('home/comments.html',commentsPageObj=commentsPageObj,app=app)
@home.route('/userlog/')
@home.route('/userlog/<int:page>/')
def userlog(page=1):
    userlogsPageObj=Userlog.query.filter_by(user_id=session.get('user_id')).paginate(page,per_page=app.config['PER_PAGE'])

    return render_template('home/userlog.html',userlogsPageObj=userlogsPageObj)
@home.route('/moviecollect/')
@home.route('/moviecollect/<int:page>/')
def moviecollect(page=1):
    moviecollectsPageObj=MovieCollect.query.filter_by(user_id=session.get('user_id')).paginate(page,per_page=app.config['PER_PAGE'])
    for c in moviecollectsPageObj.items:
        print(c.movie.name,'---------------')
    return render_template('home/moviecollect.html',moviecollectsPageObj=moviecollectsPageObj)


@home.route('/play/<int:id>/',methods=['GET','POST'])
@home.route('/play/<int:id>/<int:page>/',methods=['GET','POST'])
def play(id,page=1):
    movie=Movie.query.get_or_404(id)
    commentsPageObj=Comment.query.filter_by(movie_id=id).paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('home/play.html',movie=movie,commentsPageObj=commentsPageObj,app=app)

@home.route('/movie/list/')
@home.route('/movie/list/<int:page>/')
def movie_list(page=1):
    moviesPageObj=Movie.query.paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('home/list.html',moviesPageObj=moviesPageObj,app=app)
@home.route('/collect/add/<int:id>')
def collect_add(id):
    if MovieCollect.query.filter_by(movie_id=id).first():
        flash("电影%s已经收藏")
        return redirect(url_for('home.movie_list'))
    collect=MovieCollect(movie_id=id,user_id=session.get('user_id'))
    db.session.add(collect)
    db.session.commit()
    flash("电影%s收藏成功")
    return redirect(url_for('home.movie_list'))
@home.route('/collect/del/<int:id>/')
def collect_del(id):
    collect=MovieCollect.query.filter_by(movie_id=id).first()
    db.session.delete(collect)
    db.session.commit()
    # flash("删除电影%s收藏"%(collect.movie.name))
    return redirect(url_for('home.movie_list'))
@home.route('/comment/add/<int:id>/',methods=['POST','GET'])
def comment_add(id):
    form=CommentAddForm()
    form.name.data=Movie.query.filter_by(id=id).first().name
    if form.validate_on_submit():
        content=form.comment.data
        comment=Comment(content=content,movie_id=id,user_id=session.get('user_id'))
        db.session.add(comment)
        db.session.commit()
        flash("评论成功")
        return redirect(url_for('home.movie_list'))
    return render_template('home/comment_add.html',form=form)
@home.route('/comment/list/')
@home.route('/comment/list/<int:page>/')
def comment_list(page=1):
    commentsPageObj=Comment.query.filter_by(user_id=session.get('user_id')).paginate(page=page,per_page=app.config['PER_PAGE'])

    return render_template('home/comment_list.html',commentsPageObj=commentsPageObj,app=app)
@home.route('/comment/del/<int:id>/')
def comment_del(id):
    comment=Comment.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    flash("删除评论成功")
    return redirect(url_for('home.comment_list'))
# @home.route("/log/list/")
# @home.route("/log/list/<int:page>/")
# def log(page=1):
#     userlogPageObj = Userlog.query.paginate(page,
#                                             per_page=app.config['PER_PAGE'])
#     return render_template('admin/logs/user_log.html',
#                            userlogPageObj=userlogPageObj)