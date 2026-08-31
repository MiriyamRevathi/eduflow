// Form client validation & tab switching
document.addEventListener('DOMContentLoaded', () => {
    // Interactive Tab Switching
    const tabButtons = document.querySelectorAll('.tab-item');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            if (!tabId) return;

            // Deactivate siblings
            const parentNav = btn.closest('.card, .card-header').parentElement;
            parentNav.querySelectorAll('.tab-item').forEach(b => b.classList.remove('active'));
            parentNav.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    // Toast Dismiss Buttons
    document.querySelectorAll('.toast-close-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            btn.closest('.toast').remove();
        });
    });
});
