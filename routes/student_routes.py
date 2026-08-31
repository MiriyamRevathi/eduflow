from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.student_service import StudentService
from repositories.course_repository import CourseRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

students_bp = Blueprint('students', __name__, url_prefix='/students')
student_service = StudentService()
course_repo = CourseRepository()

@students_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    course_id = request.args.get('course_id', '')
    status = request.args.get('status', '')

    result = student_service.get_paginated_students(
        page=page,
        per_page=10,
        search_query=search_q,
        course_id=course_id,
        status=status
    )
    courses = course_repo.find_all()

    return render_template(
        'students/index.html',
        students=result['items'],
        pagination=result,
        courses=courses,
        search_q=search_q,
        course_id=course_id,
        status=status
    )

@students_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_student():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'gender': request.form.get('gender'),
            'dob': request.form.get('dob'),
            'course_id': request.form.get('course_id'),
            'class_name': request.form.get('class_name'),
            'section': request.form.get('section'),
            'semester': request.form.get('semester'),
            'academic_year': request.form.get('academic_year'),
            'guardian_name': request.form.get('guardian_name'),
            'guardian_phone': request.form.get('guardian_phone'),
            'address': request.form.get('address'),
            'enrollment_date': request.form.get('enrollment_date')
        }

        success, msg, created = student_service.create_student(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('students.view_student', student_id=created['id']))
        else:
            flash(msg, 'danger')

    courses = course_repo.find_all()
    return render_template('students/form.html', student=None, courses=courses)

@students_bp.route('/<student_id>')
@login_required
def view_student(student_id):
    student = student_service.get_student_full_profile(student_id)
    if not student:
        flash('Student record not found.', 'danger')
        return redirect(url_for('students.index'))
    return render_template('students/view.html', student=student)

@students_bp.route('/<student_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_student(student_id):
    student = student_service.get_student_full_profile(student_id)
    if not student:
        flash('Student record not found.', 'danger')
        return redirect(url_for('students.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        updates = {
            'full_name': request.form.get('full_name'),
            'phone': request.form.get('phone'),
            'gender': request.form.get('gender'),
            'dob': request.form.get('dob'),
            'course_id': request.form.get('course_id'),
            'class_name': request.form.get('class_name'),
            'section': request.form.get('section'),
            'semester': int(request.form.get('semester', 1)),
            'academic_year': request.form.get('academic_year'),
            'guardian_name': request.form.get('guardian_name'),
            'guardian_phone': request.form.get('guardian_phone'),
            'address': request.form.get('address'),
            'status': request.form.get('status', 'ACTIVE')
        }

        success, msg = student_service.update_student(student_id, updates, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('students.view_student', student_id=student_id))
        else:
            flash(msg, 'danger')

    courses = course_repo.find_all()
    return render_template('students/form.html', student=student, courses=courses)

@students_bp.route('/<student_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_student(student_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()
    success, msg = student_service.delete_student(student_id, actor_email, actor_role)
    if success:
        flash(msg, 'info')
    else:
        flash(msg, 'danger')
    return redirect(url_for('students.index'))
