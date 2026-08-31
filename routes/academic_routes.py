from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.academic_service import AcademicService
from security.rbac import login_required, admin_required
from security.session import SessionManager

academics_bp = Blueprint('academics', __name__, url_prefix='/academics')
academic_service = AcademicService()

@academics_bp.route('/')
@login_required
def index():
    courses = academic_service.get_all_courses_with_subjects()
    return render_template('academics/index.html', courses=courses)

@academics_bp.route('/courses/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_course():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'code': request.form.get('code'),
            'name': request.form.get('name'),
            'department': request.form.get('department'),
            'duration_years': request.form.get('duration_years'),
            'total_semesters': request.form.get('total_semesters')
        }

        success, msg, created = academic_service.create_course(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('academics.index'))
        else:
            flash(msg, 'danger')

    return render_template('academics/course_form.html')

@academics_bp.route('/subjects/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_subject():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'code': request.form.get('code'),
            'name': request.form.get('name'),
            'course_id': request.form.get('course_id'),
            'credits': request.form.get('credits'),
            'semester': request.form.get('semester')
        }

        success, msg, created = academic_service.create_subject(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('academics.index'))
        else:
            flash(msg, 'danger')

    courses = academic_service.course_repo.find_all()
    return render_template('academics/subject_form.html', courses=courses)
