"""
Seed script to initialize the database with default data
Run this after setting up the application: python seed_data.py
"""

from app import create_app
from app.extensions import db
from app.models import User, StaticContent, Setting

app = create_app()

# Static content to seed
STATIC_CONTENT_SEED = [
    # About Page
    {'page_key': 'about', 'section_key': 'history', 'title': 'Our History', 'content': '<p>Sanskriti Vidyalaya was established with a vision to provide quality education to students. Our journey began with a commitment to academic excellence and holistic development.</p>', 'order': 1},
    {'page_key': 'about', 'section_key': 'vision', 'title': 'Our Vision', 'content': '<p>To be a center of excellence in education, nurturing young minds to become responsible global citizens with strong values and skills.</p>', 'order': 2},
    {'page_key': 'about', 'section_key': 'mission', 'title': 'Our Mission', 'content': '<p>To provide a stimulating learning environment that encourages students to explore, discover, and achieve their full potential while instilling values of integrity, respect, and social responsibility.</p>', 'order': 3},
    {'page_key': 'about', 'section_key': 'principal_message', 'title': "Principal's Message", 'content': '<p>Welcome to Sanskriti Vidyalaya. We believe that every child is unique and has the potential to excel. Our dedicated team of educators is committed to nurturing this potential and guiding students towards success.</p>', 'order': 4},
    {'page_key': 'about', 'section_key': 'infrastructure', 'title': 'Infrastructure', 'content': '<p>Our school is equipped with modern facilities including well-ventilated classrooms, science laboratories, computer labs, library, sports grounds, and more.</p>', 'order': 5},

    # Admissions Page
    {'page_key': 'admissions', 'section_key': 'process', 'title': 'Admission Process', 'content': '<ol><li>Fill out the application form</li><li>Submit required documents</li><li>Attend the entrance assessment</li><li>Interaction with parents and student</li><li>Admission confirmation</li></ol>', 'order': 1},
    {'page_key': 'admissions', 'section_key': 'fees', 'title': 'Fee Structure', 'content': '<p>Please contact the school office for detailed fee structure and payment options.</p>', 'order': 2},
    {'page_key': 'admissions', 'section_key': 'documents', 'title': 'Required Documents', 'content': '<ul><li>Birth Certificate</li><li>Previous School Transfer Certificate</li><li>Report Cards/Mark Sheets</li><li>Passport Size Photographs</li><li>Address Proof</li><li>Aadhar Card (Parent & Child)</li></ul>', 'order': 3},
    {'page_key': 'admissions', 'section_key': 'dates', 'title': 'Important Dates', 'content': '<p>Admissions are open for the academic year. Please contact the office for current admission dates and availability.</p>', 'order': 4},

    # Contact Page
    {'page_key': 'contact', 'section_key': 'timings', 'title': 'Office Timings', 'content': '<p>Monday to Saturday: 9:00 AM - 4:00 PM<br>Sunday: Closed</p>', 'order': 1},

    # Academics Page
    {'page_key': 'academics', 'section_key': 'curriculum', 'title': 'Curriculum', 'content': '<p>Our curriculum is designed to provide a balanced education combining academics with co-curricular activities. We follow a comprehensive syllabus that prepares students for higher education and beyond.</p>', 'order': 1},
    {'page_key': 'academics', 'section_key': 'subjects', 'title': 'Subjects Offered', 'content': '<ul><li>Languages: English, Hindi, Sanskrit</li><li>Mathematics</li><li>Science (Physics, Chemistry, Biology)</li><li>Social Studies</li><li>Computer Science</li><li>Physical Education</li><li>Art & Music</li></ul>', 'order': 2},
]

# Settings to seed
SETTINGS_SEED = [
    {'key': 'site_name', 'value': 'Sanskriti Vidyalaya', 'value_type': 'string', 'description': 'School name displayed on the website'},
    {'key': 'site_tagline', 'value': 'Nurturing Excellence, Building Futures', 'value_type': 'string', 'description': 'School tagline/motto'},
    {'key': 'contact_email', 'value': 'info@sanskritividyala.edu', 'value_type': 'string', 'description': 'Contact email address'},
    {'key': 'contact_phone', 'value': '+91 1234567890', 'value_type': 'string', 'description': 'Contact phone number'},
    {'key': 'address', 'value': 'Main Road, City Name, State - 500001', 'value_type': 'string', 'description': 'School address'},
    {'key': 'map_embed_url', 'value': '', 'value_type': 'string', 'description': 'Google Maps embed URL'},
    {'key': 'facebook_url', 'value': '', 'value_type': 'string', 'description': 'Facebook page URL'},
    {'key': 'twitter_url', 'value': '', 'value_type': 'string', 'description': 'Twitter profile URL'},
    {'key': 'instagram_url', 'value': '', 'value_type': 'string', 'description': 'Instagram profile URL'},
    {'key': 'youtube_url', 'value': '', 'value_type': 'string', 'description': 'YouTube channel URL'},
    {'key': 'current_academic_year', 'value': '2024-2025', 'value_type': 'string', 'description': 'Current academic year'},
]


def seed_database():
    with app.app_context():
        print("Creating database tables...")
        db.create_all()

        # Create admin user if not exists
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            print("Creating admin user...")
            admin = User(
                username='admin',
                email='admin@sanskritividyala.edu',
                is_admin=True,
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created: username='admin', password='admin123'")
        else:
            print("Admin user already exists.")

        # Seed static content
        print("Seeding static content...")
        for content_data in STATIC_CONTENT_SEED:
            existing = StaticContent.query.filter_by(
                page_key=content_data['page_key'],
                section_key=content_data['section_key']
            ).first()
            if not existing:
                content = StaticContent(**content_data)
                db.session.add(content)
                print(f"  Added: {content_data['page_key']}/{content_data['section_key']}")
            else:
                print(f"  Skipped (exists): {content_data['page_key']}/{content_data['section_key']}")
        db.session.commit()

        # Seed settings
        print("Seeding settings...")
        for setting_data in SETTINGS_SEED:
            existing = Setting.query.filter_by(key=setting_data['key']).first()
            if not existing:
                setting = Setting(**setting_data)
                db.session.add(setting)
                print(f"  Added: {setting_data['key']}")
            else:
                print(f"  Skipped (exists): {setting_data['key']}")
        db.session.commit()

        print("\nDatabase seeding completed!")
        print("\n" + "="*50)
        print("IMPORTANT: Change the admin password after first login!")
        print("Login credentials:")
        print("  Username: admin")
        print("  Password: admin123")
        print("="*50)


if __name__ == '__main__':
    seed_database()
