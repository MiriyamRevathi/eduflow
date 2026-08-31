// Weekly Timetable Interactive Grid Controller
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
