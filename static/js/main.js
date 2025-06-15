document.addEventListener('DOMContentLoaded', function() {
    const themeToggle = document.getElementById('themeToggle');
    const themeIcon = themeToggle.querySelector('i');
    const html = document.documentElement;

    const savedTheme = localStorage.getItem('theme') || 'light';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    themeToggle.addEventListener('click', () => {
        const currentTheme = html.getAttribute('data-theme');
        const newTheme = currentTheme === 'light' ? 'dark' : 'light';
        
        html.setAttribute('data-theme', newTheme);
        localStorage.setItem('theme', newTheme);
        updateThemeIcon(newTheme);
    });

    function updateThemeIcon(theme) {
        themeIcon.className = theme === 'dark' ? 'fas fa-sun' : 'fas fa-moon';
    }
});

function checkNotifications() {
    fetch('/get-notification-count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.notification-count');
            if (data.count > 0) {
                if (!badge) {
                    const notificationLink = document.querySelector('.notification-badge .nav-link');
                    const newBadge = document.createElement('span');
                    newBadge.className = 'notification-count';
                    newBadge.textContent = data.count;
                    notificationLink.appendChild(newBadge);
                } else {
                    badge.textContent = data.count;
                    badge.style.display = 'inline';
                }
            } else if (badge) {
                badge.style.display = 'none';
            }
        })
        .catch(error => console.error('Error checking notifications:', error));
}

if (document.querySelector('.notification-badge')) {
    checkNotifications();
    setInterval(checkNotifications, 30000);
} 