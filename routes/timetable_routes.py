from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.timetable_service import TimetableService
from repositories.teacher_repository import TeacherRepository
from repositories.subject_repository import SubjectRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

timetable_bp = Blueprint('timetable', __name__, url_prefix='/timetable')
timetable_service = TimetableService()
teacher_repo = TeacherRepository()
subject_repo = SubjectRepository()

@timetable_bp.route('/')
@login_required
def index():
    class_name = request.args.get('class_name', 'CS-101')
    section = request.args.get('section', 'A')

    grid_data = timetable_service.get_timetable_grid(class_name, section)
    return render_template('timetable/index.html', grid_data=grid_data)

@timetable_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_period():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'class_name': request.form.get('class_name'),
            'section': request.form.get('section'),
            'day': request.form.get('day'),
            'start_time': request.form.get('start_time'),
            'end_time': request.form.get('end_time'),
            'subject_id': request.form.get('subject_id'),
            'teacher_id': request.form.get('teacher_id'),
            'room': request.form.get('room')
        }

        success, msg, created, conflicts = timetable_service.add_period(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('timetable.index', class_name=data['class_name'], section=data['section']))
        else:
            for c in conflicts:
                flash(c, 'danger')

    teachers = teacher_repo.find_all()
    subjects = subject_repo.find_all()
    return render_template('timetable/form.html', teachers=teachers, subjects=subjects)

@timetable_bp.route('/<period_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_period(period_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()
    success, msg = timetable_service.delete_period(period_id, actor_email, actor_role)
    if success:
        flash(msg, 'info')
    else:
        flash(msg, 'danger')
    return redirect(url_for('timetable.index'))
