from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, IntegerField, DateField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Email, NumberRange


class StaffForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])

    designation = SelectField('Designation', validators=[DataRequired()], choices=[
        ('principal', 'Principal'),
        ('vice_principal', 'Vice Principal'),
        ('teacher', 'Teacher'),
        ('librarian', 'Librarian'),
        ('lab_assistant', 'Lab Assistant'),
        ('admin_staff', 'Administrative Staff'),
        ('counselor', 'Counselor'),
        ('sports_coach', 'Sports Coach'),
        ('other', 'Other')
    ])

    department = SelectField('Department', validators=[Optional()], choices=[
        ('', '-- Select Department --'),
        ('science', 'Science'),
        ('mathematics', 'Mathematics'),
        ('english', 'English'),
        ('hindi', 'Hindi'),
        ('sanskrit', 'Sanskrit'),
        ('social_studies', 'Social Studies'),
        ('arts', 'Arts'),
        ('physical_education', 'Physical Education'),
        ('computer_science', 'Computer Science'),
        ('administration', 'Administration'),
        ('library', 'Library'),
        ('other', 'Other')
    ])

    subjects_taught = StringField('Subjects Taught', validators=[Optional(), Length(max=500)],
                                  render_kw={'placeholder': 'e.g., Physics, Chemistry, Biology'})

    qualifications = TextAreaField('Qualifications', validators=[Optional()],
                                   render_kw={'placeholder': 'e.g., M.Sc. Physics, B.Ed.'})

    email = StringField('Email', validators=[Optional(), Email(), Length(max=200)])

    phone = StringField('Phone', validators=[Optional(), Length(max=20)])

    experience_years = IntegerField('Years of Experience', validators=[Optional(), NumberRange(min=0, max=60)])

    bio = TextAreaField('Bio / About', validators=[Optional()])

    photo = FileField('Photo', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif', 'webp'], 'Images only!')
    ])

    order = IntegerField('Display Order', validators=[Optional()], default=0,
                         render_kw={'placeholder': 'Lower numbers appear first'})

    joined_date = DateField('Joined Date', validators=[Optional()])

    is_active = BooleanField('Active', default=True)

    submit = SubmitField('Save')
