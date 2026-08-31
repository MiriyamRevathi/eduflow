import os

def generate_massive_views():
    base = os.path.dirname(os.path.abspath(__file__))

    # 1. Generate 20 Blueprint Routes
    route_modules = [
        ('user', 'User', 'System user management, RBAC, and user security policies.'),
        ('student', 'Student', 'Student directory, registration, academic profile, and history.'),
        ('faculty', 'Faculty', 'Faculty member management, department assignment, and workload.'),
        ('parent', 'Parent', 'Parent portal, student link, and parent communication.'),
        ('course', 'Course', 'Degree programs, departments, and course catalog management.'),
        ('subject', 'Subject', 'Subject catalog, credit hours, and semester prerequisites.'),
        ('attendance', 'Attendance', 'Classroom attendance tracking, bulk marking, and percentages.'),
        ('exam', 'Exam', 'Examination scheduling, room allocations, and exam status.'),
        ('marks', 'Marks', 'Marks entry, grade computation (A+ to F), GPA, and transcripts.'),
        ('assignment', 'Assignment', 'Assignments, student submissions, and teacher grading feedback.'),
        ('fee', 'Fee', 'Fee structures, invoice ledgers, discount policies, and balance tracking.'),
        ('payment', 'Payment', 'Payment processing simulation (Cash/Card/UPI) and receipts.'),
        ('library', 'Library', 'Book circulation, issue/return transactions, and overdue fines.'),
        ('book', 'Book', 'Library catalog indexing, ISBN search, categories, and shelving.'),
        ('hostel', 'Hostel', 'Hostel residential halls, room capacity, and bed allocations.'),
        ('transport', 'Transport', 'Fleet vehicles, drivers, route stops, and student capacity check.'),
        ('leave', 'Leave', 'Leave applications, multi-role approval pipeline, and leave balances.'),
        ('event', 'Event', 'Campus events calendar, targeted announcements, and news feed.'),
        ('admission', 'Admission', 'Applicant pipeline, application review, and student enrollment.'),
        ('timetable', 'Timetable', 'Weekly schedule grid, period booking, and conflict detector.')
    ]

    for r_name, r_title, r_desc in route_modules:
        if r_name in ['student', 'faculty', 'admission', 'attendance', 'timetable', 'exam', 'fee', 'library', 'hostel', 'transport', 'leave', 'event', 'auth', 'dashboard', 'analytics', 'ml', 'search', 'audit', 'notification', 'portal']:
            continue  # Keep custom routes already verified

        r_path = os.path.join(base, 'routes', f"{r_name}_routes.py")
        with open(r_path, 'w', encoding='utf-8') as f:
            f.write(f'''"""
EduFlow ERP Route Controller — {r_title}Routes
Blueprint routes for {r_desc}
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.{r_name}_service import {r_title}Service
from security.rbac import login_required, admin_required
from security.session import SessionManager

{r_name}s_bp = Blueprint('{r_name}s', __name__, url_prefix='/{r_name}s')
service = {r_title}Service()

@{r_name}s_bp.route('/')
@login_required
def index():
    """List records with pagination, text search query, and status filter."""
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    status = request.args.get('status', '')

    result = service.get_paginated(page=page, per_page=10, query=search_q, status=status)
    return render_template('{r_name}s/index.html', items=result['items'], pagination=result, search_q=search_q, status=status)

@{r_name}s_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create new {r_name} record."""
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, created = service.create_record(payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('{r_name}s.index'))
        else:
            flash(msg, 'danger')

    return render_template('{r_name}s/form.html', item=None)

@{r_name}s_bp.route('/<item_id>')
@login_required
def view(item_id):
    """View detailed record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('{r_title} record not found.', 'danger')
        return redirect(url_for('{r_name}s.index'))
    return render_template('{r_name}s/view.html', item=item)

@{r_name}s_bp.route('/<item_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(item_id):
    """Edit existing {r_name} record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('{r_title} record not found.', 'danger')
        return redirect(url_for('{r_name}s.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, updated = service.update_record(item_id, payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('{r_name}s.view', item_id=item_id))
        else:
            flash(msg, 'danger')

    return render_template('{r_name}s/form.html', item=item)

@{r_name}s_bp.route('/<item_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(item_id):
    """Soft delete/archive record."""
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()
    success, msg = service.archive_record(item_id, actor_email, actor_role)
    if success:
        flash(msg, 'info')
    else:
        flash(msg, 'danger')
    return redirect(url_for('{r_name}s.index'))
''')

    print("Routes generation complete.")

if __name__ == '__main__':
    generate_massive_views()
