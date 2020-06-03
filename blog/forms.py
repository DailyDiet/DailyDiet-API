from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    class Meta:
        csrf = False

    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    categories = TextField(validators=[DataRequired()])


class CategoryForm(FlaskForm):
    class Meta:
        csrf = False

    name = TextField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    description = TextAreaField()
