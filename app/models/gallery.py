from datetime import datetime
from app.extensions import db

class GalleryAlbum(db.Model):
    __tablename__ = 'gallery_albums'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(500))
    event_date = db.Column(db.Date)
    category = db.Column(db.String(50), default='events')  # events, infrastructure, activities, achievements
    is_published = db.Column(db.Boolean, default=True)
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    photos = db.relationship('GalleryPhoto', backref='album', lazy='dynamic',
                            cascade='all, delete-orphan')

    def __repr__(self):
        return f'<GalleryAlbum {self.title}>'


class GalleryPhoto(db.Model):
    __tablename__ = 'gallery_photos'

    id = db.Column(db.Integer, primary_key=True)
    album_id = db.Column(db.Integer, db.ForeignKey('gallery_albums.id'), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    caption = db.Column(db.String(500))
    order = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<GalleryPhoto {self.id}>'
