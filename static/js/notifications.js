// Notification center handler
document.addEventListener('DOMContentLoaded', () => {
    const badgeCount = document.getElementById('unread-notification-count');
    const notifContainer = document.getElementById('notification-list-container');
    const markAllBtn = document.getElementById('mark-all-read-btn');

    function loadNotifications() {
        fetch('/notifications/api/unread')
            .then(res => res.json())
            .then(data => {
                if (badgeCount) {
                    if (data.count > 0) {
                        badgeCount.textContent = data.count;
                        badgeCount.style.display = 'inline-block';
                    } else {
                        badgeCount.style.display = 'none';
                    }
                }

                if (notifContainer) {
                    if (data.items && data.items.length > 0) {
                        let html = '';
                        data.items.forEach(n => {
                            html += `
                                <div class="notification-item">
                                    <strong>${n.title}</strong>
                                    <div>${n.message}</div>
                                    <div class="small-text text-muted">${n.timestamp}</div>
                                </div>
                            `;
                        });
                        notifContainer.innerHTML = html;
                    } else {
                        notifContainer.innerHTML = '<div class="notification-empty p-15 text-center text-muted">No unread notifications</div>';
                    }
                }
            })
            .catch(err => console.error('Notification error:', err));
    }

    loadNotifications();

    if (markAllBtn) {
        markAllBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fetch('/notifications/api/mark-all-read', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    loadNotifications();
                });
        });
    }
});
