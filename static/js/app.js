// EduFlow ERP Main Application Initialization & Global Shortcut Handler
document.addEventListener('DOMContentLoaded', () => {
    const sidebarToggle = document.getElementById('sidebar-toggle-btn');
    const sidebar = document.getElementById('app-sidebar');

    if (sidebarToggle && sidebar) {
        sidebarToggle.addEventListener('click', () => {
            sidebar.classList.toggle('collapsed');
            localStorage.setItem('eduflow_sidebar_state', sidebar.classList.contains('collapsed') ? 'collapsed' : 'expanded');
        });
        const savedState = localStorage.getItem('eduflow_sidebar_state');
        if (savedState === 'collapsed') {
            sidebar.classList.add('collapsed');
        }
    }

    console.log("EduFlow ERP Enterprise Application JS Engine Initialized.");

    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
            document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
        }
    });

    document.querySelectorAll('.form-control').forEach(input => {
        input.addEventListener('focus', () => {
            if (input.parentElement) input.parentElement.classList.add('input-focused');
        });
        input.addEventListener('blur', () => {
            if (input.parentElement) input.parentElement.classList.remove('input-focused');
        });
    });

    document.querySelectorAll('[data-confirm]').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const msg = btn.getAttribute('data-confirm') || 'Are you sure you want to perform this action?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    setTimeout(() => {
        document.querySelectorAll('.toast').forEach(toast => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        });
    }, 5000);
});
