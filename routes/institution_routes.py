"""
EduFlow ERP Route Controller — InstitutionRoutes
Blueprint routes for Super Admin Institution Management.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, Response, jsonify
from services.institution_service import InstitutionService
from security.rbac import login_required, admin_required
from security.session import SessionManager

institutions_bp = Blueprint('institutions', __name__, url_prefix='/institutions')
service = InstitutionService()

@institutions_bp.route('/')
@login_required
def index():
    status_filter = request.args.get('status', '').strip()
    type_filter = request.args.get('type', '').strip()
    search_q = request.args.get('q', '').strip().lower()

    institutions = service.get_all(status_filter=status_filter, type_filter=type_filter)
    if search_q:
        institutions = [i for i in institutions if search_q in i.get('name', '').lower() or search_q in i.get('code', '').lower() or search_q in i.get('city', '').lower()]

    stats = service.get_summary_stats()
    return render_template('institutions/index.html', institutions=institutions, stats=stats, status_filter=status_filter, type_filter=type_filter, search_q=search_q)

@institutions_bp.route('/create', methods=['POST'])
@login_required
@admin_required
def create():
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()
    payload = request.form.to_dict()

    success, msg, created = service.create_institution(payload, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/<item_id>')
@login_required
def view(item_id):
    institution = service.get_by_id(item_id)
    if not institution:
        flash('Institution not found.', 'danger')
        return redirect(url_for('institutions.index'))
    return render_template('institutions/view.html', institution=institution)

@institutions_bp.route('/<item_id>/edit', methods=['POST'])
@login_required
@admin_required
def edit(item_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()
    payload = request.form.to_dict()

    success, msg, updated = service.update_institution(item_id, payload, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/<item_id>/status/<status>', methods=['POST'])
@login_required
@admin_required
def update_status(item_id, status):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = service.set_status(item_id, status.upper(), actor_email, actor_role)
    if success:
        flash(msg, 'info')
    else:
        flash(msg, 'danger')
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/<item_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(item_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = service.delete_institution(item_id, actor_email, actor_role)
    if success:
        flash(msg, 'warning')
    else:
        flash(msg, 'danger')
    return redirect(url_for('institutions.index'))

@institutions_bp.route('/export/csv')
@login_required
def export_csv():
    csv_data = service.export_csv()
    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=institutions_export.csv"})
