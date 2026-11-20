from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange


class TestimonialForm(FlaskForm):
    author_name = StringField('Author Name', validators=[DataRequired(), Length(max=100)])
    role = StringField('Role / Relation', validators=[DataRequired(), Length(max=100)],
                       render_kw={'placeholder': 'e.g., Parent of Class 5 Student, Alumni'})
    quote = TextAreaField('Testimonial Quote', validators=[DataRequired()])
    rating = SelectField('Rating', coerce=int, choices=[
        (5, '5 Stars'),
        (4, '4 Stars'),
        (3, '3 Stars'),
        (2, '2 Stars'),
        (1, '1 Star')
    ], default=5)
    is_featured = BooleanField('Featured on Homepage', default=True)
    is_active = BooleanField('Active', default=True)
    submit = SubmitField('Save')
