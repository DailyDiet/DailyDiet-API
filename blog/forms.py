from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField
from wtforms.validators import DataRequired
from blog.models import Post


class PostForm(FlaskForm):
    class Meta:
        csrf = False

    title = TextField(validators=[DataRequired()])
    summary = TextAreaField()
    content = TextAreaField(validators=[DataRequired()])
    slug = TextField(validators=[DataRequired()])
    category = TextField(validators=[DataRequired()])

    def validate(self):
        initial_validation = super(PostForm, self).validate()
        if not initial_validation:
            return False
        slug = Post.query.filter_by(slug=self.slug.data).first()
        title = Post.query.filter_by(title=self.title.data).first()
        if slug:
            self.slug.errors.append("slug has already been taken.")
            return False
        if title:
            self.title.errors.append("title has already been taken.")
            return False
        return True