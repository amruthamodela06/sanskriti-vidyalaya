from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class BlogForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    excerpt = TextAreaField('Excerpt (Short Summary)', validators=[Optional(), Length(max=500)])
    category = SelectField('Category', choices=[
        ('news', 'News'),
        ('blog', 'Blog'),
        ('notice', 'Notice')
    ])
    image = FileField('Featured Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    is_featured = BooleanField('Featured Post')
    is_published = BooleanField('Published')
    submit = SubmitField('Save')
