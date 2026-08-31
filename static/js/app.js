// Main Application JS entry point
document.addEventListener('DOMContentLoaded', () => {
    // Sidebar Toggle
    const sidebarToggle = document.getElementById('sidebar-toggle-btn');
    const sidebar = document.getElementById('app-sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
        });
    }

    console.log("EduFlow ERP Enterprise Application JS Engine Initialized.");

    // Keyboard Shortcuts Helper
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
            document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
        }
    });

    // Form Input Focus Effects
    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', () => {
            input.parentElement.classList.add('input-focused');
        });
        input.addEventListener('blur', () => {
            input.parentElement.classList.remove('input-focused');
        });
    });

    // Confirmation Action Buttons
    document.querySelectorAll('[data-confirm]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const msg = btn.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    // Auto-dismiss alert toasts after 5 seconds
    setTimeout(() => {
        document.querySelectorAll('.toast').forEach(toast => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        });
    }, 5000);
});
