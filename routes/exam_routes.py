from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.exam_service import ExamService
from repositories.course_repository import CourseRepository
from repositories.subject_repository import SubjectRepository
from repositories.student_repository import StudentRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

exams_bp = Blueprint('exams', __name__, url_prefix='/exams')
exam_service = ExamService()
course_repo = CourseRepository()
subject_repo = SubjectRepository()
student_repo = StudentRepository()

@exams_bp.route('/')
@login_required
def index():
    exams = exam_service.get_all_exams()
    return render_template('exams/index.html', exams=exams)

@exams_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_exam():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'title': request.form.get('title'),
            'course_id': request.form.get('course_id'),
            'subject_id': request.form.get('subject_id'),
            'exam_date': request.form.get('exam_date'),
            'start_time': request.form.get('start_time'),
            'end_time': request.form.get('end_time'),
            'room': request.form.get('room'),
            'max_marks': request.form.get('max_marks'),
            'pass_marks': request.form.get('pass_marks')
        }

        success, msg, created = exam_service.create_exam(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('exams.index'))
        else:
            flash(msg, 'danger')

    courses = course_repo.find_all()
    subjects = subject_repo.find_all()
    return render_template('exams/form.html', courses=courses, subjects=subjects)

@exams_bp.route('/<exam_id>/marks', methods=['GET', 'POST'])
@login_required
@admin_required
def enter_marks(exam_id):
    exam = exam_service.exam_repo.find_by_id(exam_id)
    if not exam:
        flash('Exam not found.', 'danger')
        return redirect(url_for('exams.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        student_ids = request.form.getlist('student_id')
        marks_payload = []
        for s_id in student_ids:
            marks_obtained = request.form.get(f'marks_{s_id}', 0)
            remarks = request.form.get(f'remarks_{s_id}', '')
            marks_payload.append({
                'student_id': s_id,
                'marks_obtained': marks_obtained,
                'remarks': remarks
            })

        success, msg = exam_service.save_bulk_marks(exam_id, marks_payload, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('exams.index'))
        else:
            flash(msg, 'danger')

    students = student_repo.find_by_course(exam.get('course_id'))
    if not students:
        students = student_repo.find_all()

    existing_marks = exam_service.marks_repo.find_by_exam(exam_id)
    marks_map = {m['student_id']: m for m in existing_marks}

    return render_template('exams/marks_entry.html', exam=exam, students=students, marks_map=marks_map)
