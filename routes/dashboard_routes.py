from flask import Blueprint, render_template, request
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

@dashboard_bp.route('/dashboard')
@dashboard_bp.route('/')
@login_required
def index():
    user_role = SessionManager.get_current_role()
    period = request.args.get('period', 'this_month')

    institutions = inst_repo.find_all()

    total_inst = len(institutions)
    total_students = sum(i.get('students_count', 0) for i in institutions)
    total_faculty = sum(i.get('faculty_count', 0) for i in institutions)
    total_active_users = user_repo.count() + total_students
    total_fee_collection = sum(i.get('fee_collection', 0.0) for i in institutions)
    total_pending_fees = sum(i.get('pending_fees', 0.0) for i in institutions)

    stats = {
        'total_institutions': total_inst,
        'total_students': total_students,
        'total_faculty': total_faculty,
        'total_active_users': total_active_users,
        'total_fee_collection': total_fee_collection,
        'total_pending_fees': total_pending_fees,
        'avg_attendance': 94.2
    }

    requires_attention = [
        {
            'id': 'att-01',
            'type': 'warning',
            'icon': '⚠️',
            'title': 'Metro Science Academy — Pending Registration Approval',
            'description': 'Submitted documentation 2 days ago. Requires Super Admin verification.',
            'badge': 'Pending Approval',
            'badge_class': 'badge-warning',
            'action_label': 'Approve',
            'action_url': '/institutions?status=PENDING'
        },
        {
            'id': 'att-02',
            'type': 'danger',
            'icon': '🚨',
            'title': 'Horizon College of Arts — Low Attendance Alert',
            'description': 'Monthly attendance dropped to 84.1% (below 85% compliance threshold).',
            'badge': 'Low Attendance',
            'badge_class': 'badge-danger',
            'action_label': 'Resolve',
            'action_url': '/attendance'
        },
        {
            'id': 'att-03',
            'type': 'warning',
            'icon': '💰',
            'title': 'Royal Academy High — Overdue Fee Balances',
            'description': '$142,000 in tuition fees past due date by over 30 days.',
            'badge': 'Overdue Fees',
            'badge_class': 'badge-warning',
            'action_label': 'Send Notice',
            'action_url': '/fees'
        },
        {
            'id': 'att-04',
            'type': 'secondary',
            'icon': '🔒',
            'title': 'Pacific Institute — Suspended Account Review',
            'description': 'Account temporarily suspended during regulatory audit.',
            'badge': 'Suspended',
            'badge_class': 'badge-secondary',
            'action_label': 'Manage',
            'action_url': '/institutions?status=SUSPENDED'
        }
    ]

    recent_activities = audit_repo.get_recent(limit=8)

    return render_template(
        'dashboard/index.html',
        stats=stats,
        institutions=institutions,
        requires_attention=requires_attention,
        recent_activities=recent_activities,
        user_role=user_role,
        selected_period=period
    )
