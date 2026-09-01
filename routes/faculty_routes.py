from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from services.faculty_service import FacultyService
from repositories.subject_repository import SubjectRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

faculty_bp = Blueprint('faculty', __name__, url_prefix='/faculty')
faculty_service = FacultyService()
subject_repo = SubjectRepository()

@faculty_bp.route('/super-admin/faculty')
@faculty_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    department = request.args.get('department', '')
    selected_inst_id = session.get('selected_institution_id', 'ALL')

    result = faculty_service.get_paginated_faculty(
        page=page,
        per_page=10,
        search_query=search_q,
        department=department,
        institution_id=selected_inst_id
    )

    return render_template(
        'faculty/index.html',
        teachers=result['items'],
        pagination=result,
        search_q=search_q,
        department=department
    )

@faculty_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_faculty():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        assigned_subjects = request.form.getlist('assigned_subject_ids')
        assigned_classes_raw = request.form.get('assigned_classes', '')
        classes_list = [c.strip() for c in assigned_classes_raw.split(',') if c.strip()]

        data = {
            'full_name': request.form.get('full_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'department': request.form.get('department'),
            'designation': request.form.get('designation'),
            'assigned_subject_ids': assigned_subjects,
            'assigned_classes': classes_list,
            'role': request.form.get('role', 'TEACHER')
        }

        success, msg, created = faculty_service.create_faculty(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('faculty.view_faculty', teacher_id=created['id']))
        else:
            flash(msg, 'danger')

    all_subjects = subject_repo.find_all()
    return render_template('faculty/form.html', teacher=None, subjects=all_subjects)

@faculty_bp.route('/<teacher_id>')
@login_required
def view_faculty(teacher_id):
    teacher = faculty_service.get_faculty_profile(teacher_id)
    if not teacher:
        flash('Faculty member not found.', 'danger')
        return redirect(url_for('faculty.index'))
    return render_template('faculty/view.html', teacher=teacher)

@faculty_bp.route('/<teacher_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_faculty(teacher_id):
    teacher = faculty_service.get_faculty_profile(teacher_id)
    if not teacher:
        flash('Faculty record not found.', 'danger')
        return redirect(url_for('faculty.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        assigned_subjects = request.form.getlist('assigned_subject_ids')
        assigned_classes_raw = request.form.get('assigned_classes', '')
        classes_list = [c.strip() for c in assigned_classes_raw.split(',') if c.strip()]

        updates = {
            'full_name': request.form.get('full_name'),
            'phone': request.form.get('phone'),
            'department': request.form.get('department'),
            'designation': request.form.get('designation'),
            'assigned_subject_ids': assigned_subjects,
            'assigned_classes': classes_list,
            'status': request.form.get('status', 'ACTIVE')
        }

        success, msg = faculty_service.update_faculty(teacher_id, updates, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('faculty.view_faculty', teacher_id=teacher_id))
        else:
            flash(msg, 'danger')

    all_subjects = subject_repo.find_all()
    return render_template('faculty/form.html', teacher=teacher, subjects=all_subjects)

@faculty_bp.route('/<teacher_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_faculty(teacher_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()
    success, msg = faculty_service.delete_faculty(teacher_id, actor_email, actor_role)
    if success:
        flash(msg, 'info')
    else:
        flash(msg, 'danger')
    return redirect(url_for('faculty.index'))
