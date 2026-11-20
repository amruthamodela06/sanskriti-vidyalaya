from datetime import date
from flask import Blueprint, jsonify, request
from app.models import Blog, Event, Announcement, Staff, FAQ

api_bp = Blueprint('api', __name__)


@api_bp.route('/news')
def api_news():
    """Return published news/blog articles as JSON."""
    limit = min(request.args.get('limit', 10, type=int), 50)
    category = request.args.get('category', '').strip()
    query = Blog.query.filter_by(is_published=True)
    if category:
        query = query.filter_by(category=category)
    items = query.order_by(Blog.published_at.desc(), Blog.created_at.desc()).limit(limit).all()
    return jsonify({
        'count': len(items),
        'items': [
            {
                'id': b.id,
                'title': b.title,
                'slug': b.slug,
                'category': b.category,
                'excerpt': b.excerpt,
                'is_featured': b.is_featured,
                'views': b.views,
                'published_at': b.published_at.isoformat() if b.published_at else None
            }
            for b in items
        ]
    })


@api_bp.route('/events')
def api_events():
    """Return upcoming published school events as JSON."""
    today = date.today()
    limit = min(request.args.get('limit', 10, type=int), 50)
    events = Event.query.filter(
        Event.is_published == True,
        Event.event_date >= today
    ).order_by(Event.event_date).limit(limit).all()
    return jsonify({
        'count': len(events),
        'items': [
            {
                'id': e.id,
                'title': e.title,
                'event_date': e.event_date.isoformat(),
                'event_time': e.event_time.strftime('%H:%M') if e.event_time else None,
                'end_date': e.end_date.isoformat() if e.end_date else None,
                'location': e.location,
                'event_type': e.event_type,
                'is_featured': e.is_featured
            }
            for e in events
        ]
    })


@api_bp.route('/announcements')
def api_announcements():
    """Return currently active announcements as JSON."""
    today = date.today()
    announcements = Announcement.query.filter(
        Announcement.is_active == True,
        (Announcement.start_date == None) | (Announcement.start_date <= today),
        (Announcement.end_date == None) | (Announcement.end_date >= today)
    ).order_by(Announcement.priority.desc()).all()
    return jsonify({
        'count': len(announcements),
        'items': [
            {
                'id': a.id,
                'title': a.title,
                'content': a.content,
                'type': a.announcement_type,
                'link_url': a.link_url,
                'priority': a.priority
            }
            for a in announcements
        ]
    })


@api_bp.route('/faculty')
def api_faculty():
    """Return active faculty members as JSON."""
    department = request.args.get('department', '').strip()
    query = Staff.query.filter_by(is_active=True)
    if department:
        query = query.filter_by(department=department)
    members = query.order_by(Staff.order, Staff.name).all()
    return jsonify({
        'count': len(members),
        'items': [
            {
                'id': m.id,
                'name': m.name,
                'designation': m.designation,
                'department': m.department,
                'subjects_taught': m.subjects_list,
                'qualifications': m.qualifications,
                'experience_years': m.experience_years
            }
            for m in members
        ]
    })


@api_bp.route('/faqs')
def api_faqs():
    """Return active FAQs as JSON."""
    faqs = FAQ.query.filter_by(is_active=True).order_by(FAQ.order, FAQ.id).all()
    return jsonify({
        'count': len(faqs),
        'items': [
            {
                'id': f.id,
                'question': f.question,
                'answer': f.answer,
                'category': f.category
            }
            for f in faqs
        ]
    })
