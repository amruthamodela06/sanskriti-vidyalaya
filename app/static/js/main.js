// Main JavaScript for Sanskriti Vidyalaya School Website

document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth'
                });
            }
        });
    });

    // Duplicate announcement ticker content for seamless loop
    const ticker = document.querySelector('.ticker-content');
    if (ticker) {
        ticker.innerHTML += ticker.innerHTML;
    }

    // Back to top button visibility & scroll
    const backToTopBtn = document.getElementById('backToTopBtn');
    if (backToTopBtn) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        backToTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Theme toggle with localStorage persistence
    const themeToggleBtn = document.getElementById('themeToggleBtn');
    const themeToggleIcon = document.getElementById('themeToggleIcon');
    const applyTheme = (theme) => {
        document.documentElement.setAttribute('data-bs-theme', theme);
        if (themeToggleIcon) {
            themeToggleIcon.className = theme === 'dark' ? 'bi bi-sun' : 'bi bi-moon-stars';
        }
    };
    const savedTheme = localStorage.getItem('sv_theme') || 'light';
    applyTheme(savedTheme);
    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', function() {
            const current = document.documentElement.getAttribute('data-bs-theme') === 'dark' ? 'dark' : 'light';
            const next = current === 'dark' ? 'light' : 'dark';
            localStorage.setItem('sv_theme', next);
            applyTheme(next);
        });
    }
});

// nl2br filter simulation for Jinja
// This is handled server-side, but keeping for reference
