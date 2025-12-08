from datetime import datetime
from app.extensions import db

class AdmissionInquiry(db.Model):
    __tablename__ = 'admission_inquiries'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(100), nullable=False)
    parent_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    class_applying = db.Column(db.String(50), nullable=False)
    previous_school = db.Column(db.String(200))
    message = db.Column(db.Text)
    is_read = db.Column(db.Boolean, default=False)
    is_contacted = db.Column(db.Boolean, default=False)
    admin_notes = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')  # pending, contacted, admitted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AdmissionInquiry {self.student_name}>'
