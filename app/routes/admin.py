import csv
import io
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, Response
from flask_login import login_required, current_user
from app.extensions import db
from app.models import (User, Blog, Event, Holiday, GalleryAlbum, GalleryPhoto,
                       Timetable, StaticContent, Announcement, ContactMessage, Setting, Staff,
                       AdmissionInquiry)
from app.forms.blog import BlogForm
from app.forms.event import EventForm, HolidayForm
from app.forms.gallery import AlbumForm, PhotoUploadForm, PhotoEditForm
from app.forms.content import StaticContentForm, AnnouncementForm, TimetableForm
from app.forms.contact import MessageReplyForm
from app.forms.staff import StaffForm
from app.utils.decorators import admin_required
from app.utils.helpers import save_uploaded_file, generate_slug, delete_file

admin_bp = Blueprint('admin', __name__)


@admin_bp.context_processor
def inject_admin_badges():
    """Inject unread message and pending admission counts for the admin sidebar."""
    try:
        unread_messages_count = ContactMessage.query.filter_by(is_read=False).count()
        pending_admissions_count = AdmissionInquiry.query.filter_by(status='pending').count()
    except Exception:
        unread_messages_count = 0
        pending_admissions_count = 0
    return dict(
        unread_messages_count=unread_messages_count,
        pending_admissions_count=pending_admissions_count
    )

# ============================================
# Dashboard
# ============================================
@admin_bp.route('/')
@admin_required
def dashboard():
    stats = {
        'blogs': Blog.query.count(),
        'events': Event.query.count(),
        'albums': GalleryAlbum.query.count(),
        'messages': ContactMessage.query.filter_by(is_read=False).count(),
        'pending_admissions': AdmissionInquiry.query.filter_by(status='pending').count(),
        'staff': Staff.query.filter_by(is_active=True).count()
    }
    recent_blogs = Blog.query.order_by(Blog.created_at.desc()).limit(5).all()
    recent_messages = ContactMessage.query.filter_by(is_read=False).order_by(ContactMessage.created_at.desc()).limit(5).all()
    upcoming_events = Event.query.filter(Event.event_date >= datetime.now().date()).order_by(Event.event_date).limit(5).all()
    recent_admissions = AdmissionInquiry.query.order_by(AdmissionInquiry.created_at.desc()).limit(5).all()

    return render_template('admin/dashboard.html',
                          stats=stats,
                          recent_blogs=recent_blogs,
                          recent_messages=recent_messages,
                          upcoming_events=upcoming_events,
                          recent_admissions=recent_admissions)

# ============================================
# Blog Management
# ============================================
@admin_bp.route('/blogs')
@admin_required
def blogs_list():
    page = request.args.get('page', 1, type=int)
    blogs = Blog.query.order_by(Blog.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/blogs/list.html', blogs=blogs)

@admin_bp.route('/blogs/new', methods=['GET', 'POST'])
@admin_required
def blog_create():
    form = BlogForm()
    if form.validate_on_submit():
        blog = Blog(
            title=form.title.data,
            slug=generate_slug(form.title.data, Blog),
            content=form.content.data,
            excerpt=form.excerpt.data,
            category=form.category.data,
            is_featured=form.is_featured.data,
            is_published=form.is_published.data,
            author_id=current_user.id
        )
        if form.is_published.data:
            blog.published_at = datetime.utcnow()

        if form.image.data:
            image_url, _ = save_uploaded_file(form.image.data, 'blog_images')
            blog.image_url = image_url

        db.session.add(blog)
        db.session.commit()
        flash('Blog post created successfully.', 'success')
        return redirect(url_for('admin.blogs_list'))

    return render_template('admin/blogs/form.html', form=form, title='Create Blog Post')

@admin_bp.route('/blogs/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def blog_edit(id):
    blog = Blog.query.get_or_404(id)
    form = BlogForm(obj=blog)

    if form.validate_on_submit():
        blog.title = form.title.data
        blog.slug = generate_slug(form.title.data, Blog, blog.id)
        blog.content = form.content.data
        blog.excerpt = form.excerpt.data
        blog.category = form.category.data
        blog.is_featured = form.is_featured.data

        if form.is_published.data and not blog.is_published:
            blog.published_at = datetime.utcnow()
        blog.is_published = form.is_published.data

        if form.image.data:
            if blog.image_url:
                delete_file(blog.image_url)
            image_url, _ = save_uploaded_file(form.image.data, 'blog_images')
            blog.image_url = image_url

        db.session.commit()
        flash('Blog post updated successfully.', 'success')
        return redirect(url_for('admin.blogs_list'))

    return render_template('admin/blogs/form.html', form=form, title='Edit Blog Post', blog=blog)

@admin_bp.route('/blogs/<int:id>/delete', methods=['POST'])
@admin_required
def blog_delete(id):
    blog = Blog.query.get_or_404(id)
    if blog.image_url:
        delete_file(blog.image_url)
    db.session.delete(blog)
    db.session.commit()
    flash('Blog post deleted successfully.', 'success')
    return redirect(url_for('admin.blogs_list'))

# ============================================
# Events Management
# ============================================
@admin_bp.route('/events')
@admin_required
def events_list():
    page = request.args.get('page', 1, type=int)
    events = Event.query.order_by(Event.event_date.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/events/list.html', events=events)

@admin_bp.route('/events/new', methods=['GET', 'POST'])
@admin_required
def event_create():
    form = EventForm()
    if form.validate_on_submit():
        event = Event(
            title=form.title.data,
            description=form.description.data,
            event_date=form.event_date.data,
            event_time=form.event_time.data,
            end_date=form.end_date.data,
            location=form.location.data,
            event_type=form.event_type.data,
            is_featured=form.is_featured.data,
            is_published=form.is_published.data
        )
        if form.image.data:
            image_url, _ = save_uploaded_file(form.image.data, 'events')
            event.image_url = image_url

        db.session.add(event)
        db.session.commit()
        flash('Event created successfully.', 'success')
        return redirect(url_for('admin.events_list'))

    return render_template('admin/events/form.html', form=form, title='Create Event')

@admin_bp.route('/events/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def event_edit(id):
    event = Event.query.get_or_404(id)
    form = EventForm(obj=event)

    if form.validate_on_submit():
        event.title = form.title.data
        event.description = form.description.data
        event.event_date = form.event_date.data
        event.event_time = form.event_time.data
        event.end_date = form.end_date.data
        event.location = form.location.data
        event.event_type = form.event_type.data
        event.is_featured = form.is_featured.data
        event.is_published = form.is_published.data

        if form.image.data:
            if event.image_url:
                delete_file(event.image_url)
            image_url, _ = save_uploaded_file(form.image.data, 'events')
            event.image_url = image_url

        db.session.commit()
        flash('Event updated successfully.', 'success')
        return redirect(url_for('admin.events_list'))

    return render_template('admin/events/form.html', form=form, title='Edit Event', event=event)

@admin_bp.route('/events/<int:id>/delete', methods=['POST'])
@admin_required
def event_delete(id):
    event = Event.query.get_or_404(id)
    if event.image_url:
        delete_file(event.image_url)
    db.session.delete(event)
    db.session.commit()
    flash('Event deleted successfully.', 'success')
    return redirect(url_for('admin.events_list'))

# ============================================
# Holidays Management
# ============================================
@admin_bp.route('/holidays')
@admin_required
def holidays_list():
    page = request.args.get('page', 1, type=int)
    holidays = Holiday.query.order_by(Holiday.date.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/holidays/list.html', holidays=holidays)

@admin_bp.route('/holidays/new', methods=['GET', 'POST'])
@admin_required
def holiday_create():
    form = HolidayForm()
    if form.validate_on_submit():
        holiday = Holiday(
            name=form.name.data,
            date=form.date.data,
            end_date=form.end_date.data,
            description=form.description.data,
            holiday_type=form.holiday_type.data,
            academic_year=form.academic_year.data
        )
        db.session.add(holiday)
        db.session.commit()
        flash('Holiday created successfully.', 'success')
        return redirect(url_for('admin.holidays_list'))

    return render_template('admin/holidays/form.html', form=form, title='Add Holiday')

@admin_bp.route('/holidays/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def holiday_edit(id):
    holiday = Holiday.query.get_or_404(id)
    form = HolidayForm(obj=holiday)

    if form.validate_on_submit():
        holiday.name = form.name.data
        holiday.date = form.date.data
        holiday.end_date = form.end_date.data
        holiday.description = form.description.data
        holiday.holiday_type = form.holiday_type.data
        holiday.academic_year = form.academic_year.data

        db.session.commit()
        flash('Holiday updated successfully.', 'success')
        return redirect(url_for('admin.holidays_list'))

    return render_template('admin/holidays/form.html', form=form, title='Edit Holiday', holiday=holiday)

@admin_bp.route('/holidays/<int:id>/delete', methods=['POST'])
@admin_required
def holiday_delete(id):
    holiday = Holiday.query.get_or_404(id)
    db.session.delete(holiday)
    db.session.commit()
    flash('Holiday deleted successfully.', 'success')
    return redirect(url_for('admin.holidays_list'))

# ============================================
# Gallery Management
# ============================================
@admin_bp.route('/gallery')
@admin_required
def gallery_albums():
    page = request.args.get('page', 1, type=int)
    albums = GalleryAlbum.query.order_by(GalleryAlbum.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/gallery/albums.html', albums=albums)

@admin_bp.route('/gallery/new', methods=['GET', 'POST'])
@admin_required
def album_create():
    form = AlbumForm()
    if form.validate_on_submit():
        album = GalleryAlbum(
            title=form.title.data,
            slug=generate_slug(form.title.data, GalleryAlbum),
            description=form.description.data,
            event_date=form.event_date.data,
            category=form.category.data,
            is_published=form.is_published.data,
            order=form.order.data
        )
        if form.cover_image.data:
            image_url, _ = save_uploaded_file(form.cover_image.data, 'gallery')
            album.cover_image = image_url

        db.session.add(album)
        db.session.commit()
        flash('Album created successfully.', 'success')
        return redirect(url_for('admin.album_photos', id=album.id))

    return render_template('admin/gallery/album_form.html', form=form, title='Create Album')

@admin_bp.route('/gallery/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def album_edit(id):
    album = GalleryAlbum.query.get_or_404(id)
    form = AlbumForm(obj=album)

    if form.validate_on_submit():
        album.title = form.title.data
        album.slug = generate_slug(form.title.data, GalleryAlbum, album.id)
        album.description = form.description.data
        album.event_date = form.event_date.data
        album.category = form.category.data
        album.is_published = form.is_published.data
        album.order = form.order.data

        if form.cover_image.data:
            if album.cover_image:
                delete_file(album.cover_image)
            image_url, _ = save_uploaded_file(form.cover_image.data, 'gallery')
            album.cover_image = image_url

        db.session.commit()
        flash('Album updated successfully.', 'success')
        return redirect(url_for('admin.gallery_albums'))

    return render_template('admin/gallery/album_form.html', form=form, title='Edit Album', album=album)

@admin_bp.route('/gallery/<int:id>/photos', methods=['GET', 'POST'])
@admin_required
def album_photos(id):
    album = GalleryAlbum.query.get_or_404(id)
    form = PhotoUploadForm()

    if form.validate_on_submit() and form.photos.data:
        for photo_file in form.photos.data:
            if photo_file:
                image_url, thumb_url = save_uploaded_file(photo_file, 'gallery', create_thumbnail=True)
                if image_url:
                    photo = GalleryPhoto(
                        album_id=album.id,
                        image_url=image_url,
                        thumbnail_url=thumb_url
                    )
                    db.session.add(photo)
        db.session.commit()
        flash('Photos uploaded successfully.', 'success')
        return redirect(url_for('admin.album_photos', id=id))

    photos = album.photos.order_by(GalleryPhoto.order).all()
    return render_template('admin/gallery/photos.html', album=album, photos=photos, form=form)

@admin_bp.route('/gallery/photo/<int:id>/delete', methods=['POST'])
@admin_required
def photo_delete(id):
    photo = GalleryPhoto.query.get_or_404(id)
    album_id = photo.album_id
    if photo.image_url:
        delete_file(photo.image_url)
    if photo.thumbnail_url:
        delete_file(photo.thumbnail_url)
    db.session.delete(photo)
    db.session.commit()
    flash('Photo deleted successfully.', 'success')
    return redirect(url_for('admin.album_photos', id=album_id))

@admin_bp.route('/gallery/<int:id>/delete', methods=['POST'])
@admin_required
def album_delete(id):
    album = GalleryAlbum.query.get_or_404(id)
    # Delete all photos
    for photo in album.photos:
        if photo.image_url:
            delete_file(photo.image_url)
        if photo.thumbnail_url:
            delete_file(photo.thumbnail_url)
    if album.cover_image:
        delete_file(album.cover_image)
    db.session.delete(album)
    db.session.commit()
    flash('Album deleted successfully.', 'success')
    return redirect(url_for('admin.gallery_albums'))

# ============================================
# Timetables Management
# ============================================
@admin_bp.route('/timetables')
@admin_required
def timetables_list():
    timetables = Timetable.query.order_by(Timetable.class_name, Timetable.section).all()
    return render_template('admin/timetables/list.html', timetables=timetables)

@admin_bp.route('/timetables/new', methods=['GET', 'POST'])
@admin_required
def timetable_create():
    form = TimetableForm()
    if form.validate_on_submit():
        timetable = Timetable(
            class_name=form.class_name.data,
            section=form.section.data,
            academic_year=form.academic_year.data,
            is_active=form.is_active.data
        )
        if form.file.data:
            file_url, _ = save_uploaded_file(form.file.data, 'timetables')
            timetable.file_url = file_url
            # Determine file type
            ext = form.file.data.filename.rsplit('.', 1)[1].lower()
            timetable.file_type = 'pdf' if ext == 'pdf' else 'image'

        db.session.add(timetable)
        db.session.commit()
        flash('Timetable created successfully.', 'success')
        return redirect(url_for('admin.timetables_list'))

    return render_template('admin/timetables/form.html', form=form, title='Add Timetable')

@admin_bp.route('/timetables/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def timetable_edit(id):
    timetable = Timetable.query.get_or_404(id)
    form = TimetableForm(obj=timetable)

    if form.validate_on_submit():
        timetable.class_name = form.class_name.data
        timetable.section = form.section.data
        timetable.academic_year = form.academic_year.data
        timetable.is_active = form.is_active.data

        if form.file.data:
            if timetable.file_url:
                delete_file(timetable.file_url)
            file_url, _ = save_uploaded_file(form.file.data, 'timetables')
            timetable.file_url = file_url
            ext = form.file.data.filename.rsplit('.', 1)[1].lower()
            timetable.file_type = 'pdf' if ext == 'pdf' else 'image'

        db.session.commit()
        flash('Timetable updated successfully.', 'success')
        return redirect(url_for('admin.timetables_list'))

    return render_template('admin/timetables/form.html', form=form, title='Edit Timetable', timetable=timetable)

@admin_bp.route('/timetables/<int:id>/delete', methods=['POST'])
@admin_required
def timetable_delete(id):
    timetable = Timetable.query.get_or_404(id)
    if timetable.file_url:
        delete_file(timetable.file_url)
    db.session.delete(timetable)
    db.session.commit()
    flash('Timetable deleted successfully.', 'success')
    return redirect(url_for('admin.timetables_list'))

# ============================================
# Static Content Management
# ============================================
@admin_bp.route('/content')
@admin_required
def content_list():
    contents = StaticContent.query.order_by(StaticContent.page_key, StaticContent.order).all()
    # Group by page
    pages = {}
    for content in contents:
        if content.page_key not in pages:
            pages[content.page_key] = []
        pages[content.page_key].append(content)
    return render_template('admin/content/list.html', pages=pages)

@admin_bp.route('/content/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def content_edit(id):
    content = StaticContent.query.get_or_404(id)
    form = StaticContentForm(obj=content)

    if form.validate_on_submit():
        content.title = form.title.data
        content.content = form.content.data
        content.order = form.order.data
        content.is_active = form.is_active.data

        if form.image.data:
            if content.image_url:
                delete_file(content.image_url)
            image_url, _ = save_uploaded_file(form.image.data, 'content')
            content.image_url = image_url

        db.session.commit()
        flash('Content updated successfully.', 'success')
        return redirect(url_for('admin.content_list'))

    return render_template('admin/content/form.html', form=form, content=content)

# ============================================
# Announcements Management
# ============================================
@admin_bp.route('/announcements')
@admin_required
def announcements_list():
    announcements = Announcement.query.order_by(Announcement.priority.desc(), Announcement.created_at.desc()).all()
    return render_template('admin/announcements/list.html', announcements=announcements)

@admin_bp.route('/announcements/new', methods=['GET', 'POST'])
@admin_required
def announcement_create():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(
            title=form.title.data,
            content=form.content.data,
            link_url=form.link_url.data,
            link_text=form.link_text.data,
            announcement_type=form.announcement_type.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            priority=form.priority.data,
            is_active=form.is_active.data
        )
        db.session.add(announcement)
        db.session.commit()
        flash('Announcement created successfully.', 'success')
        return redirect(url_for('admin.announcements_list'))

    return render_template('admin/announcements/form.html', form=form, title='Create Announcement')

@admin_bp.route('/announcements/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def announcement_edit(id):
    announcement = Announcement.query.get_or_404(id)
    form = AnnouncementForm(obj=announcement)

    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        announcement.link_url = form.link_url.data
        announcement.link_text = form.link_text.data
        announcement.announcement_type = form.announcement_type.data
        announcement.start_date = form.start_date.data
        announcement.end_date = form.end_date.data
        announcement.priority = form.priority.data
        announcement.is_active = form.is_active.data

        db.session.commit()
        flash('Announcement updated successfully.', 'success')
        return redirect(url_for('admin.announcements_list'))

    return render_template('admin/announcements/form.html', form=form, title='Edit Announcement', announcement=announcement)

@admin_bp.route('/announcements/<int:id>/delete', methods=['POST'])
@admin_required
def announcement_delete(id):
    announcement = Announcement.query.get_or_404(id)
    db.session.delete(announcement)
    db.session.commit()
    flash('Announcement deleted successfully.', 'success')
    return redirect(url_for('admin.announcements_list'))

# ============================================
# Contact Messages
# ============================================
@admin_bp.route('/messages')
@admin_required
def messages_list():
    page = request.args.get('page', 1, type=int)
    messages = ContactMessage.query.order_by(ContactMessage.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/messages.html', messages=messages)

@admin_bp.route('/messages/<int:id>', methods=['GET', 'POST'])
@admin_required
def message_detail(id):
    message = ContactMessage.query.get_or_404(id)
    form = MessageReplyForm(obj=message)

    if form.validate_on_submit():
        message.admin_notes = form.admin_notes.data
        message.is_read = form.is_read.data
        message.is_replied = form.is_replied.data
        db.session.commit()
        flash('Message updated successfully.', 'success')
        return redirect(url_for('admin.messages_list'))

    # Mark as read when viewed
    if not message.is_read:
        message.is_read = True
        db.session.commit()

    return render_template('admin/message_detail.html', message=message, form=form)

@admin_bp.route('/messages/<int:id>/delete', methods=['POST'])
@admin_required
def message_delete(id):
    message = ContactMessage.query.get_or_404(id)
    db.session.delete(message)
    db.session.commit()
    flash('Message deleted successfully.', 'success')
    return redirect(url_for('admin.messages_list'))

# ============================================
# Settings
# ============================================
@admin_bp.route('/settings', methods=['GET', 'POST'])
@admin_required
def settings():
    if request.method == 'POST':
        for key in request.form:
            if key.startswith('setting_'):
                setting_key = key.replace('setting_', '')
                setting = Setting.query.filter_by(key=setting_key).first()
                if setting:
                    setting.value = request.form[key]
        db.session.commit()
        flash('Settings updated successfully.', 'success')
        return redirect(url_for('admin.settings'))

    settings = Setting.query.order_by(Setting.key).all()
    return render_template('admin/settings.html', settings=settings)


# ============================================
# Staff Management
# ============================================
@admin_bp.route('/staff')
@admin_required
def staff_list():
    page = request.args.get('page', 1, type=int)
    staff = Staff.query.order_by(Staff.order, Staff.name).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/staff/list.html', staff=staff)


@admin_bp.route('/staff/new', methods=['GET', 'POST'])
@admin_required
def staff_create():
    form = StaffForm()
    if form.validate_on_submit():
        staff = Staff(
            name=form.name.data,
            designation=form.designation.data,
            department=form.department.data if form.department.data else None,
            subjects_taught=form.subjects_taught.data,
            qualifications=form.qualifications.data,
            email=form.email.data,
            phone=form.phone.data,
            experience_years=form.experience_years.data,
            bio=form.bio.data,
            order=form.order.data or 0,
            joined_date=form.joined_date.data,
            is_active=form.is_active.data
        )
        if form.photo.data:
            photo_url, _ = save_uploaded_file(form.photo.data, 'staff')
            staff.photo_url = photo_url

        db.session.add(staff)
        db.session.commit()
        flash('Staff member added successfully.', 'success')
        return redirect(url_for('admin.staff_list'))

    return render_template('admin/staff/form.html', form=form, title='Add Staff Member')


@admin_bp.route('/staff/<int:id>/edit', methods=['GET', 'POST'])
@admin_required
def staff_edit(id):
    staff = Staff.query.get_or_404(id)
    form = StaffForm(obj=staff)

    if form.validate_on_submit():
        staff.name = form.name.data
        staff.designation = form.designation.data
        staff.department = form.department.data if form.department.data else None
        staff.subjects_taught = form.subjects_taught.data
        staff.qualifications = form.qualifications.data
        staff.email = form.email.data
        staff.phone = form.phone.data
        staff.experience_years = form.experience_years.data
        staff.bio = form.bio.data
        staff.order = form.order.data or 0
        staff.joined_date = form.joined_date.data
        staff.is_active = form.is_active.data

        if form.photo.data:
            if staff.photo_url:
                delete_file(staff.photo_url)
            photo_url, _ = save_uploaded_file(form.photo.data, 'staff')
            staff.photo_url = photo_url

        db.session.commit()
        flash('Staff member updated successfully.', 'success')
        return redirect(url_for('admin.staff_list'))

    return render_template('admin/staff/form.html', form=form, title='Edit Staff Member', staff=staff)


@admin_bp.route('/staff/<int:id>/delete', methods=['POST'])
@admin_required
def staff_delete(id):
    staff = Staff.query.get_or_404(id)
    if staff.photo_url:
        delete_file(staff.photo_url)
    db.session.delete(staff)
    db.session.commit()
    flash('Staff member deleted successfully.', 'success')
    return redirect(url_for('admin.staff_list'))


# ============================================
# Admission Inquiries
# ============================================
@admin_bp.route('/admissions')
@admin_required
def admissions_list():
    page = request.args.get('page', 1, type=int)
    status = request.args.get('status', '')

    query = AdmissionInquiry.query
    if status:
        query = query.filter_by(status=status)

    inquiries = query.order_by(AdmissionInquiry.created_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])
    return render_template('admin/admissions/list.html', inquiries=inquiries, current_status=status)


@admin_bp.route('/admissions/<int:id>', methods=['GET', 'POST'])
@admin_required
def admission_detail(id):
    inquiry = AdmissionInquiry.query.get_or_404(id)

    if request.method == 'POST':
        inquiry.status = request.form.get('status', inquiry.status)
        inquiry.admin_notes = request.form.get('admin_notes', '')
        inquiry.is_contacted = 'is_contacted' in request.form
        db.session.commit()
        flash('Inquiry updated successfully.', 'success')
        return redirect(url_for('admin.admissions_list'))

    # Mark as read when viewed
    if not inquiry.is_read:
        inquiry.is_read = True
        db.session.commit()

    return render_template('admin/admissions/detail.html', inquiry=inquiry)


@admin_bp.route('/admissions/<int:id>/delete', methods=['POST'])
@admin_required
def admission_delete(id):
    inquiry = AdmissionInquiry.query.get_or_404(id)
    db.session.delete(inquiry)
    db.session.commit()
    flash('Inquiry deleted successfully.', 'success')
    return redirect(url_for('admin.admissions_list'))


@admin_bp.route('/admissions/export')
@admin_required
def admissions_export():
    """Export admission inquiries (optionally filtered by status) as CSV."""
    status = request.args.get('status', '')
    query = AdmissionInquiry.query
    if status:
        query = query.filter_by(status=status)
    inquiries = query.order_by(AdmissionInquiry.created_at.desc()).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Student Name', 'Parent Name', 'Email', 'Phone', 'Class Applying', 'Previous School', 'Status', 'Contacted', 'Message', 'Admin Notes', 'Submitted At'])
    for inq in inquiries:
        writer.writerow([
            inq.id, inq.student_name, inq.parent_name, inq.email, inq.phone,
            inq.class_applying, inq.previous_school or '', inq.status,
            'Yes' if inq.is_contacted else 'No', inq.message or '', inq.admin_notes or '',
            inq.created_at.strftime('%Y-%m-%d %H:%M:%S')
        ])

    filename = f"admission-inquiries{'-' + status if status else ''}.csv"
    return Response(
        output.getvalue(),
        mimetype='text/csv',
        headers={'Content-Disposition': f'attachment; filename={filename}'}
    )
