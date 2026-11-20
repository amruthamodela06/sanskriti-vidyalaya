import os
import unittest
from datetime import date, datetime

from app import create_app
from app.config import Config
from app.extensions import db
from app.models import (
    User, Blog, Event, Holiday, Staff, FAQ, Testimonial,
    Announcement, AdmissionInquiry, ContactMessage
)


class TestConfig(Config):
    TESTING = True
    WTF_CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


class SanskritiVidyalayaTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

        # Create admin user
        self.admin = User(username='admin', email='admin@test.edu', is_admin=True, is_active=True)
        self.admin.set_password('admin123')
        db.session.add(self.admin)

        # Sample data
        self.blog = Blog(
            title='Annual Science Fair 2026',
            slug='annual-science-fair-2026',
            content='<p>Students showcased innovative science projects.</p>',
            excerpt='Science fair highlights.',
            category='news',
            is_published=True,
            published_at=datetime.utcnow()
        )
        self.event = Event(
            title='Sports Day',
            description='Annual inter-house athletic meet.',
            event_date=date(2026, 12, 15),
            location='School Ground',
            event_type='sports',
            is_published=True
        )
        self.staff = Staff(
            name='Dr. Kavita Rao',
            designation='teacher',
            department='science',
            subjects_taught='Physics, Chemistry',
            is_active=True
        )
        self.faq = FAQ(
            question='What are school hours?',
            answer='8:30 AM to 3:00 PM',
            category='general',
            is_active=True
        )
        self.testimonial = Testimonial(
            author_name='Suresh Iyer',
            role='Parent',
            quote='Great school!',
            rating=5,
            is_featured=True,
            is_active=True
        )
        db.session.add_all([self.blog, self.event, self.staff, self.faq, self.testimonial])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def login_admin(self):
        return self.client.post('/login', data={
            'username': 'admin',
            'password': 'admin123'
        }, follow_redirects=True)

    def test_public_pages_load(self):
        for route in ['/', '/about', '/academics', '/admissions', '/faculty',
                      '/gallery', '/news', '/events', '/contact', '/faq', '/downloads', '/search']:
            resp = self.client.get(route)
            self.assertEqual(resp.status_code, 200, f"Route {route} failed")

    def test_health_and_seo_routes(self):
        health = self.client.get('/health')
        self.assertEqual(health.status_code, 200)
        self.assertEqual(health.get_json()['status'], 'healthy')

        sitemap = self.client.get('/sitemap.xml')
        self.assertEqual(sitemap.status_code, 200)
        self.assertIn(b'<urlset', sitemap.data)

        robots = self.client.get('/robots.txt')
        self.assertEqual(robots.status_code, 200)
        self.assertIn(b'Sitemap:', robots.data)

        rss = self.client.get('/news/feed.xml')
        self.assertEqual(rss.status_code, 200)
        self.assertIn(b'<rss version="2.0"', rss.data)

    def test_security_headers(self):
        resp = self.client.get('/')
        self.assertEqual(resp.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(resp.headers.get('X-Frame-Options'), 'SAMEORIGIN')

    def test_event_detail_and_ics(self):
        detail = self.client.get(f'/events/{self.event.id}')
        self.assertEqual(detail.status_code, 200)
        self.assertIn(b'Sports Day', detail.data)

        ics = self.client.get(f'/events/{self.event.id}/ics')
        self.assertEqual(ics.status_code, 200)
        self.assertIn(b'BEGIN:VCALENDAR', ics.data)
        self.assertIn(b'SUMMARY:Sports Day', ics.data)

    def test_search_and_filters(self):
        resp = self.client.get('/search?q=Science')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Annual Science Fair 2026', resp.data)

        faculty = self.client.get('/faculty?department=science')
        self.assertEqual(faculty.status_code, 200)
        self.assertIn(b'Dr. Kavita Rao', faculty.data)

    def test_api_v1_endpoints(self):
        for ep in ['/api/v1/news', '/api/v1/events', '/api/v1/announcements', '/api/v1/faculty', '/api/v1/faqs']:
            resp = self.client.get(ep)
            self.assertEqual(resp.status_code, 200)
            data = resp.get_json()
            self.assertIn('count', data)
            self.assertIn('items', data)

    def test_admin_auth_and_exports(self):
        unauth = self.client.get('/admin/')
        self.assertEqual(unauth.status_code, 302)

        login_resp = self.login_admin()
        self.assertEqual(login_resp.status_code, 200)

        adm_csv = self.client.get('/admin/admissions/export')
        self.assertEqual(adm_csv.status_code, 200)
        self.assertEqual(adm_csv.mimetype, 'text/csv')

        msg_csv = self.client.get('/admin/messages/export')
        self.assertEqual(msg_csv.status_code, 200)
        self.assertEqual(msg_csv.mimetype, 'text/csv')

    def test_404_handler(self):
        resp = self.client.get('/non-existent-page-xyz')
        self.assertEqual(resp.status_code, 404)


if __name__ == '__main__':
    unittest.main()
