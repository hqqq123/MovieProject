from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import StringField,FileField,DateTimeField,TextAreaField,SubmitField,SelectField,SelectMultipleField
from wtforms.validators import DataRequired

from app.models import Tag


class BaseForm(FlaskForm):
    name=StringField(
        label="电影名称",
        validators=[DataRequired()]
    )
    star=SelectField(
        label="星级",
        coerce=int,
        choices=[(1,"一星"),(2,"二星"),(3,"三星"),(4,"四星"),(5,"五星")]
    )
    area=StringField(
        label="地区"
    )
    length=StringField(
        label="片长",
    )
    release_time=DateTimeField(
        label="上映时间",

    )
    url=FileField(
        label="电影文件",
        validators=[
            FileAllowed(['avi','mp4'],message="只支持.avi和.mp4格式")
        ]
    )
    logo = FileField(
        label="电影封面",
        validators=[
            FileAllowed(['jpg', 'png'], message="只支持.jpg和.png文件")
        ]

    )
    info=TextAreaField(
        label="电影简介",
    )
    tag_id=SelectField(
        label="类型",
        coerce=int,
    )
    def __init__(self, *args, **kwargs):
        super(BaseForm, self).__init__(*args, **kwargs)
        self.tag_id.choices = [(tag.id, tag.name) for tag in Tag.query.all()]
class AddForm(BaseForm):
    submit=SubmitField(label="添加影片")

class EditForm(BaseForm):
    submit=SubmitField(label="编辑影片")