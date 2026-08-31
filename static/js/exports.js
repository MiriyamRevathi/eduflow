// Client-Side CSV Exporter & Print Handler
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

        const csvFile = new Blob([csv.join('
')], { type: 'text/csv' });
        const downloadLink = document.createElement('a');
        downloadLink.download = filename;
        downloadLink.href = window.URL.createObjectURL(csvFile);
        downloadLink.style.display = 'none';
        document.body.appendChild(downloadLink);
        downloadLink.click();
        downloadLink.remove();
    }
});
