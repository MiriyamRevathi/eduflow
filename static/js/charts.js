// HTML5 Canvas Chart Engine for EduFlow ERP Super Admin Dashboard Analytics
document.addEventListener('DOMContentLoaded', () => {

    window.renderDashboardCharts = function(period = 'this_month') {
        renderStudentGrowthChart(period);
        renderFeeCollectionChart(period);
        renderAttendanceDonutChart(period);
        renderInstitutionCompareChart(period);
    };

    function renderStudentGrowthChart(period) {
        const canvas = document.getElementById('dashboard-student-growth-canvas');
        if (!canvas || !canvas.getContext) return;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        ctx.clearRect(0, 0, width, height);
        ctx.strokeStyle = '#e2e8f0';
        ctx.lineWidth = 1;

        // Grid lines
        for (let y = 30; y < height - 30; y += 40) {
            ctx.beginPath();
            ctx.moveTo(40, y);
            ctx.lineTo(width - 20, y);
            ctx.stroke();
        }

        const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug'];
        let values = [38200, 39500, 41000, 42100, 43500, 44200, 44800, 45280];

        if (period === 'today') {
            values = [45100, 45150, 45180, 45210, 45240, 45260, 45275, 45280];
        } else if (period === 'this_week') {
            values = [44900, 44950, 45020, 45100, 45180, 45240, 45260, 45280];
        }

        ctx.strokeStyle = '#2563eb';
        ctx.lineWidth = 3;
        ctx.beginPath();

        const stepX = (width - 80) / (months.length - 1);
        const minVal = 35000;
        const maxVal = 48000;

        values.forEach((val, idx) => {
            const x = 50 + idx * stepX;
            const y = height - 40 - ((val - minVal) / (maxVal - minVal)) * (height - 80);
            if (idx === 0) ctx.moveTo(x, y);
            else ctx.lineTo(x, y);

            // Draw data points
            ctx.fillStyle = '#2563eb';
            ctx.beginPath();
            ctx.arc(x, y, 4, 0, Math.PI * 2);
            ctx.fill();
        });
        ctx.stroke();

        ctx.fillStyle = '#64748b';
        ctx.font = '11px sans-serif';
        months.forEach((m, idx) => {
            const x = 50 + idx * stepX - 10;
            ctx.fillText(m, x, height - 10);
        });
    }

    function renderFeeCollectionChart(period) {
        const canvas = document.getElementById('dashboard-fee-collection-canvas');
        if (!canvas || !canvas.getContext) return;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        ctx.clearRect(0, 0, width, height);

        const categories = ['Q1', 'Q2', 'Q3', 'Q4'];
        const collected = [3.2, 3.8, 3.6, 3.6];
        const pending = [0.4, 0.5, 0.45, 0.5];

        const barWidth = 45;
        const gap = 55;

        categories.forEach((cat, idx) => {
            const x = 60 + idx * (barWidth + gap);
            const collH = (collected[idx] / 5.0) * (height - 60);
            const pendH = (pending[idx] / 5.0) * (height - 60);

            // Collected Bar (Green)
            const yColl = height - 30 - collH;
            ctx.fillStyle = '#10b981';
            ctx.fillRect(x, yColl, barWidth, collH);

            // Pending Bar (Red/Orange) stacked above
            const yPend = yColl - pendH;
            ctx.fillStyle = '#f59e0b';
            ctx.fillRect(x, yPend, barWidth, pendH);

            ctx.fillStyle = '#64748b';
            ctx.font = '12px sans-serif';
            ctx.fillText(cat, x + 12, height - 10);
            ctx.fillText('$' + collected[idx] + 'M', x + 4, yColl + 20);
        });
    }

    function renderAttendanceDonutChart(period) {
        const canvas = document.getElementById('dashboard-attendance-donut-canvas');
        if (!canvas || !canvas.getContext) return;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;
        const centerX = width / 2;
        const centerY = height / 2;
        const outerRadius = 75;
        const innerRadius = 50;

        ctx.clearRect(0, 0, width, height);

        const data = [
            { label: 'Present', pct: 0.942, color: '#10b981' },
            { label: 'Absent', pct: 0.041, color: '#ef4444' },
            { label: 'Leave', pct: 0.017, color: '#f59e0b' }
        ];

        let startAngle = -Math.PI / 2;

        data.forEach(item => {
            const sliceAngle = item.pct * Math.PI * 2;
            ctx.beginPath();
            ctx.arc(centerX, centerY, outerRadius, startAngle, startAngle + sliceAngle);
            ctx.arc(centerX, centerY, innerRadius, startAngle + sliceAngle, startAngle, true);
            ctx.closePath();
            ctx.fillStyle = item.color;
            ctx.fill();
            startAngle += sliceAngle;
        });

        ctx.fillStyle = '#0f172a';
        ctx.font = 'bold 20px sans-serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText('94.2%', centerX, centerY - 8);
        ctx.font = '10px sans-serif';
        ctx.fillStyle = '#64748b';
        ctx.fillText('Attendance', centerX, centerY + 12);
    }

    function renderInstitutionCompareChart(period) {
        const canvas = document.getElementById('dashboard-institution-compare-canvas');
        if (!canvas || !canvas.getContext) return;
        const ctx = canvas.getContext('2d');
        const width = canvas.width;
        const height = canvas.height;

        ctx.clearRect(0, 0, width, height);

        const insts = [
            { name: 'Trinity Global', students: 12400, color: '#2563eb' },
            { name: 'St. Xavier Univ', students: 8420, color: '#3b82f6' },
            { name: 'Apex Tech', students: 3250, color: '#60a5fa' },
            { name: 'Horizon Arts', students: 2100, color: '#93c5fd' },
            { name: 'Pacific Mgmt', students: 1850, color: '#a5b4fc' }
        ];

        const barHeight = 22;
        const startY = 20;

        insts.forEach((inst, idx) => {
            const y = startY + idx * (barHeight + 14);
            const barW = (inst.students / 13000) * (width - 160);

            ctx.fillStyle = '#475569';
            ctx.font = '11px sans-serif';
            ctx.textAlign = 'left';
            ctx.fillText(inst.name, 10, y + 15);

            ctx.fillStyle = inst.color;
            ctx.fillRect(110, y, barW, barHeight);

            ctx.fillStyle = '#0f172a';
            ctx.font = 'bold 11px sans-serif';
            ctx.fillText(inst.students.toLocaleString(), 120 + barW, y + 15);
        });
    }

    // Initial render
    window.renderDashboardCharts();
});
