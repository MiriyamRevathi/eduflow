// Vanilla HTML5 Canvas Charting Engine for EduFlow ERP
document.addEventListener('DOMContentLoaded', () => {
    // 1. Dashboard Trend Canvas
    const dashboardCanvas = document.getElementById('dashboard-trend-canvas');
    if (dashboardCanvas && dashboardCanvas.getContext) {
        const ctx = dashboardCanvas.getContext('2d');
        const width = dashboardCanvas.width;
        const height = dashboardCanvas.height;

        ctx.clearRect(0, 0, width, height);

        // Draw background grid lines
        ctx.strokeStyle = '#e9ecef';
        ctx.lineWidth = 1;
        for (let y = 30; y < height - 30; y += 40) {
            ctx.beginPath();
            ctx.moveTo(40, y);
            ctx.lineTo(width - 20, y);
            ctx.stroke();
        }

        // Attendance Trend Line Data
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

            // Draw point dots
            ctx.fillStyle = '#4361ee';
            ctx.beginPath();
            ctx.arc(x, y, 5, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.stroke();

        // Draw day labels
        ctx.fillStyle = '#6c757d';
        ctx.font = '12px sans-serif';
        days.forEach((day, idx) => {
            const x = 50 + idx * stepX - 10;
            ctx.fillText(day, x, height - 10);
        });
    }

    // 2. Analytics Canvas
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
