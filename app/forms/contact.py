from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, Length, Optional

class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    subject = StringField('Subject', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class MessageReplyForm(FlaskForm):
    admin_notes = TextAreaField('Admin Notes')
    is_read = BooleanField('Mark as Read')
    is_replied = BooleanField('Mark as Replied')
    submit = SubmitField('Update')

class AdmissionInquiryForm(FlaskForm):
    student_name = StringField('Student Name', validators=[DataRequired(), Length(max=100)])
    parent_name = StringField('Parent/Guardian Name', validators=[DataRequired(), Length(max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email(), Length(max=120)])
    phone = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    class_applying = StringField('Class Applying For', validators=[DataRequired(), Length(max=50)])
    previous_school = StringField('Previous School (if any)', validators=[Optional(), Length(max=200)])
    message = TextAreaField('Additional Information', validators=[Optional()])
    submit = SubmitField('Submit Inquiry')
