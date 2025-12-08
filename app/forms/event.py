from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, DateField, TimeField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class EventForm(FlaskForm):
    title = StringField('Event Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    event_date = DateField('Event Date', validators=[DataRequired()])
    event_time = TimeField('Event Time', validators=[Optional()])
    end_date = DateField('End Date (for multi-day events)', validators=[Optional()])
    location = StringField('Location', validators=[Optional(), Length(max=200)])
    event_type = SelectField('Event Type', choices=[
        ('general', 'General'),
        ('academic', 'Academic'),
        ('cultural', 'Cultural'),
        ('sports', 'Sports'),
        ('competition', 'Competition'),
        ('meeting', 'Meeting'),
        ('celebration', 'Celebration')
    ])
    image = FileField('Event Image', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])
    is_featured = BooleanField('Featured Event')
    is_published = BooleanField('Published', default=True)
    submit = SubmitField('Save')

class HolidayForm(FlaskForm):
    name = StringField('Holiday Name', validators=[DataRequired(), Length(max=200)])
    date = DateField('Date', validators=[DataRequired()])
    end_date = DateField('End Date (for holiday ranges)', validators=[Optional()])
    description = TextAreaField('Description')
    holiday_type = SelectField('Holiday Type', choices=[
        ('national', 'National Holiday'),
        ('religious', 'Religious Holiday'),
        ('school', 'School Holiday'),
        ('vacation', 'Vacation')
    ])
    academic_year = StringField('Academic Year', validators=[Optional(), Length(max=20)],
                                render_kw={'placeholder': 'e.g., 2024-2025'})
    submit = SubmitField('Save')
