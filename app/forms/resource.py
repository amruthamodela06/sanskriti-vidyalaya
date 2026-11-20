from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SelectField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class DownloadResourceForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[Optional()])
    category = SelectField('Category', choices=[
        ('circular', 'Circular / Notice'),
        ('syllabus', 'Syllabus'),
        ('form', 'Application Form'),
        ('calendar', 'Academic Calendar'),
        ('newsletter', 'Newsletter')
    ])
    file = FileField('Document File (PDF, DOC, DOCX, or Image)', validators=[
        FileAllowed(['pdf', 'doc', 'docx', 'jpg', 'jpeg', 'png'], 'Documents or images only!')
    ])
    academic_year = StringField('Academic Year', validators=[Optional(), Length(max=20)],
                                render_kw={'placeholder': 'e.g., 2025-2026'})
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
