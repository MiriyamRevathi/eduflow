from flask import Blueprint, render_template, redirect, url_for
from services.student_service import StudentService
from services.faculty_service import FacultyService
from services.fee_service import FeeService
from services.library_service import LibraryService
from services.hostel_service import HostelService
from services.transport_service import TransportService
from services.timetable_service import TimetableService
from security.rbac import login_required
from security.session import SessionManager

portal_bp = Blueprint('portal', __name__, url_prefix='/portal')

student_service = StudentService()
faculty_service = FacultyService()
fee_service = FeeService()
library_service = LibraryService()
hostel_service = HostelService()
transport_service = TransportService()
timetable_service = TimetableService()

@portal_bp.route('/student')
@login_required
def student_portal():
    user_id = SessionManager.get_current_user_id()
    # Find student by user_id or fallback to default student
    student = student_service.student_repo.find_by_user_id(user_id)
    if not student:
        students = student_service.student_repo.find_all()
        student = students[0] if students else None

    if student:
        profile = student_service.get_student_full_profile(student['id'])
        timetable = timetable_service.get_timetable_grid(student.get('class_name', 'CS-101'), student.get('section', 'A'))
    else:
        profile = None
        timetable = None

    return render_template('portals/student_portal.html', student=profile, timetable=timetable)

@portal_bp.route('/parent')
@login_required
def parent_portal():
    user_id = SessionManager.get_current_user_id()
    parent = student_service.user_repo.find_by_id(user_id)
    students = student_service.student_repo.find_all()
    child = students[0] if students else None
    if child:
        child_profile = student_service.get_student_full_profile(child['id'])
    else:
        child_profile = None

    return render_template('portals/parent_portal.html', parent=parent, child=child_profile)

@portal_bp.route('/faculty')
@login_required
def faculty_portal():
    user_id = SessionManager.get_current_user_id()
    teacher = faculty_service.teacher_repo.find_by_user_id(user_id)
    if not teacher:
        teachers = faculty_service.teacher_repo.find_all()
        teacher = teachers[0] if teachers else None

    if teacher:
        profile = faculty_service.get_faculty_profile(teacher['id'])
    else:
        profile = None

    return render_template('portals/faculty_portal.html', faculty=profile)

@portal_bp.route('/accountant')
@login_required
def accountant_portal():
    fees = fee_service.get_all_fees()
    return render_template('portals/accountant_portal.html', fees=fees)

@portal_bp.route('/librarian')
@login_required
def librarian_portal():
    books = library_service.get_catalog()
    txns = library_service.library_repo.find_all()
    return render_template('portals/librarian_portal.html', books=books, transactions=txns)

@portal_bp.route('/warden')
@login_required
def warden_portal():
    hostels = hostel_service.get_hostels_summary()
    return render_template('portals/warden_portal.html', hostels=hostels)

@portal_bp.route('/transport')
@login_required
def transport_portal():
    routes = transport_service.get_all_routes()
    return render_template('portals/transport_portal.html', routes=routes)
