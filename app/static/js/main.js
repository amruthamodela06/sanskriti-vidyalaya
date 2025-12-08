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
});

// nl2br filter simulation for Jinja
// This is handled server-side, but keeping for reference
