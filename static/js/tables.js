// Table interactive sorting and row selection
document.addEventListener('DOMContentLoaded', () => {
    // Dropdown Toggles (User menu & Notifications)
    const userMenuBtn = document.getElementById('user-menu-btn');
    const userMenu = document.getElementById('user-menu');

    if (userMenuBtn && userMenu) {
        userMenuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            userMenu.classList.toggle('active');
        });
    }

    const notifBtn = document.getElementById('notifications-btn');
    const notifMenu = document.getElementById('notification-menu');

    if (notifBtn && notifMenu) {
        notifBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            notifMenu.classList.toggle('active');
        });
    }

    document.addEventListener('click', () => {
        if (userMenu) userMenu.classList.remove('active');
        if (notifMenu) notifMenu.classList.remove('active');
    });
});
