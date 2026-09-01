"""
EduFlow ERP Route Controller — UserRoutes
Blueprint routes for System user management, RBAC, and user security policies.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from services.user_service import UserService
from security.rbac import login_required, admin_required
from security.session import SessionManager

users_bp = Blueprint('users', __name__, url_prefix='/users')
service = UserService()

@users_bp.route('/super-admin/users')
@users_bp.route('/')
@login_required
def index():
    """List records with pagination, text search query, and status filter."""
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    status = request.args.get('status', '')
    selected_inst_id = session.get('selected_institution_id', 'ALL')

    result = service.get_paginated(page=page, per_page=10, query=search_q, status=status, institution_id=selected_inst_id)
    return render_template('users/index.html', items=result['items'], pagination=result, search_q=search_q, status=status)

@users_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def create():
    """Create new user record."""
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, created = service.create_record(payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('users.index'))
        else:
            flash(msg, 'danger')

    return render_template('users/form.html', item=None)

@users_bp.route('/<item_id>')
@login_required
def view(item_id):
    """View detailed record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('User record not found.', 'danger')
        return redirect(url_for('users.index'))
    return render_template('users/view.html', item=item)

@users_bp.route('/<item_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit(item_id):
    """Edit existing user record."""
    item = service.get_by_id(item_id)
    if not item:
        flash('User record not found.', 'danger')
        return redirect(url_for('users.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()
        payload = request.form.to_dict()

        success, msg, updated = service.update_record(item_id, payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('users.view', item_id=item_id))
        else:
            flash(msg, 'danger')

    return render_template('users/form.html', item=item)

@users_bp.route('/<item_id>/delete', methods=['POST'])
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
    return redirect(url_for('users.index'))
