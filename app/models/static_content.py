from datetime import datetime
from app.extensions import db

class StaticContent(db.Model):
    __tablename__ = 'static_contents'

    id = db.Column(db.Integer, primary_key=True)
    page_key = db.Column(db.String(50), nullable=False)  # about, admissions, contact
    section_key = db.Column(db.String(50), nullable=False)  # history, vision, mission, etc.
    title = db.Column(db.String(200))
    content = db.Column(db.Text)
    image_url = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('page_key', 'section_key', name='unique_page_section'),
    )

    def __repr__(self):
        return f'<StaticContent {self.page_key}/{self.section_key}>'
