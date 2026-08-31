// Printable & Exports handler
document.addEventListener('DOMContentLoaded', () => {
    // Print button triggers
    const printBtns = document.querySelectorAll('.btn-print');
    printBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            window.print();
        });
    });
});
