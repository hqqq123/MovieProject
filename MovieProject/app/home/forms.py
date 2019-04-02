from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,SubmitField,PasswordField,SelectField,FileField,TextAreaField
from wtforms.validators import DataRequired, Length,EqualTo,Email


class BaseForm(FlaskForm):
    username=StringField(
        label="用户名",
        validators=[DataRequired()]
    )
    password = PasswordField(
        label="密码",
        validators=[
            DataRequired(),
            Length(6,18,message="长度必须在6-18位之间"),
        ]
    )
class LoginForm(BaseForm):
    submit=SubmitField(label="登录")

class RegisteForm(BaseForm):
    repasssword=PasswordField(
        label="确认密码",
        validators=[
            DataRequired(),
            EqualTo('password',message="密码不一致")
        ]
    )
    email=StringField(
        label="邮箱",
        validators=[
            DataRequired(),
            Email(message="邮箱格式不正确"),

        ]
    )
    phone=StringField(
        label="电话号码",
        validators=[
            Length(11,11,message="号码格式不正确")
        ]
    )
    gender=SelectField(
        label="性别",
        validators=[
            DataRequired(message="请选择性别")

        ],
        coerce=bool,
        choices=[(True,"男"),(False,"女")]

    )
    face=FileField(
        label="头像",
        validators=[
            FileAllowed(['jpg','png'],message="只支持.jpg和.png文件")

        ]
    )
    info=TextAreaField(label="个人简介")
    submit=SubmitField(label="注册")


class EditUserForm(FlaskForm):
    username=StringField(
        label="用户名",
        validators=[DataRequired()]
    )

    email=StringField(
        label="邮箱",
        validators=[
            DataRequired(),
            Email(message="邮箱格式不正确"),

        ]
    )
    phone=StringField(
        label="电话号码",
        validators=[
            Length(11,11,message="号码格式不正确")
        ]
    )
    gender=SelectField(
        label="性别",
        validators=[
            DataRequired(message="请选择性别")

        ],
        coerce=bool,
        choices=[(True,"男"),(False,"女")]

    )
    face=FileField(
        label="头像",
        validators=[
            FileAllowed(['jpg','png'],message="只支持.jpg和.png文件")

        ]
    )
    info=TextAreaField(label="个人简介")
    submit=SubmitField(label="更新信息")


class PwdForm(FlaskForm):
    old_pwd=PasswordField(
        label="旧密码",
        validators=[DataRequired()],
        render_kw={'placeholder':'请输入旧密码'}
    )
    new_pwd = PasswordField(
        label="新密码密码",
        validators=[DataRequired()],
        render_kw={'placeholder': '请输入新密码'}
    )
    repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired(),
            EqualTo('new_pwd',message="密码不一致")
        ],
        render_kw={'placeholder': '请输入新密码'}
    )
    submit=SubmitField(label="修改密码")

class CommentAddForm(FlaskForm):
    name=StringField(
        label="电影名称",
        validators=[DataRequired()]
    )
    comment=TextAreaField(
        label="评论",
        validators=[DataRequired()]
    )
    submit=SubmitField(label="评论")
