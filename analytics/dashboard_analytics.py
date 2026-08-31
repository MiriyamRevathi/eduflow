"""
EduFlow ERP Dashboard Analytics Engine
Aggregates key metrics for executive dashboards.
"""
from typing import Dict, Any, List
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.fee_repository import FeeRepository

class DashboardAnalytics:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.teacher_repo = TeacherRepository()
        self.course_repo = CourseRepository()
        self.attendance_repo = AttendanceRepository()
        self.fee_repo = FeeRepository()

    def compute_summary_kpis(self) -> Dict[str, Any]:
        total_students = self.student_repo.count()
        total_faculty = self.teacher_repo.count()
        total_courses = self.course_repo.count()
        all_fees = self.fee_repo.find_all()
        pending_amount = sum(f.get('pending_amount', 0) for f in all_fees)
        paid_amount = sum(f.get('paid_amount', 0) for f in all_fees)
        total_net = sum(f.get('net_amount', 0) for f in all_fees)
        collection_ratio = round((paid_amount / total_net * 100.0), 1) if total_net > 0 else 0.0

        return {
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_courses': total_courses,
            'pending_fee_balance': pending_amount,
            'collected_fee_total': paid_amount,
            'collection_ratio_pct': collection_ratio
        }
