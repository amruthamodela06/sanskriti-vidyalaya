from flask import Flask, render_template, jsonify
from sqlalchemy import text
from app.extensions import db, login_manager, migrate, csrf
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    # Configure login
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Register blueprints
    from app.routes.public import public_bp
    from app.routes.admin import admin_bp
    from app.routes.auth import auth_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp)

    # User loader for Flask-Login
    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Context processor for templates
    @app.context_processor
    def inject_settings():
        from app.models.settings import Setting
        from datetime import datetime
        try:
            settings = {s.key: s.value for s in Setting.query.all()}
        except:
            settings = {}
        return dict(site_settings=settings, current_year=datetime.now().year)

    # Custom Jinja2 template filters
    import re
    from markupsafe import Markup, escape

    @app.template_filter('striptags_truncate')
    def striptags_truncate(value, length=120):
        if not value:
            return ''
        clean = re.sub(r'<[^>]+>', '', str(value)).strip()
        if len(clean) <= length:
            return clean
        return clean[:length].rsplit(' ', 1)[0] + '...'

    @app.template_filter('reading_time')
    def reading_time(value):
        if not value:
            return '1 min read'
        clean = re.sub(r'<[^>]+>', '', str(value))
        words = len(clean.split())
        minutes = max(1, round(words / 200))
        return f"{minutes} min read"

    @app.template_filter('nl2br')
    def nl2br(value):
        if not value:
            return ''
        return Markup('<br>'.join(escape(str(value)).splitlines()))

    # Error handlers
    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('errors/403.html'), 403

    @app.errorhandler(413)
    def payload_too_large_error(error):
        return render_template('errors/403.html', message="The uploaded file exceeds the maximum allowed size (16MB)."), 413

    @app.route('/health')
    def health_check():
        """Lightweight health check endpoint verifying database connectivity."""
        try:
            db.session.execute(text('SELECT 1'))
            return jsonify({'status': 'healthy', 'database': 'connected'}), 200
        except Exception:
            return jsonify({'status': 'unhealthy', 'database': 'disconnected'}), 503

    # Security headers
    @app.after_request
    def set_security_headers(response):
        response.headers.setdefault('X-Content-Type-Options', 'nosniff')
        response.headers.setdefault('X-Frame-Options', 'SAMEORIGIN')
        response.headers.setdefault('Referrer-Policy', 'strict-origin-when-cross-origin')
        response.headers.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')
        return response

    # Create tables
    with app.app_context():
        db.create_all()

    return app
