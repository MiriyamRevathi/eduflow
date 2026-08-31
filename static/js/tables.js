// Interactive Data Tables, Column Sorting & Selection
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
