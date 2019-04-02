from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import DataRequired

class BaseForm(FlaskForm):
    username=StringField(
        label="用户名",
        validators=[DataRequired()]
    )
    password=PasswordField(
        label="密码",
        validators=[DataRequired()]
    )
class LoginForm(BaseForm):
    submit=SubmitField(label="登录")

