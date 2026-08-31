"""
EduFlow ERP Route Controller — MarksRoutes
Blueprint routes for Marks entry, grade computation (A+ to F), GPA, and transcripts.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from services.marks_service import MarksService
from security.rbac import login_required, admin_required
from security.session import SessionManager

markss_bp = Blueprint('markss', __name__, url_prefix='/markss')
service = MarksService()

@markss_bp.route('/')
@login_required
def index():
    """List records with pagination, text search query, and status filter."""
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    status = request.args.get('status', '')

    result = service.get_paginated(page=page, per_page=10, query=search_q, status=status)
    return render_template('markss/index.html', items=result['items'], pagination=result, search_q=search_q, status=status)

@markss_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create new marks record."""
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, created = service.create_record(payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('markss.index'))
        else:
            flash(msg, 'danger')

    return render_template('markss/form.html', item=None)

@markss_bp.route('/<item_id>')
@login_required
def view(item_id):
    """View detailed record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('Marks record not found.', 'danger')
        return redirect(url_for('markss.index'))
    return render_template('markss/view.html', item=item)

@markss_bp.route('/<item_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(item_id):
    """Edit existing marks record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('Marks record not found.', 'danger')
        return redirect(url_for('markss.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, updated = service.update_record(item_id, payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('markss.view', item_id=item_id))
        else:
            flash(msg, 'danger')

    return render_template('markss/form.html', item=item)

@markss_bp.route('/<item_id>/delete', methods=['POST'])
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
    return redirect(url_for('markss.index'))
