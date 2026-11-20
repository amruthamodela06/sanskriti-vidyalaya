from datetime import datetime
from app.extensions import db


class DownloadResource(db.Model):
    __tablename__ = 'download_resources'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50), default='circular')  # circular, syllabus, form, calendar, newsletter
    file_url = db.Column(db.String(500), nullable=False)
    academic_year = db.Column(db.String(20))
    is_active = db.Column(db.Boolean, default=True)
    download_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<DownloadResource {self.title}>'
