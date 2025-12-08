from datetime import datetime
from app.extensions import db

class Holiday(db.Model):
    __tablename__ = 'holidays'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    description = db.Column(db.Text)
    holiday_type = db.Column(db.String(50), default='general')  # national, religious, school, vacation
    academic_year = db.Column(db.String(20))  # e.g., "2024-2025"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Holiday {self.name}>'
