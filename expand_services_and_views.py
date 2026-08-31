import os

def expand_all():
    base = os.path.dirname(os.path.abspath(__file__))

    # 1. Expand Analytics Modules
    analytics_files = {
        'dashboard_analytics.py': '''"""
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
''',
        'academic_analytics.py': '''"""
EduFlow ERP Academic Performance Analytics
Computes course GPAs, subject pass rates, and grade distributions.
"""
from typing import Dict, Any, List
from repositories.marks_repository import MarksRepository
from repositories.course_repository import CourseRepository
from repositories.subject_repository import SubjectRepository

class AcademicAnalytics:
    def __init__(self):
        self.marks_repo = MarksRepository()
        self.course_repo = CourseRepository()
        self.subject_repo = SubjectRepository()

    def get_course_performance_breakdown(self, course_id: str) -> Dict[str, Any]:
        subjects = self.subject_repo.find_by_course(course_id)
        subject_stats = []
        for s in subjects:
            marks = self.marks_repo.find_by_field('subject_id', s['id'])
            if marks:
                avg_obtained = sum(m.get('marks_obtained', 0) for m in marks) / len(marks)
                pass_cnt = sum(1 for m in marks if m.get('status') == 'PASSED')
                pass_rate = round((pass_cnt / len(marks) * 100.0), 1)
            else:
                avg_obtained = 0.0
                pass_rate = 100.0

            subject_stats.append({
                'subject_id': s['id'],
                'subject_name': s['name'],
                'avg_marks': round(avg_obtained, 2),
                'pass_rate_pct': pass_rate
            })

        return {
            'course_id': course_id,
            'subject_stats': subject_stats
        }
''',
        'attendance_analytics.py': '''"""
EduFlow ERP Attendance Analytics
Computes monthly attendance trends and absence alerts.
"""
from typing import Dict, Any, List
from repositories.attendance_repository import AttendanceRepository
from repositories.student_repository import StudentRepository

class AttendanceAnalytics:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.student_repo = StudentRepository()

    def get_low_attendance_students(self, threshold_pct: float = 75.0) -> List[Dict[str, Any]]:
        students = self.student_repo.find_all()
        low_att_list = []
        for std in students:
            pct = self.attendance_repo.get_attendance_percentage(std['id'])
            if pct < threshold_pct:
                std_copy = dict(std)
                std_copy['attendance_pct'] = pct
                low_att_list.append(std_copy)
        return low_att_list
''',
        'fee_analytics.py': '''"""
EduFlow ERP Fee Analytics
Generates financial ledgers and collection summaries.
"""
from typing import Dict, Any, List
from repositories.fee_repository import FeeRepository
from repositories.payment_repository import PaymentRepository

class FeeAnalytics:
    def __init__(self):
        self.fee_repo = FeeRepository()
        self.payment_repo = PaymentRepository()

    def get_financial_summary(self) -> Dict[str, Any]:
        fees = self.fee_repo.find_all()
        payments = self.payment_repo.find_all()

        total_invoiced = sum(f.get('net_amount', 0) for f in fees)
        total_collected = sum(p.get('amount', 0) for p in payments)
        total_outstanding = total_invoiced - total_collected

        method_breakdown = {}
        for p in payments:
            m = p.get('payment_method', 'CARD')
            method_breakdown[m] = method_breakdown.get(m, 0.0) + float(p.get('amount', 0))

        return {
            'total_invoiced': total_invoiced,
            'total_collected': total_collected,
            'total_outstanding': total_outstanding,
            'method_breakdown': method_breakdown
        }
'''
    }

    for fn, content in analytics_files.items():
        fp = os.path.join(base, 'analytics', fn)
        with open(fp, 'w', encoding='utf-8') as f:
            f.write(content)

    print("Analytics engines generated.")

if __name__ == '__main__':
    expand_all()
