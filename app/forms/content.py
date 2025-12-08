from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, SelectField, BooleanField, IntegerField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class StaticContentForm(FlaskForm):
    title = StringField('Section Title', validators=[Optional(), Length(max=200)])
    content = TextAreaField('Content')
    image = FileField('Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    order = IntegerField('Display Order', default=0)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    content = TextAreaField('Content')
    link_url = StringField('Link URL', validators=[Optional(), Length(max=500)])
    link_text = StringField('Link Text', validators=[Optional(), Length(max=100)])
    announcement_type = SelectField('Type', choices=[
        ('info', 'Information'),
        ('urgent', 'Urgent'),
        ('success', 'Success')
    ])
    start_date = DateField('Start Date', validators=[Optional()])
    end_date = DateField('End Date', validators=[Optional()])
    priority = IntegerField('Priority (higher = more important)', default=0)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')

class TimetableForm(FlaskForm):
    class_name = StringField('Class', validators=[DataRequired(), Length(max=50)],
                            render_kw={'placeholder': 'e.g., Class 10'})
    section = StringField('Section', validators=[Optional(), Length(max=10)],
                         render_kw={'placeholder': 'e.g., A'})
    file = FileField('Timetable File (PDF or Image)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp', 'pdf'], 'Images or PDF only!')
    ])
    academic_year = StringField('Academic Year', validators=[DataRequired(), Length(max=20)],
                               render_kw={'placeholder': 'e.g., 2024-2025'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
