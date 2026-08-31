// Global search autocomplete handler
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('global-search-input');
    const resultsContainer = document.getElementById('global-search-results');

    if (searchInput && resultsContainer) {
        let debounceTimer;
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            const q = searchInput.value.trim();

            if (q.length < 2) {
                resultsContainer.innerHTML = '<div class="search-hint">Start typing to search across all EduFlow collections...</div>';
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/search/api?q=${encodeURIComponent(q)}`)
                    .then(res => res.json())
                    .then(data => {
                        if (data.results && data.results.length > 0) {
                            let html = '';
                            data.results.forEach(item => {
                                html += `
                                    <a href="${item.url}" class="search-item">
                                        <span class="badge badge-primary">${item.category}</span>
                                        <strong>${item.title}</strong>
                                        <div class="small-text text-muted">${item.subtitle}</div>
                                    </a>
                                `;
                            });
                            resultsContainer.innerHTML = html;
                        } else {
                            resultsContainer.innerHTML = '<div class="search-hint text-muted">No records found matching query.</div>';
                        }
                    })
                    .catch(err => {
                        console.error('Search API error:', err);
                    });
            }, 250);
        });
    }
});
