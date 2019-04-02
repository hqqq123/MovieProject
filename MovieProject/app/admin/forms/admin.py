from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SelectField,SubmitField
from wtforms.validators import DataRequired, EqualTo

from app.models import Role


class AddForm(FlaskForm):
    username=StringField(
        label="管理员名称",
        validators=[DataRequired()]
    )
    password = PasswordField(
        label='管理员密码',
        validators=[
            DataRequired()
        ],
    )
    repassword = PasswordField(
        label='确认密码',
        validators=[
            DataRequired(),
            EqualTo('password', message='两次密码不一致')
        ],
    )
    is_super=SelectField(
        label="身份",
        coerce=int,
        choices=[(0,'普通管理员'),(1,'超级管理员')]

    )
    role_id=SelectField(
        label="角色",
        coerce=int,
    )
    def __init__(self,*args,**kwargs):
        super(AddForm,self).__init__(*args,**kwargs)
        self.role_id.choices=[(role.id,role.name) for role in Role.query.all()]

    submit=SubmitField(label='添加管理员')
class EditForm(FlaskForm):
    username = StringField(
        label="管理员名称",
        validators=[DataRequired()]
    )
    is_super = SelectField(
        label="身份",
        coerce=int,
        choices=[(0, '普通管理员'), (1, '超级管理员')]

    )
    role_id = SelectField(
        label="角色",
        coerce=int,
    )

    def __init__(self, *args, **kwargs):
        super(EditForm, self).__init__(*args, **kwargs)
        self.role_id.choices = [(role.id, role.name) for role in Role.query.all()]

    submit = SubmitField(label='更新管理员信息')