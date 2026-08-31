from flask import Blueprint, render_template, Response
from services.report_service import ReportService
from security.rbac import login_required

analytics_bp = Blueprint('analytics', __name__, url_prefix='/analytics')
reporting_bp = Blueprint('reporting', __name__, url_prefix='/reporting')
report_service = ReportService()

@analytics_bp.route('/')
@login_required
def index():
    return render_template('analytics/index.html')

@reporting_bp.route('/students/csv')
@login_required
def export_students_csv():
    csv_data = report_service.export_students_csv()
    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=students_export.csv"})

@reporting_bp.route('/attendance/csv')
@login_required
def export_attendance_csv():
    csv_data = report_service.export_attendance_csv()
    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=attendance_export.csv"})

@reporting_bp.route('/exams/csv')
@login_required
def export_exams_csv():
    csv_data = report_service.export_exams_csv()
    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=exams_export.csv"})

@reporting_bp.route('/fees/csv')
@login_required
def export_fees_csv():
    csv_data = report_service.export_fees_csv()
    return Response(csv_data, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=fees_export.csv"})
