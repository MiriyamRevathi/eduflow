from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.admission_service import AdmissionService
from repositories.course_repository import CourseRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

admissions_bp = Blueprint('admissions', __name__, url_prefix='/admissions')
admission_service = AdmissionService()
course_repo = CourseRepository()

@admissions_bp.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    search_q = request.args.get('q', '').strip()
    status = request.args.get('status', '')

    result = admission_service.get_paginated_admissions(
        page=page,
        per_page=10,
        search_query=search_q,
        status=status
    )

    return render_template(
        'admissions/index.html',
        admissions=result['items'],
        pagination=result,
        search_q=search_q,
        status=status
    )

@admissions_bp.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        data = {
            'applicant_name': request.form.get('applicant_name'),
            'email': request.form.get('email'),
            'phone': request.form.get('phone'),
            'course_id': request.form.get('course_id'),
            'previous_qualification': request.form.get('previous_qualification'),
            'remarks': request.form.get('remarks')
        }

        success, msg, created = admission_service.apply(data)
        if success:
            flash(msg, 'success')
            if SessionManager.is_authenticated():
                return redirect(url_for('admissions.index'))
            else:
                return redirect(url_for('auth.login'))
        else:
            flash(msg, 'danger')

    courses = course_repo.find_all()
    return render_template('admissions/apply.html', courses=courses)

@admissions_bp.route('/<admission_id>')
@login_required
def view_admission(admission_id):
    admission = admission_service.admission_repo.find_by_id(admission_id)
    if not admission:
        flash('Admission record not found.', 'danger')
        return redirect(url_for('admissions.index'))

    course = course_repo.find_by_id(admission.get('course_id'))
    admission['course'] = course
    return render_template('admissions/view.html', admission=admission)

@admissions_bp.route('/<admission_id>/status', methods=['POST'])
@login_required
@admin_required
def update_status(admission_id):
    new_status = request.form.get('status')
    remarks = request.form.get('remarks', '')
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = admission_service.update_status(admission_id, new_status, remarks, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('admissions.view_admission', admission_id=admission_id))

@admissions_bp.route('/<admission_id>/enroll', methods=['POST'])
@login_required
@admin_required
def enroll_applicant(admission_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = admission_service.enroll_applicant(admission_id, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('admissions.view_admission', admission_id=admission_id))
