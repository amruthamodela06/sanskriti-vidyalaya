import os
import uuid
from werkzeug.utils import secure_filename
from flask import current_app
from PIL import Image

def allowed_file(filename, allowed_extensions):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, subfolder, create_thumbnail=False):
    """Save uploaded file and optionally create thumbnail"""
    if file and file.filename:
        filename = secure_filename(file.filename)
        # Add unique prefix to prevent overwrites
        unique_filename = f"{uuid.uuid4().hex[:8]}_{filename}"

        # Create subfolder if not exists
        upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
        os.makedirs(upload_path, exist_ok=True)

        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)

        # Create thumbnail if image
        thumbnail_url = None
        if create_thumbnail and allowed_file(filename, current_app.config['ALLOWED_IMAGE_EXTENSIONS']):
            thumbnail_url = create_thumbnail_image(file_path, upload_path, unique_filename)

        return f"uploads/{subfolder}/{unique_filename}", thumbnail_url
    return None, None

def create_thumbnail_image(file_path, upload_path, filename, size=(300, 300)):
    """Create thumbnail for an image"""
    thumb_filename = f"thumb_{filename}"
    thumb_path = os.path.join(upload_path, thumb_filename)

    with Image.open(file_path) as img:
        img.thumbnail(size)
        img.save(thumb_path)

    subfolder = os.path.basename(upload_path)
    return f"uploads/{subfolder}/{thumb_filename}"

def generate_slug(title, model_class, existing_id=None):
    """Generate unique slug from title"""
    from slugify import slugify
    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while True:
        query = model_class.query.filter_by(slug=slug)
        if existing_id:
            query = query.filter(model_class.id != existing_id)
        if not query.first():
            break
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug

def delete_file(file_url):
    """Delete a file from uploads"""
    if file_url:
        file_path = os.path.join(current_app.static_folder, file_url)
        if os.path.exists(file_path):
            os.remove(file_path)
