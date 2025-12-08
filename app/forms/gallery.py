from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, MultipleFileField
from wtforms import StringField, TextAreaField, DateField, SelectField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class AlbumForm(FlaskForm):
    title = StringField('Album Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    event_date = DateField('Event Date', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('events', 'Events'),
        ('infrastructure', 'Infrastructure'),
        ('activities', 'Activities'),
        ('achievements', 'Achievements'),
        ('sports', 'Sports'),
        ('cultural', 'Cultural')
    ])
    cover_image = FileField('Cover Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    is_published = BooleanField('Published', default=True)
    order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save')

class PhotoUploadForm(FlaskForm):
    photos = MultipleFileField('Upload Photos', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    submit = SubmitField('Upload')

class PhotoEditForm(FlaskForm):
    caption = StringField('Caption', validators=[Optional(), Length(max=500)])
    order = IntegerField('Display Order', default=0)
    submit = SubmitField('Save')
