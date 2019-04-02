from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired

class BaseForm(FlaskForm):
    name=StringField(
        label="标签名称",
        validators=[DataRequired()]
    )

class AddForm(BaseForm):
    submit=SubmitField(label="添加标签")
class EditForm(BaseForm):
    submit=SubmitField(label="编辑标签")
