from datetime import datetime

from app import db


class Movie(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(50),unique=True,index=True)
    info=db.Column(db.TEXT)
    star=db.Column(db.SmallInteger)
    area=db.Column(db.String(50))
    length=db.Column(db.String(20))
    release_time=db.Column(db.DateTime)
    url=db.Column(db.String(200),unique=True)
    logo=db.Column(db.String(200),unique=True)

    tag_id=db.Column(db.Integer,db.ForeignKey('tag.id'))
    comments=db.relationship('Comment',backref='movie')
    moviecollects=db.relationship('MovieCollect',backref='movie')


class User(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(50),unique=True,index=True)
    password=db.Column(db.String(200))
    email=db.Column(db.String(50),unique=True)
    phone=db.Column(db.String(20),unique=True)
    face=db.Column(db.String(200))
    gender=db.Column(db.Boolean)
    info=db.Column(db.TEXT)

    comments=db.relationship('Comment',backref='user')
    userlogs=db.relationship('Userlog',backref='user')
    moviecollects=db.relationship('MovieCollect',backref='user')



    def password_verify(self,password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password,password)

class Admin(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(50),unique=True,index=True)
    password=db.Column(db.String(200))
    is_super=db.Column(db.Boolean,default=False)

    adminlogs=db.relationship('Adminlog',backref='admin')
    adminOplogs=db.relationship('AdminOplog',backref='admin')
    role_id=db.Column(db.Integer,db.ForeignKey('role.id'))

    def password_verify(self,password):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.password,password)


class Tag(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(50),unique=True,index=True)

    movies=db.relationship('Movie',backref='tag')

class Preview(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(50),unique=True,index=True)
    logo=db.Column(db.String(200),unique=True)

class Comment(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    content=db.Column(db.TEXT)

    movie_id=db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))

class Userlog(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    ip=db.Column(db.String(30))
    area=db.Column(db.String(50))

    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))


class Adminlog(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    ip=db.Column(db.String(30))
    area=db.Column(db.String(50))

    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'))


class AdminOplog(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    ip=db.Column(db.String(30))
    area=db.Column(db.String(50))
    content=db.Column(db.String(50))

    admin_id=db.Column(db.Integer,db.ForeignKey('admin.id'))


class Auth(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(30),unique=True)
    url=db.Column(db.String(50),unique=True)
    # role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

class Role(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    name=db.Column(db.String(30),unique=True)
    # auths=db.relationship('Auth',backref='role')
    auths=db.Column(db.String(100))
    admins=db.relationship('Admin',backref='role')


class MovieCollect(db.Model):
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    addtime=db.Column(db.DateTime,default=datetime.utcnow())
    movie_id=db.Column(db.Integer,db.ForeignKey('movie.id'))
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'))
