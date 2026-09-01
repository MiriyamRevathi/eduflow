from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.attendance_service import AttendanceService
from security.rbac import login_required
from security.session import SessionManager
from utils.datetime_utils import DateTimeUtils

attendance_bp = Blueprint('attendance', __name__, url_prefix='/attendance')
attendance_service = AttendanceService()

@attendance_bp.route('/super-admin/attendance')
@attendance_bp.route('/')
@login_required
def index():
    date_str = request.args.get('date', DateTimeUtils.current_date_str())
    class_name = request.args.get('class_name', 'CS-101')
    section = request.args.get('section', 'A')
    selected_inst_id = session.get('selected_institution_id', 'ALL')

    overview = attendance_service.get_attendance_overview(date_str, class_name, section)
    if selected_inst_id != 'ALL' and 'records' in overview:
        overview['records'] = [r for r in overview['records'] if r.get('institution_id') == selected_inst_id or not r.get('institution_id')]
    return render_template('attendance/index.html', overview=overview)

@attendance_bp.route('/mark', methods=['GET', 'POST'])
@login_required
def mark():
    if request.method == 'POST':
        date_str = request.form.get('date')
        class_name = request.form.get('class_name')
        section = request.form.get('section')
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        student_ids = request.form.getlist('student_id')
        attendance_payload = []
        for s_id in student_ids:
            status = request.form.get(f'status_{s_id}', 'PRESENT')
            remarks = request.form.get(f'remarks_{s_id}', '')
            attendance_payload.append({
                'student_id': s_id,
                'status': status,
                'remarks': remarks
            })

        success, msg = attendance_service.save_bulk_attendance(date_str, class_name, section, attendance_payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('attendance.index', date=date_str, class_name=class_name, section=section))
        else:
            flash(msg, 'danger')

    date_str = request.args.get('date', DateTimeUtils.current_date_str())
    class_name = request.args.get('class_name', 'CS-101')
    section = request.args.get('section', 'A')
    overview = attendance_service.get_attendance_overview(date_str, class_name, section)

    return render_template('attendance/mark.html', overview=overview)
