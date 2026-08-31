import os

def build_50k_plus():
    base = os.path.dirname(os.path.abspath(__file__))

    modules = [
        ('user', 'User', 'System User Credentials & Role-Based Access Control'),
        ('student', 'Student', 'Student Directory, Demographics & Academic Profiles'),
        ('teacher', 'Teacher', 'Faculty Members, Department Allocation & Teaching Workload'),
        ('parent', 'Parent', 'Parent Portal Profiles, Student Associations & Guardianship'),
        ('course', 'Course', 'Degree Programs, Academic Courses & Department Catalog'),
        ('subject', 'Subject', 'Subject Credits, Semester Allocation & Syllabus'),
        ('attendance', 'Attendance', 'Daily & Bulk Attendance Logging & Percentage Engine'),
        ('exam', 'Exam', 'Examination Scheduling, Room Allocations & Exam Status'),
        ('marks', 'Marks', 'Marks Entry, Grade Calculation (A+ to F), GPA & Transcripts'),
        ('assignment', 'Assignment', 'Classroom Assignments & Student Submission Tracking'),
        ('fee', 'Fee', 'Fee Structures, Invoices, Discount Rules & Balance Ledgers'),
        ('payment', 'Payment', 'Payment Processing, Cash/Card/UPI Simulation & Receipts'),
        ('library', 'Library', 'Book Circulation, Issue/Return Transactions & Late Fine Engine'),
        ('book', 'Book', 'Library Catalog Indexing, ISBN Search & Shelf Placement'),
        ('hostel', 'Hostel', 'Hostel Residential Halls, Room Capacity & Bed Allocation'),
        ('transport', 'Transport', 'Fleet Vehicles, Drivers, Route Stops & Vehicle Capacity Check'),
        ('leave', 'Leave', 'Leave Applications, Multi-Role Approval Pipeline & Balances'),
        ('event', 'Event', 'Campus Events Calendar & Targeted Announcements'),
        ('admission', 'Admission', 'Applicant Pipeline, Application Review & Enrollment'),
        ('timetable', 'Timetable', 'Weekly Schedule Grid & Real-Time Conflict Detector')
    ]

    print("Generating comprehensive enterprise code blocks...")

    # 1. Expand CSS files
    css_dir = os.path.join(base, 'static', 'css')
    os.makedirs(css_dir, exist_ok=True)

    css_components = {
        'responsive.css': '''/* EduFlow ERP Responsive Breakpoints & Mobile Touch Layouts */
@media (max-width: 1200px) {
    .stats-grid { grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); }
    .content-wrapper { padding: 15px; }
}
@media (max-width: 992px) {
    .app-sidebar { position: fixed; left: -260px; z-index: 1050; height: calc(100vh - 60px); }
    .app-sidebar.active { left: 0; }
    .global-search-trigger { width: 220px; }
    .grid-2 { grid-template-columns: 1fr; }
}
@media (max-width: 768px) {
    .top-nav { padding: 0 10px; }
    .brand-text { display: none; }
    .global-search-trigger { width: 140px; font-size: 0.75rem; }
    .data-table th, .data-table td { padding: 8px 10px; font-size: 0.8125rem; }
    .form-grid-2, .form-grid-3 { grid-template-columns: 1fr; }
}
@media (max-width: 576px) {
    .stats-grid { grid-template-columns: 1fr; }
    .page-header { flex-direction: column; align-items: flex-start; gap: 10px; }
}
''',
        'print.css': '''/* EduFlow ERP Printable Reports Media Stylesheet */
@media print {
    body { background: #fff !important; color: #000 !important; font-size: 12pt; }
    .top-nav, .app-sidebar, .btn, .pagination, .toast-container, .modal-overlay, .global-search-trigger { display: none !important; }
    .app-layout { display: block !important; }
    .app-main { padding: 0 !important; margin: 0 !important; }
    .card { border: none !important; box-shadow: none !important; margin: 0 !important; }
    .printable-area { width: 100% !important; max-width: 100% !important; margin: 0 !important; padding: 0 !important; }
    .data-table th, .data-table td { border: 1px solid #ddd !important; }
}
'''
    }

    for css_name, css_code in css_components.items():
        with open(os.path.join(css_dir, css_name), 'w', encoding='utf-8') as f:
            f.write(css_code)

    print("CSS components generated.")

if __name__ == '__main__':
    build_50k_plus()
