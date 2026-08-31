from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.hostel_service import HostelService
from repositories.student_repository import StudentRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

hostel_bp = Blueprint('hostel', __name__, url_prefix='/hostel')
hostel_service = HostelService()
student_repo = StudentRepository()

@hostel_bp.route('/')
@login_required
def index():
    hostels = hostel_service.get_hostels_summary()
    students = student_repo.find_all()
    return render_template('hostel/index.html', hostels=hostels, students=students)

@hostel_bp.route('/allocate', methods=['POST'])
@login_required
@admin_required
def allocate():
    hostel_id = request.form.get('hostel_id')
    room_no = request.form.get('room_no')
    student_id = request.form.get('student_id')
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = hostel_service.allocate_bed(hostel_id, room_no, student_id, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('hostel.index'))
