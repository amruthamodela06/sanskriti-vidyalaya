from datetime import datetime
from app.extensions import db

class Timetable(db.Model):
    __tablename__ = 'timetables'

    id = db.Column(db.Integer, primary_key=True)
    class_name = db.Column(db.String(50), nullable=False)  # e.g., "Class 10"
    section = db.Column(db.String(10))  # e.g., "A", "B"
    file_url = db.Column(db.String(500))  # PDF/Image upload
    file_type = db.Column(db.String(20))  # pdf, image
    academic_year = db.Column(db.String(20), nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Timetable {self.class_name} {self.section}>'
