from flask_wtf import FlaskForm

from wtforms import StringField,SubmitField
from wtforms.validators import DataRequired
class BaseForm(FlaskForm):
    name=StringField(
        label="权限名称",
        validators=[DataRequired()]
    )
    url=StringField(
        label="访问链接",
        validators=[DataRequired()]
    )
class AddAuthForm(BaseForm):
    submit=SubmitField(label="添加权限")
class EditAuthForm(BaseForm):
    submit=SubmitField(label="更新权限")