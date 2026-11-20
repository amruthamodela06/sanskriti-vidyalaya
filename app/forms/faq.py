from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Optional


class FAQForm(FlaskForm):
    question = StringField('Question', validators=[DataRequired(), Length(max=500)])
    answer = TextAreaField('Answer', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('general', 'General'),
        ('admissions', 'Admissions'),
        ('academics', 'Academics'),
        ('fees', 'Fees & Scholarships'),
        ('transport', 'Transport & Facilities')
    ])
    order = IntegerField('Display Order', validators=[Optional()], default=0)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
