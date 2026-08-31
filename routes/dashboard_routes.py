from flask import Blueprint, render_template, session
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.fee_repository import FeeRepository
from repositories.exam_repository import ExamRepository
from repositories.book_repository import BookRepository
from repositories.hostel_repository import HostelRepository
from repositories.transport_repository import TransportRepository
from repositories.audit_repository import AuditRepository
from security.rbac import login_required
from security.session import SessionManager
from utils.datetime_utils import DateTimeUtils

dashboard_bp = Blueprint('dashboard', __name__)

student_repo = StudentRepository()
teacher_repo = TeacherRepository()
course_repo = CourseRepository()
attendance_repo = AttendanceRepository()
fee_repo = FeeRepository()
exam_repo = ExamRepository()
book_repo = BookRepository()
hostel_repo = HostelRepository()
transport_repo = TransportRepository()
audit_repo = AuditRepository()

@dashboard_bp.route('/dashboard')
@dashboard_bp.route('/')
@login_required
def index():
    user_role = SessionManager.get_current_role()

    # Base Metrics for Admin & Dashboard Cards
    total_students = student_repo.count()
    total_faculty = teacher_repo.count()
    total_courses = course_repo.count()

    today_str = DateTimeUtils.current_date_str()
    today_att = attendance_repo.find_by_date(today_str)
    present_today = sum(1 for a in today_att if a.get('status') == 'PRESENT')
    attendance_pct = round((present_today / total_students * 100.0), 1) if total_students > 0 else 92.5

    all_fees = fee_repo.find_all()
    pending_fees = sum(f.get('pending_amount', 0) for f in all_fees)

    upcoming_exams = len(exam_repo.find_where({'status': 'SCHEDULED'}))
    total_books = book_repo.count()
    
    hostels = hostel_repo.find_all()
    occupied_beds = 0
    total_beds = 0
    for h in hostels:
        for r in h.get('rooms', []):
            total_beds += int(r.get('capacity', 2))
            occupied_beds += int(r.get('occupied', 0))

    routes = transport_repo.find_all()
    total_transport_students = sum(len(r.get('assigned_student_ids', [])) for r in routes)

    recent_activities = audit_repo.get_recent(limit=10)

    stats = {
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_courses': total_courses,
        'attendance_pct': attendance_pct,
        'pending_fees': pending_fees,
        'upcoming_exams': upcoming_exams,
        'total_books': total_books,
        'hostel_occupancy': f"{occupied_beds}/{total_beds}",
        'transport_users': total_transport_students
    }

    return render_template(
        'dashboard/index.html',
        stats=stats,
        recent_activities=recent_activities,
        user_role=user_role
    )
