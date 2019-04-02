from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,FileField,SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired

class BaseForm(FlaskForm):
    name=StringField(
        label="电影名称",
        validators=[DataRequired()]
    )
    logo=FileField(
        label="封面图片",
        validators=[
            FileAllowed(['jpg','png'],message="只支持.jpg和.png文件")
        ]

    )
class AddForm(BaseForm):
    submit=SubmitField(label="添加预告")
class EditForm(BaseForm):
    submit=SubmitField(label="编辑预告")