"""
EduFlow ERP Route Controller — ReportsRoutes
Blueprint routes for System Reports Engine.
"""
from flask import Blueprint, render_template, Response
from services.report_service import ReportService
from security.rbac import login_required

reports_bp = Blueprint('reports', __name__, url_prefix='/reports')
report_service = ReportService()

@reports_bp.route('/')
@login_required
def index():
    return render_template('reports/index.html')
