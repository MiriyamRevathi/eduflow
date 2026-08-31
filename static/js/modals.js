// Modal dialogs and backdrop interaction controller
document.addEventListener('DOMContentLoaded', () => {
    const searchTrigger = document.getElementById('open-global-search');
    const searchModal = document.getElementById('global-search-modal');
    const closeSearchBtn = document.getElementById('close-search-modal');
    const searchInput = document.getElementById('global-search-input');

    if (searchTrigger && searchModal) {
        searchTrigger.addEventListener('click', () => {
            searchModal.classList.add('active');
            if (searchInput) searchInput.focus();
        });
    }

    if (closeSearchBtn && searchModal) {
        closeSearchBtn.addEventListener('click', () => {
            searchModal.classList.remove('active');
        });
    }

    document.addEventListener('keydown', (e) => {
        if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
            e.preventDefault();
            if (searchModal) {
                searchModal.classList.toggle('active');
                if (searchModal.classList.contains('active') && searchInput) {
                    searchInput.focus();
                }
            }
        }
    });

    window.addEventListener('click', (e) => {
        if (e.target.classList.contains('modal-overlay')) {
            e.target.classList.remove('active');
        }
    });
});
