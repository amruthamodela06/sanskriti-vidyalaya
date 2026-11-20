from datetime import datetime, date
from flask import Blueprint, render_template, request, flash, redirect, url_for, current_app, Response
from app.extensions import db
from app.models import (Blog, Event, Holiday, GalleryAlbum, GalleryPhoto,
                       Timetable, StaticContent, Announcement, ContactMessage, Staff,
                       AdmissionInquiry)
from app.forms.contact import ContactForm, AdmissionInquiryForm

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def home():
    # Get active announcements
    today = date.today()
    announcements = Announcement.query.filter(
        Announcement.is_active == True,
        (Announcement.start_date == None) | (Announcement.start_date <= today),
        (Announcement.end_date == None) | (Announcement.end_date >= today)
    ).order_by(Announcement.priority.desc()).all()

    # Get featured/recent news
    news = Blog.query.filter_by(is_published=True).order_by(
        Blog.is_featured.desc(), Blog.published_at.desc()).limit(6).all()

    # Get upcoming events
    events = Event.query.filter(
        Event.event_date >= today,
        Event.is_published == True
    ).order_by(Event.event_date).limit(4).all()

    # Get recent gallery albums
    albums = GalleryAlbum.query.filter_by(is_published=True).order_by(
        GalleryAlbum.created_at.desc()).limit(4).all()

    return render_template('public/home.html',
                          announcements=announcements,
                          news=news,
                          events=events,
                          albums=albums)

@public_bp.route('/about')
def about():
    contents = StaticContent.query.filter_by(
        page_key='about', is_active=True
    ).order_by(StaticContent.order).all()
    return render_template('public/about.html', contents=contents)

@public_bp.route('/academics')
def academics():
    contents = StaticContent.query.filter_by(
        page_key='academics', is_active=True
    ).order_by(StaticContent.order).all()
    timetables = Timetable.query.filter_by(is_active=True).order_by(
        Timetable.class_name, Timetable.section).all()
    return render_template('public/academics.html', contents=contents, timetables=timetables)

@public_bp.route('/admissions', methods=['GET', 'POST'])
def admissions():
    form = AdmissionInquiryForm()
    contents = StaticContent.query.filter_by(
        page_key='admissions', is_active=True
    ).order_by(StaticContent.order).all()

    if form.validate_on_submit():
        inquiry = AdmissionInquiry(
            student_name=form.student_name.data,
            parent_name=form.parent_name.data,
            email=form.email.data,
            phone=form.phone.data,
            class_applying=form.class_applying.data,
            previous_school=form.previous_school.data,
            message=form.message.data
        )
        db.session.add(inquiry)
        db.session.commit()
        flash('Thank you for your admission inquiry! We will contact you soon.', 'success')
        return redirect(url_for('public.admissions'))

    return render_template('public/admissions.html', contents=contents, form=form)

@public_bp.route('/gallery')
def gallery():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')

    query = GalleryAlbum.query.filter_by(is_published=True)
    if category:
        query = query.filter_by(category=category)

    albums = query.order_by(GalleryAlbum.order, GalleryAlbum.created_at.desc()).paginate(
        page=page, per_page=12)

    categories = db.session.query(GalleryAlbum.category).distinct().all()
    categories = [c[0] for c in categories if c[0]]

    return render_template('public/gallery.html', albums=albums, categories=categories, current_category=category)

@public_bp.route('/gallery/<slug>')
def gallery_album(slug):
    album = GalleryAlbum.query.filter_by(slug=slug, is_published=True).first_or_404()
    photos = album.photos.order_by(GalleryPhoto.order).all()
    return render_template('public/gallery_album.html', album=album, photos=photos)

@public_bp.route('/news')
def news():
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    search_query = request.args.get('q', '').strip()

    query = Blog.query.filter_by(is_published=True)
    if category:
        query = query.filter_by(category=category)
    if search_query:
        like_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Blog.title.ilike(like_pattern),
                Blog.excerpt.ilike(like_pattern),
                Blog.content.ilike(like_pattern)
            )
        )

    blogs = query.order_by(Blog.published_at.desc()).paginate(
        page=page, per_page=current_app.config['ITEMS_PER_PAGE'])

    return render_template('public/news.html', blogs=blogs, current_category=category, search_query=search_query)

@public_bp.route('/news/<slug>')
def news_detail(slug):
    blog = Blog.query.filter_by(slug=slug, is_published=True).first_or_404()
    # Increment views
    blog.views += 1
    db.session.commit()

    # Get related posts
    related = Blog.query.filter(
        Blog.is_published == True,
        Blog.id != blog.id,
        Blog.category == blog.category
    ).order_by(Blog.published_at.desc()).limit(3).all()

    return render_template('public/news_detail.html', blog=blog, related=related)

@public_bp.route('/events')
def events():
    today = date.today()

    # Upcoming events
    upcoming = Event.query.filter(
        Event.event_date >= today,
        Event.is_published == True
    ).order_by(Event.event_date).all()

    # Past events
    past = Event.query.filter(
        Event.event_date < today,
        Event.is_published == True
    ).order_by(Event.event_date.desc()).limit(10).all()

    # Holidays
    holidays = Holiday.query.filter(
        Holiday.date >= today
    ).order_by(Holiday.date).all()

    return render_template('public/events.html',
                          upcoming=upcoming,
                          past=past,
                          holidays=holidays)

@public_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    contents = StaticContent.query.filter_by(
        page_key='contact', is_active=True
    ).order_by(StaticContent.order).all()

    if form.validate_on_submit():
        message = ContactMessage(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            subject=form.subject.data,
            message=form.message.data
        )
        db.session.add(message)
        db.session.commit()
        flash('Thank you for your message. We will get back to you soon!', 'success')
        return redirect(url_for('public.contact'))

    return render_template('public/contact.html', form=form, contents=contents)


@public_bp.route('/faculty')
def faculty():
    selected_dept = request.args.get('department', '').strip()
    search_query = request.args.get('q', '').strip()

    query = Staff.query.filter_by(is_active=True)
    if search_query:
        like_pattern = f"%{search_query}%"
        query = query.filter(
            db.or_(
                Staff.name.ilike(like_pattern),
                Staff.subjects_taught.ilike(like_pattern),
                Staff.qualifications.ilike(like_pattern)
            )
        )

    staff_members = query.order_by(Staff.order, Staff.name).all()

    # Collect all available departments for filter pills
    all_depts_rows = db.session.query(Staff.department).filter(
        Staff.is_active == True,
        Staff.department.isnot(None),
        Staff.department != ''
    ).distinct().all()
    available_departments = sorted({row[0] for row in all_depts_rows})

    # Separate leadership (Principal, Vice Principal) from other staff
    leadership = []
    departments = {}

    for member in staff_members:
        if member.designation in ['principal', 'vice_principal'] and not selected_dept:
            leadership.append(member)
        elif member.designation not in ['principal', 'vice_principal']:
            dept = member.department or 'other'
            if selected_dept and dept != selected_dept:
                continue
            if dept not in departments:
                departments[dept] = []
            departments[dept].append(member)

    return render_template('public/faculty.html',
                          leadership=leadership,
                          departments=departments,
                          available_departments=available_departments,
                          selected_dept=selected_dept,
                          search_query=search_query)


@public_bp.route('/sitemap.xml')
def sitemap():
    """Generate dynamic XML sitemap for public pages, news, and albums."""
    pages = []
    static_endpoints = [
        'public.home', 'public.about', 'public.academics', 'public.admissions',
        'public.faculty', 'public.gallery', 'public.news', 'public.events', 'public.contact'
    ]
    for endpoint in static_endpoints:
        pages.append({
            'loc': url_for(endpoint, _external=True),
            'changefreq': 'weekly',
            'priority': '1.0' if endpoint == 'public.home' else '0.8'
        })

    blogs = Blog.query.filter_by(is_published=True).order_by(Blog.published_at.desc()).all()
    for blog in blogs:
        lastmod = (blog.updated_at or blog.published_at or blog.created_at).strftime('%Y-%m-%d')
        pages.append({
            'loc': url_for('public.news_detail', slug=blog.slug, _external=True),
            'lastmod': lastmod,
            'changefreq': 'monthly',
            'priority': '0.7'
        })

    albums = GalleryAlbum.query.filter_by(is_published=True).order_by(GalleryAlbum.created_at.desc()).all()
    for album in albums:
        pages.append({
            'loc': url_for('public.gallery_album', slug=album.slug, _external=True),
            'lastmod': album.created_at.strftime('%Y-%m-%d'),
            'changefreq': 'monthly',
            'priority': '0.6'
        })

    xml_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                 '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for page in pages:
        xml_lines.append('  <url>')
        xml_lines.append(f'    <loc>{page["loc"]}</loc>')
        if 'lastmod' in page:
            xml_lines.append(f'    <lastmod>{page["lastmod"]}</lastmod>')
        xml_lines.append(f'    <changefreq>{page["changefreq"]}</changefreq>')
        xml_lines.append(f'    <priority>{page["priority"]}</priority>')
        xml_lines.append('  </url>')
    xml_lines.append('</urlset>')

    return Response('\n'.join(xml_lines), mimetype='application/xml')


@public_bp.route('/robots.txt')
def robots_txt():
    """Serve robots.txt for search engine crawlers."""
    sitemap_url = url_for('public.sitemap', _external=True)
    content = f"User-agent: *\nAllow: /\nDisallow: /admin/\nDisallow: /login\nSitemap: {sitemap_url}\n"
    return Response(content, mimetype='text/plain')
