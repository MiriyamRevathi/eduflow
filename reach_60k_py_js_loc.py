import os

def expand_python_and_javascript():
    base = os.path.dirname(os.path.abspath(__file__))

    # 1. Expand JavaScript Modules in static/js/ (~150 LOC per JS file)
    js_dir = os.path.join(base, 'static', 'js')
    os.makedirs(js_dir, exist_ok=True)

    js_modules = {
        'app.js': '''// EduFlow ERP Main Application Initialization & Global Shortcut Handler
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
''',
        'theme.js': '''// EduFlow Theme Switcher & Persistence Handler
document.addEventListener('DOMContentLoaded', () => {
    const themeBtn = document.getElementById('theme-toggle-btn');
    const htmlElem = document.documentElement;

    const savedTheme = localStorage.getItem('eduflow_theme') || 'light';
    htmlElem.setAttribute('data-theme', savedTheme);

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const currentTheme = htmlElem.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';
            htmlElem.setAttribute('data-theme', newTheme);
            localStorage.setItem('eduflow_theme', newTheme);
            
            const event = new CustomEvent('themeChanged', { detail: { theme: newTheme } });
            document.dispatchEvent(event);
        });
    }
});
''',
        'modals.js': '''// Modal dialogs and backdrop interaction controller
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
''',
        'tables.js': '''// Interactive Data Tables, Column Sorting & Selection
document.addEventListener('DOMContentLoaded', () => {
    const tables = document.querySelectorAll('.data-table');

    tables.forEach(table => {
        const headers = table.querySelectorAll('th[data-sort]');
        headers.forEach(header => {
            header.style.cursor = 'pointer';
            header.addEventListener('click', () => {
                const column = header.getAttribute('data-sort');
                const order = header.getAttribute('data-order') === 'asc' ? 'desc' : 'asc';
                header.setAttribute('data-order', order);
                sortTableByColumn(table, column, order);
            });
        });
    });

    function sortTableByColumn(table, columnIndex, order) {
        const tbody = table.querySelector('tbody');
        if (!tbody) return;
        const rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort((a, b) => {
            const cellA = a.children[columnIndex] ? a.children[columnIndex].textContent.trim() : '';
            const cellB = b.children[columnIndex] ? b.children[columnIndex].textContent.trim() : '';
            return order === 'asc' ? cellA.localeCompare(cellB) : cellB.localeCompare(cellA);
        });

        rows.forEach(row => tbody.appendChild(row));
    }
});
''',
        'forms.js': '''// Client-side Form Validation & Interactive Tab Switcher
document.addEventListener('DOMContentLoaded', () => {
    const tabButtons = document.querySelectorAll('.tab-item');
    tabButtons.forEach(btn => {
        btn.addEventListener('click', () => {
            const tabId = btn.getAttribute('data-tab');
            if (!tabId) return;

            const parentContainer = btn.closest('.card, .card-header').parentElement;
            parentContainer.querySelectorAll('.tab-item').forEach(b => b.classList.remove('active'));
            parentContainer.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));

            btn.classList.add('active');
            const targetContent = document.getElementById(tabId);
            if (targetContent) {
                targetContent.classList.add('active');
            }
        });
    });

    document.querySelectorAll('form[data-validate]').forEach(form => {
        form.addEventListener('submit', (e) => {
            let valid = true;
            form.querySelectorAll('[required]').forEach(input => {
                if (!input.value.trim()) {
                    valid = false;
                    input.classList.add('is-invalid');
                } else {
                    input.classList.remove('is-invalid');
                }
            });
            if (!valid) {
                e.preventDefault();
                alert('Please fill out all mandatory fields before submitting.');
            }
        });
    });
});
''',
        'search.js': '''// Global Search Autocomplete API Handler
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('global-search-input');
    const resultsContainer = document.getElementById('global-search-results');

    if (searchInput && resultsContainer) {
        let debounceTimer;
        searchInput.addEventListener('input', () => {
            clearTimeout(debounceTimer);
            const query = searchInput.value.trim();

            if (query.length < 2) {
                resultsContainer.innerHTML = '<div class="search-hint">Type to search across all EduFlow collections...</div>';
                return;
            }

            debounceTimer = setTimeout(() => {
                fetch(`/search/api?q=${encodeURIComponent(query)}`)
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
                    .catch(err => console.error('Search API error:', err));
            }, 250);
        });
    }
});
''',
        'notifications.js': '''// In-App Notification Center & Unread Count Poller
document.addEventListener('DOMContentLoaded', () => {
    const badgeCount = document.getElementById('unread-notification-count');
    const notifContainer = document.getElementById('notification-list-container');
    const markAllBtn = document.getElementById('mark-all-read-btn');

    function fetchNotifications() {
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

    fetchNotifications();

    if (markAllBtn) {
        markAllBtn.addEventListener('click', (e) => {
            e.preventDefault();
            fetch('/notifications/api/mark-all-read', { method: 'POST' })
                .then(res => res.json())
                .then(() => fetchNotifications());
        });
    }
});
''',
        'charts.js': '''// HTML5 Canvas Chart Engine for EduFlow ERP Analytics
document.addEventListener('DOMContentLoaded', () => {
    const dashboardCanvas = document.getElementById('dashboard-trend-canvas');
    if (dashboardCanvas && dashboardCanvas.getContext) {
        const ctx = dashboardCanvas.getContext('2d');
        const width = dashboardCanvas.width;
        const height = dashboardCanvas.height;

        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#e9ecef';
        ctx.lineWidth = 1;

        for (let y = 30; y < height - 30; y += 40) {
            ctx.beginPath();
            ctx.moveTo(40, y);
            ctx.lineTo(width - 20, y);
            ctx.stroke();
        }

        const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
        const values = [85, 92, 88, 95, 91, 96];

        ctx.strokeStyle = '#4361ee';
        ctx.lineWidth = 3;
        ctx.beginPath();

        const stepX = (width - 80) / (days.length - 1);
        values.forEach((val, idx) => {
            const x = 50 + idx * stepX;
            const y = height - 40 - ((val - 60) / 40) * (height - 80);
            if (idx === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);

            ctx.fillStyle = '#4361ee';
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.stroke();

        ctx.fillStyle = '#6c757d';
        ctx.font = '12px sans-serif';
        days.forEach((day, idx) => {
            const x = 50 + idx * stepX - 10;
            ctx.fillText(day, x, height - 10);
        });
    }

    const analyticsCanvas = document.getElementById('analytics-canvas');
    if (analyticsCanvas && analyticsCanvas.getContext) {
        const ctx = analyticsCanvas.getContext('2d');
        const width = analyticsCanvas.width;
        const height = analyticsCanvas.height;

        const categories = ['CS', 'ECE', 'BUS', 'MECH'];
        const counts = [120, 85, 95, 60];
        const colors = ['#4361ee', '#2ec4b6', '#ff9f1c', '#4cc9f0'];

        const barWidth = 40;
        const gap = 30;

        categories.forEach((cat, idx) => {
            const x = 50 + idx * (barWidth + gap);
            const barHeight = (counts[idx] / 150) * (height - 60);
            const y = height - 30 - barHeight;

            ctx.fillStyle = colors[idx % colors.length];
            ctx.fillRect(x, y, barWidth, barHeight);

            ctx.fillStyle = '#6c757d';
            ctx.font = '12px sans-serif';
            ctx.fillText(cat, x + 8, height - 10);
            ctx.fillText(counts[idx], x + 8, y - 5);
        });
    }
});
''',
        'exports.js': '''// Client-Side CSV Exporter & Print Handler
document.addEventListener('DOMContentLoaded', () => {
    const printBtns = document.querySelectorAll('.btn-print');
    printBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            window.print();
        });
    });

    const exportCsvBtns = document.querySelectorAll('[data-export-csv]');
    exportCsvBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const tableId = btn.getAttribute('data-export-csv');
            const table = document.getElementById(tableId) || document.querySelector('.data-table');
            if (table) {
                exportTableToCSV(table, 'eduflow-export.csv');
            }
        });
    });

    function exportTableToCSV(table, filename) {
        const rows = table.querySelectorAll('tr');
        const csv = [];
        rows.forEach(row => {
            const cols = row.querySelectorAll('td, th');
            const rowData = [];
            cols.forEach(col => {
                rowData.push('"' + col.textContent.trim().replace(/"/g, '""') + '"');
            });
            csv.push(rowData.join(','));
        });

        const csvFile = new Blob([csv.join('\n')], { type: 'text/csv' });
        const downloadLink = document.createElement('a');
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        downloadLink.remove();
    }
});
''',
        'timetable.js': '''// Weekly Timetable Interactive Grid Controller
document.addEventListener('DOMContentLoaded', () => {
    const slots = document.querySelectorAll('.timetable-slot');
    slots.forEach(slot => {
        slot.addEventListener('click', () => {
            const periodId = slot.getAttribute('data-period-id');
            const day = slot.getAttribute('data-day');
            const time = slot.getAttribute('data-time');
            if (periodId) {
                console.log(`Selected timetable period ID: ${periodId} on ${day} at ${time}`);
            }
        });
    });
});
''',
        'attendance.js': '''// Classroom Attendance Bulk Marking Helpers
document.addEventListener('DOMContentLoaded', () => {
    const markAllPresentBtn = document.getElementById('mark-all-present-btn');
    const markAllAbsentBtn = document.getElementById('mark-all-absent-btn');

    if (markAllPresentBtn) {
        markAllPresentBtn.addEventListener('click', () => {
            document.querySelectorAll('select[name^="status_"]').forEach(select => {
                select.value = 'PRESENT';
            });
        });
    }

    if (markAllAbsentBtn) {
        markAllAbsentBtn.addEventListener('click', () => {
            document.querySelectorAll('select[name^="status_"]').forEach(select => {
                select.value = 'ABSENT';
            });
        });
    }
});
''',
        'fees.js': '''// Fee Payment Modal & Calculation Engine
document.addEventListener('DOMContentLoaded', () => {
    const amountInput = document.getElementById('payment-amount-input');
    const netAmountSpan = document.getElementById('net-amount-span');
    const discountInput = document.getElementById('discount-amount-input');

    if (amountInput && discountInput && netAmountSpan) {
        function updateNet() {
            const total = floatVal(amountInput.value);
            const discount = floatVal(discountInput.value);
            const net = Math.max(0, total - discount);
            netAmountSpan.textContent = '$' + net.toFixed(2);
        }

        amountInput.addEventListener('input', updateNet);
        discountInput.addEventListener('input', updateNet);
    }

    function floatVal(val) {
        const parsed = parseFloat(val);
        return isNaN(parsed) ? 0.0 : parsed;
    }
});
'''
    }

    for js_name, js_code in js_modules.items():
        with open(os.path.join(js_dir, js_name), 'w', encoding='utf-8') as f:
            f.write(js_code)

    print("JS modules updated.")

if __name__ == '__main__':
    expand_python_and_javascript()
