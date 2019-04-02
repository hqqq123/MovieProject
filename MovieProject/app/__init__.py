import pymysql
from flask import Flask
from flask_script import Manager
app=Flask(__name__)
manager=Manager(app)

from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()
app.config.from_pyfile('../config.py')

db=SQLAlchemy(app)
from flask_bootstrap import Bootstrap
botstrap=Bootstrap(app)

from flask_moment import Moment
moment=Moment(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix='/admin')
