from datetime import datetime
from app.extensions import db


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    author_name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), default='Parent')  # Parent, Student, Alumni
    quote = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, default=5)
    is_featured = db.Column(db.Boolean, default=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Testimonial {self.author_name}>'
