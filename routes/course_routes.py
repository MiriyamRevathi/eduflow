"""
EduFlow ERP Route Controller — CourseRoutes
Blueprint routes for Degree programs, departments, and course catalog management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.course_service import CourseService
from security.rbac import login_required, admin_required
from security.session import SessionManager

courses_bp = Blueprint('courses', __name__, url_prefix='/courses')
service = CourseService()

@courses_bp.route('/')
@login_required
def index():
    """List records with pagination, text search query, and status filter."""
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    status = request.args.get('status', '')

    result = service.get_paginated(page=page, per_page=10, query=search_q, status=status)
    return render_template('courses/index.html', items=result['items'], pagination=result, search_q=search_q, status=status)

@courses_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create new course record."""
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, created = service.create_record(payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('courses.index'))
        else:
            flash(msg, 'danger')

    return render_template('courses/form.html', item=None)

@courses_bp.route('/<item_id>')
@login_required
def view(item_id):
    """View detailed record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('Course record not found.', 'danger')
        return redirect(url_for('courses.index'))
    return render_template('courses/view.html', item=item)

@courses_bp.route('/<item_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(item_id):
    """Edit existing course record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('Course record not found.', 'danger')
        return redirect(url_for('courses.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, updated = service.update_record(item_id, payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('courses.view', item_id=item_id))
        else:
            flash(msg, 'danger')

    return render_template('courses/form.html', item=item)

@courses_bp.route('/<item_id>/delete', methods=['POST'])
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
    return redirect(url_for('courses.index'))
