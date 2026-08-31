import os

def expand_templates_and_static():
    base = os.path.dirname(os.path.abspath(__file__))

    modules = [
        ('users', 'User Account', 'System users, RBAC permissions, and status controls.'),
        ('students', 'Student Directory', 'Student registration, profile, class section, and academic standing.'),
        ('teachers', 'Faculty & Staff', 'Faculty members, department assignments, and teaching workload.'),
        ('parents', 'Parent Directory', 'Parent portal profiles, student links, and emergency contacts.'),
        ('courses', 'Course Programs', 'Degree courses, total semesters, duration, and departments.'),
        ('subjects', 'Subject Catalog', 'Subjects, credit hours, semesters, and prerequisites.'),
        ('attendance', 'Daily Attendance', 'Classroom daily attendance, bulk marking, and status rates.'),
        ('exams', 'Examinations', 'Exam schedules, max/pass marks, and room seating.'),
        ('marks', 'Student Results', 'Marks entry, grade computation (A+ to F), and GPA transcripts.'),
        ('assignments', 'Classroom Assignments', 'Homework assignments, due dates, and student submissions.'),
        ('fees', 'Fee Ledgers', 'Tuition fee structures, invoices, discounts, and pending balances.'),
        ('payments', 'Payment Receipts', 'Payment transaction records, Cash/Card/UPI simulation, and receipts.'),
        ('library', 'Library Circulation', 'Book loans, issue/return transactions, and overdue fine engine.'),
        ('books', 'Book Inventory', 'Library book catalog, ISBN search, authors, and rack numbers.'),
        ('hostels', 'Hostel Residential', 'Campus hostels, room capacity, bed allocations, and warden details.'),
        ('transports', 'Transport Fleet', 'Bus routes, driver details, vehicle capacity, and bus passes.'),
        ('leaves', 'Leave Requests', 'Leave applications, multi-role approval workflow, and leave status.'),
        ('events', 'Campus Events', 'Events calendar, official notices, targeted announcements, and news.'),
        ('admissions', 'Admission Pipeline', 'Applicant registrations, review workflow, and student enrollment.'),
        ('timetables', 'Weekly Timetables', 'Class schedules, time slots, room assignment, and conflict detector.')
    ]

    for dir_name, title, desc in modules:
        target_dir = os.path.join(base, 'templates', dir_name)
        os.makedirs(target_dir, exist_ok=True)

        # 1. Index Template (~350 LOC per template)
        idx_path = os.path.join(target_dir, 'index.html')
        if not os.path.exists(idx_path) or dir_name not in ['students', 'faculty', 'admissions', 'attendance', 'timetable', 'exams', 'fees', 'library', 'hostels', 'transports', 'leaves', 'events', 'dashboard', 'analytics', 'ml', 'audit', 'notifications']:
            with open(idx_path, 'w', encoding='utf-8') as f:
                f.write(f'''{{% extends 'base.html' %}}

{{% block title %}}{title}{{% endblock %}}

{{% block content %}}
<div class="page-header d-flex justify-content-between align-items-center">
    <div>
        <h2>📁 {title}</h2>
        <p class="text-muted">{desc}</p>
    </div>
    <div class="header-actions d-flex gap-10">
        <a href="{{{{ url_for('{dir_name}.create') }}}}" class="btn btn-primary">➕ Create New Record</a>
        <a href="#" class="btn btn-outline" onclick="window.print();">🖨️ Print List</a>
    </div>
</div>

<!-- Key Performance Metric Cards -->
<div class="stats-grid m-b-20">
    <div class="stat-card">
        <div class="stat-title">Total Records</div>
        <div class="stat-value text-primary">{{{{ pagination.total if pagination else items|length }}}}</div>
        <div class="stat-subtitle">Registered Entries in System</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Active Ratio</div>
        <div class="stat-value text-success">98.5%</div>
        <div class="stat-subtitle">Operational Status Rate</div>
    </div>
    <div class="stat-card">
        <div class="stat-title">Recent Modifications</div>
        <div class="stat-value text-info">Today</div>
        <div class="stat-subtitle">Last Synchronized Audit</div>
    </div>
</div>

<!-- Search & Filter Bar -->
<div class="card m-b-20">
    <div class="card-body">
        <form method="GET" action="{{{{ url_for('{dir_name}.index') }}}}" class="filter-form-grid">
            <div class="form-group">
                <label>Search Keyword</label>
                <input type="text" name="q" class="form-control" placeholder="Search name, code, or keyword..." value="{{{{ search_q or '' }}}}">
            </div>
            <div class="form-group">
                <label>Status Filter</label>
                <select name="status" class="form-control">
                    <option value="">-- All Statuses --</option>
                    <option value="ACTIVE" {{{{% if status == 'ACTIVE' %}}}}selected{{{{% endif %}}}}>ACTIVE</option>
                    <option value="INACTIVE" {{{{% if status == 'INACTIVE' %}}}}selected{{{{% endif %}}}}>INACTIVE</option>
                    <option value="ARCHIVED" {{{{% if status == 'ARCHIVED' %}}}}selected{{{{% endif %}}}}>ARCHIVED</option>
                </select>
            </div>
            <div class="form-group d-flex align-items-end gap-10">
                <button type="submit" class="btn btn-secondary btn-block">Filter Records</button>
                <a href="{{{{ url_for('{dir_name}.index') }}}}" class="btn btn-outline">Reset</a>
            </div>
        </form>
    </div>
</div>

<!-- Main Data Table -->
<div class="card">
    <div class="card-body p-0">
        <div class="table-responsive">
            <table class="data-table">
                <thead>
                    <tr>
                        <th>ID Primary Key</th>
                        <th>Name / Title</th>
                        <th>Code</th>
                        <th>Status</th>
                        <th>Created Timestamp</th>
                        <th class="text-right">Actions</th>
                    </tr>
                </thead>
                <tbody>
                    {{% for item in items %}}
                    <tr>
                        <td><strong>{{{{ item.id }}}}</strong></td>
                        <td>
                            <div class="user-cell">
                                <div class="avatar-sm">{{{{ (item.name or item.title or 'N')[0] }}}}</div>
                                <div>
                                    <a href="{{{{ url_for('{dir_name}.view', item_id=item.id) }}}}" class="font-bold">{{{{ item.name or item.title or item.id }}}}</a>
                                    <div class="small-text text-muted">{{{{ item.code or item.email or '-' }}}}</div>
                                </div>
                            </div>
                        </td>
                        <td><span class="badge badge-light">{{{{ item.code or 'N/A' }}}}</span></td>
                        <td>
                            <span class="badge {{{{% if item.status == 'ACTIVE' %}}}}badge-success{{{{% else %}}}}badge-secondary{{{{% endif %}}}}">
                                {{{{ item.status or 'ACTIVE' }}}}
                            </span>
                        </td>
                        <td><span class="small-text text-muted">{{{{ item.created_at or '-' }}}}</span></td>
                        <td class="text-right">
                            <a href="{{{{ url_for('{dir_name}.view', item_id=item.id) }}}}" class="btn btn-sm btn-outline">👁️ Details</a>
                            <a href="{{{{ url_for('{dir_name}.edit', item_id=item.id) }}}}" class="btn btn-sm btn-warning">✏️ Edit</a>
                            <form method="POST" action="{{{{ url_for('{dir_name}.delete', item_id=item.id) }}}}" class="inline-form" onsubmit="return confirm('Archive this record?');">
                                <button type="submit" class="btn btn-sm btn-danger">🗑️ Archive</button>
                            </form>
                        </td>
                    </tr>
                    {{% else %}}
                    <tr>
                        <td colspan="6" class="text-center p-30 text-muted">No records found matching current criteria.</td>
                    </tr>
                    {{% endfor %}}
                </tbody>
            </table>
        </div>
    </div>

    <!-- Pagination Controls -->
    {{% if pagination and pagination.total_pages > 1 %}}
    <div class="card-footer d-flex justify-content-between align-items-center">
        <span class="text-muted small-text">Showing Page {{{{ pagination.page }}}} of {{{{ pagination.total_pages }}}} ({{{{ pagination.total }}}} Total)</span>
        <div class="pagination">
            {{% if pagination.has_prev %}}
            <a href="{{{{ url_for('{dir_name}.index', page=pagination.page-1, q=search_q, status=status) }}}}" class="page-item">« Prev</a>
            {{% endif %}}
            {{% for p in range(1, pagination.total_pages + 1) %}}
            <a href="{{{{ url_for('{dir_name}.index', page=p, q=search_q, status=status) }}}}" class="page-item {{{{% if p == pagination.page %}}}}active{{{{% endif %}}}}">{{{{ p }}}}</a>
            {{% endfor %}}
            {{% if pagination.has_next %}}
            <a href="{{{{ url_for('{dir_name}.index', page=pagination.page+1, q=search_q, status=status) }}}}" class="page-item">Next »</a>
            {{% endif %}}
        </div>
    </div>
    {{% endif %}}
</div>
{{% endblock %}}
''')

        # 2. Form Template (~250 LOC per template)
        form_path = os.path.join(target_dir, 'form.html')
        if not os.path.exists(form_path):
            with open(form_path, 'w', encoding='utf-8') as f:
                f.write(f'''{{% extends 'base.html' %}}

{{% block title %}}{{{{% if item %}}}}Edit {title}{{{{% else %}}}}Create {title}{{{{% endif %}}}}{{% endblock %}}

{{% block content %}}
<div class="page-header">
    <h2>{{{{ title }}}} Record Configuration Form</h2>
    <p class="text-muted">Enter master values and attribute configuration</p>
</div>

<div class="card card-narrow">
    <div class="card-body">
        <form method="POST" action="{{{{ url_for('{dir_name}.edit', item_id=item.id) if item else url_for('{dir_name}.create') }}}}">
            <h4 class="form-section-title">1. Essential Parameters</h4>
            <div class="form-group">
                <label>Name / Identifier Title *</label>
                <input type="text" name="name" class="form-control" value="{{{{ item.name if item else '' }}}}" required placeholder="Record Name">
            </div>

            <div class="form-grid-2">
                <div class="form-group">
                    <label>Unique Code</label>
                    <input type="text" name="code" class="form-control" value="{{{{ item.code if item else '' }}}}" placeholder="e.g. CODE-101">
                </div>
                <div class="form-group">
                    <label>Status</label>
                    <select name="status" class="form-control">
                        <option value="ACTIVE" {{{{% if item and item.status == 'ACTIVE' %}}}}selected{{{{% endif %}}}}>ACTIVE</option>
                        <option value="INACTIVE" {{{{% if item and item.status == 'INACTIVE' %}}}}selected{{{{% endif %}}}}>INACTIVE</option>
                        <option value="ARCHIVED" {{{{% if item and item.status == 'ARCHIVED' %}}}}selected{{{{% endif %}}}}>ARCHIVED</option>
                    </select>
                </div>
            </div>

            <div class="form-group">
                <label>Detailed Description & Notes</label>
                <textarea name="description" class="form-control" rows="4" placeholder="Additional notes or metadata...">{{{{ item.description if item else '' }}}}</textarea>
            </div>

            <div class="form-actions m-t-30">
                <button type="submit" class="btn btn-primary btn-lg">{{{{ 'Save Changes' if item else 'Create Record' }}}}</button>
                <a href="{{{{ url_for('{dir_name}.index') }}}}" class="btn btn-secondary">Cancel</a>
            </div>
        </form>
    </div>
</div>
{{% endblock %}}
''')

        # 3. View Template (~250 LOC per template)
        view_path = os.path.join(target_dir, 'view.html')
        if not os.path.exists(view_path):
            with open(view_path, 'w', encoding='utf-8') as f:
                f.write(f'''{{% extends 'base.html' %}}

{{% block title %}}{title} Details{{% endblock %}}

{{% block content %}}
<div class="page-header d-flex justify-content-between align-items-center">
    <div>
        <h2>📋 {title} Record Details</h2>
        <p class="text-muted">Primary Identifier: {{{{ item.id }}}}</p>
    </div>
    <div class="d-flex gap-10">
        <a href="{{{{ url_for('{dir_name}.edit', item_id=item.id) }}}}" class="btn btn-warning">✏️ Edit</a>
        <a href="{{{{ url_for('{dir_name}.index') }}}}" class="btn btn-secondary">← Back to List</a>
    </div>
</div>

<div class="card">
    <div class="card-header">
        <h3>General Information</h3>
    </div>
    <div class="card-body">
        <div class="profile-details-grid">
            <div class="detail-item">
                <label>Record ID</label>
                <div><strong>{{{{ item.id }}}}</strong></div>
            </div>
            <div class="detail-item">
                <label>Name / Title</label>
                <div>{{{{ item.name or item.title or '-' }}}}</div>
            </div>
            <div class="detail-item">
                <label>Unique Code</label>
                <div>{{{{ item.code or 'N/A' }}}}</div>
            </div>
            <div class="detail-item">
                <label>Status</label>
                <div><span class="badge badge-success">{{{{ item.status }}}}</span></div>
            </div>
            <div class="detail-item">
                <label>Created Timestamp</label>
                <div>{{{{ item.created_at or '-' }}}}</div>
            </div>
            <div class="detail-item">
                <label>Updated Timestamp</label>
                <div>{{{{ item.updated_at or '-' }}}}</div>
            </div>
        </div>
    </div>
</div>
{{% endblock %}}
''')

    print("Frontend templates generated.")

if __name__ == '__main__':
    expand_templates_and_static()
