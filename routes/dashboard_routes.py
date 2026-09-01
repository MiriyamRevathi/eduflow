from flask import Blueprint, render_template, request, session
from repositories.institution_repository import InstitutionRepository
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.user_repository import UserRepository
from repositories.fee_repository import FeeRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.audit_repository import AuditRepository
from security.rbac import login_required
from security.session import SessionManager

dashboard_bp = Blueprint('dashboard', __name__)

inst_repo = InstitutionRepository()
student_repo = StudentRepository()
teacher_repo = TeacherRepository()
user_repo = UserRepository()
fee_repo = FeeRepository()
attendance_repo = AttendanceRepository()
audit_repo = AuditRepository()

@dashboard_bp.route('/super-admin/dashboard')
@dashboard_bp.route('/dashboard')
@dashboard_bp.route('/')
@login_required
def index():
    user_role = SessionManager.get_current_role()
    period = request.args.get('period', 'this_month')
    selected_inst_id = session.get('selected_institution_id', 'ALL')

    all_institutions = inst_repo.find_all()

    if selected_inst_id != 'ALL':
        institutions = [i for i in all_institutions if i.get('id') == selected_inst_id]
        inst_info = inst_repo.find_by_id(selected_inst_id)
        
        all_students = [s for s in student_repo.find_all() if s.get('institution_id') == selected_inst_id]
        all_faculty = [t for t in teacher_repo.find_all() if t.get('institution_id') == selected_inst_id]
        all_users = [u for u in user_repo.find_all() if u.get('institution_id') == selected_inst_id]
        all_fees = [f for f in fee_repo.find_all() if f.get('institution_id') == selected_inst_id]

        total_inst = 1
        total_students = len(all_students) if all_students else inst_info.get('students_count', 0) if inst_info else 0
        total_faculty = len(all_faculty) if all_faculty else inst_info.get('faculty_count', 0) if inst_info else 0
        total_active_users = len(all_users) if all_users else total_students + total_faculty
        total_fee_collection = sum(f.get('paid_amount', 0.0) for f in all_fees) if all_fees else inst_info.get('fee_collection', 0.0) if inst_info else 0.0
        total_pending_fees = sum(f.get('pending_amount', 0.0) for f in all_fees) if all_fees else inst_info.get('pending_fees', 0.0) if inst_info else 0.0
        avg_attendance = inst_info.get('attendance_rate', 95.0) if inst_info else 95.0
    else:
        institutions = all_institutions
        total_inst = len(institutions)
        total_students = sum(i.get('students_count', 0) for i in institutions)
        total_faculty = sum(i.get('faculty_count', 0) for i in institutions)
        total_active_users = user_repo.count() + total_students
        total_fee_collection = sum(i.get('fee_collection', 0.0) for i in institutions)
        total_pending_fees = sum(i.get('pending_fees', 0.0) for i in institutions)
        avg_attendance = 94.2

    stats = {
        'total_institutions': total_inst,
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_active_users': total_active_users,
        'total_fee_collection': total_fee_collection,
        'total_pending_fees': total_pending_fees,
        'avg_attendance': avg_attendance
    }

    requires_attention = [
        {
            'id': 'att-01',
            'title': 'Metro Science Academy — Pending Registration Review',
            'description': 'Registration submitted. Requires Super Admin verification.',
            'action_label': 'Approve',
            'action_url': '/institutions/?status=PENDING'
        },
        {
            'id': 'att-02',
            'title': 'Horizon College of Arts — Low Attendance Warning',
            'description': 'Attendance dropped to 84.1% (below 85% compliance threshold).',
            'action_label': 'Resolve',
            'action_url': '/attendance/'
        },
        {
            'id': 'att-03',
            'title': 'Royal Academy High — Overdue Fees Notice',
            'description': '$142,000 in tuition fees past due date.',
            'action_label': 'Send Notice',
            'action_url': '/fees/'
        }
    ]

    recent_activities = audit_repo.get_recent(limit=6)

    return render_template(
        'dashboard/index.html',
        stats=stats,
        institutions=institutions,
        requires_attention=requires_attention,
        recent_activities=recent_activities,
        user_role=user_role,
        selected_period=period,
        selected_inst_id=selected_inst_id
    )
