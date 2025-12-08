# Sanskriti Vidyalaya

A school website built with Flask.

## Features

- **Public Pages**: Home, About, Academics, Admissions, Faculty, Events, News, Gallery, Contact
- **Admin Panel**: Dashboard with full content management
- **Staff Management**: Add and manage faculty members
- **Blog/News**: Create and publish news articles
- **Events & Holidays**: Manage school events and holiday calendar
- **Gallery**: Photo albums with image uploads
- **Timetables**: Upload class timetables
- **Announcements**: Scrolling announcements on homepage
- **Admission Inquiries**: Online admission inquiry form
- **Contact Messages**: Receive and manage contact form submissions
- **Site Settings**: Customize school name, contact info, social links

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
