// Classroom Attendance Bulk Marking Helpers
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
