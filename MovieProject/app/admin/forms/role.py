from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired

from app.models import Auth


class BaseForm(FlaskForm):
    name=StringField(
        label="角色名称",
        validators=[DataRequired()]
    )

class AddForm(BaseForm):
    auths = SelectMultipleField(
        label="权限",
        coerce=str,
    )

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.auths.choices = [(auth.name, auth.name) for auth in Auth.query.all()]

    submit=SubmitField(label='添加角色')


class EditForm(BaseForm):
    old_auths = StringField(
        label="旧权限",

    )
    auths = SelectMultipleField(
        label="新权限",
        coerce=str,
    )

    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.auths.choices = [(auth.name, auth.name) for auth in Auth.query.all()]
    submit = SubmitField(label='更新角色')