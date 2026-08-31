from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.leave_service import LeaveService
from security.rbac import login_required, admin_required
from security.session import SessionManager

leave_bp = Blueprint('leave', __name__, url_prefix='/leave')
leave_service = LeaveService()

@leave_bp.route('/')
@login_required
def index():
    leaves = leave_service.get_all_leaves()
    return render_template('leave/index.html', leaves=leaves)

@leave_bp.route('/apply', methods=['POST'])
@login_required
def apply():
    actor_id = SessionManager.get_current_user_id()
    actor_name = session_name = SessionManager.SESSION_NAME_KEY
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    data = {
        'leave_type': request.form.get('leave_type'),
        'start_date': request.form.get('start_date'),
        'end_date': request.form.get('end_date'),
        'reason': request.form.get('reason')
    }

    success, msg, created = leave_service.apply_leave(data, actor_id, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('leave.index'))

@leave_bp.route('/<leave_id>/status', methods=['POST'])
@login_required
@admin_required
def update_status(leave_id):
    status = request.form.get('status')
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = leave_service.update_leave_status(leave_id, status, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('leave.index'))
