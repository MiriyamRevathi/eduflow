from flask import Blueprint, render_template
from repositories.audit_repository import AuditRepository
from security.rbac import login_required, admin_required

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')
audit_repo = AuditRepository()

@audit_bp.route('/')
@login_required
@admin_required
def index():
    logs = audit_repo.get_recent(limit=50)
    return render_template('audit/index.html', logs=logs)
