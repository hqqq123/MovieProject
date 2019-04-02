import getpass

from flask import Flask
from flask_migrate import MigrateCommand

from app import manager
from app import db
from app.models import User, Admin
from werkzeug.security import generate_password_hash

@manager.command
def initdb():

    db.drop_all()
    db.create_all()
    u=User(name='redhat',password=generate_password_hash('redhat'))
    db.session.add(u)
    db.session.commit()
    print("初始化数据库成功")

@manager.command
def createsuper():
    username=input("请输入管理员名称:")
    if Admin.query.filter_by(name=username).first():
        print("管理员%s已经存在" %(username))
    else:
        password=getpass.getpass("请输入密码：")
        password_hash=generate_password_hash(password)
        admin=Admin(name=username,password=password_hash,is_super=True)
        db.session.add(admin)
        db.session.commit()
        print("管理员%s创建成功" %(username))


manager.add_command('db',MigrateCommand)
if __name__ == '__main__':
    manager.run()
