from flask import Blueprint, render_template
from repositories.audit_repository import AuditRepository
from security.rbac import login_required, admin_required

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')
audit_repo = AuditRepository()

@audit_bp.route('/super-admin/audit-logs')
@audit_bp.route('/')
@login_required
@admin_required
def index():
    selected_inst_id = session.get('selected_institution_id', 'ALL')
    logs = audit_repo.get_recent(limit=50)
    if selected_inst_id != 'ALL':
        logs = [l for l in logs if l.get('institution_id') == selected_inst_id or not l.get('institution_id')]
    return render_template('audit/index.html', logs=logs)
