# Sanskriti Vidyalaya

A school website built with Flask.

## Features

- **Public Pages**: Home, About, Academics, Admissions, Faculty, Events, News, Gallery, Downloads & Circulars, FAQs, Search, Contact
- **Admin Panel**: Dashboard with live stats, notification badges, quick status toggles, and CSV exports
- **Staff Management**: Add and manage faculty members with department filtering and search
- **Blog/News**: Create and publish news articles with RSS 2.0 feed, reading time, and search
- **Events & Holidays**: Manage school events, holiday calendar, and `.ics` calendar downloads
- **Gallery**: Photo albums with image uploads, thumbnails, captions, and display ordering
- **Timetables**: Upload class timetables with class and academic year filters
- **Downloads & Circulars**: Manage circulars, syllabus PDFs, and forms with download tracking
- **FAQs & Testimonials**: Manage frequently asked questions and parent/student/alumni testimonials
- **Announcements**: Scrolling announcements on homepage
- **Admission Inquiries**: Online admission inquiry form with CSV export
- **Contact Messages**: Receive and manage contact form submissions with status filters and CSV export
- **Site Settings**: Customize school name, contact info, social links
- **REST API & Ops**: Read-only `/api/v1/*` JSON endpoints, `/health` check, `/sitemap.xml`, `/robots.txt`, and dark mode toggle

## Tech Stack

- **Backend**: Flask 3.0, Flask-SQLAlchemy, Flask-Login, Flask-WTF
- **Database**: SQLite (local) / PostgreSQL (production)
- **Frontend**: Bootstrap 5.3, Bootstrap Icons
- **Deployment**: Render

## Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/amruthamodela06/sanskriti-vidyalaya.git
   cd sanskriti-vidyalaya
   ```

2. Create virtual environment:
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
   python run.py
   ```

5. Open http://localhost:5000 in your browser

## Running Tests

```bash
python -m unittest discover -s tests -v
```

## Public API Endpoints

- `GET /api/v1/news` — Published news & blog posts
- `GET /api/v1/events` — Upcoming published events
- `GET /api/v1/announcements` — Active announcements
- `GET /api/v1/faculty` — Active faculty directory
- `GET /api/v1/faqs` — Active FAQs
- `GET /health` — Application & database health check
- `GET /news/feed.xml` — RSS 2.0 feed
- `GET /sitemap.xml` — Dynamic XML sitemap

## Admin Access

- URL: `/login`
- Default credentials: `admin` / `admin123`
- Change password after first login!



## Project Structure

```
sanskriti-vidyalaya/
├── app/
│   ├── models/         # Database models
│   ├── routes/         # Route handlers
│   ├── forms/          # WTForms classes
│   ├── templates/      # Jinja2 templates
│   ├── static/         # CSS, JS, images, uploads
│   └── utils/          # Helper functions
├── instance/           # SQLite database (local)
├── run.py              # Application entry point
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment config
└── build.sh            # Build script for Render
```

## License

This project is private and proprietary.
