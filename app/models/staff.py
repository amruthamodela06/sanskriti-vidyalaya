from datetime import datetime
from app.extensions import db


class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    photo_url = db.Column(db.String(500))
    designation = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100))
    subjects_taught = db.Column(db.Text)
    qualifications = db.Column(db.Text)
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    experience_years = db.Column(db.Integer)
    bio = db.Column(db.Text)
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    joined_date = db.Column(db.Date)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Staff {self.name}>'

    @property
    def subjects_list(self):
        """Return subjects as a list"""
        if self.subjects_taught:
            return [s.strip() for s in self.subjects_taught.split(',')]
        return []
