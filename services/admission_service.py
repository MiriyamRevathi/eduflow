"""
EduFlow ERP Service — AdmissionService
Applicant registration, review pipeline, approval workflow, and student enrollment.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.admission_repository import AdmissionRepository
from repositories.student_repository import StudentRepository
from repositories.user_repository import UserRepository
from repositories.course_repository import CourseRepository
from repositories.audit_repository import AuditRepository
from security.password import PasswordSecurity
from utils.id_generator import IDGenerator
from config import Config

class AdmissionService:
    def __init__(self):
        self.admission_repo = AdmissionRepository()
        self.repo = self.admission_repo
        self.student_repo = StudentRepository()
        self.user_repo = UserRepository()
        self.course_repo = CourseRepository()
        self.audit_repo = AuditRepository()

    def get_paginated_admissions(self, page: int = 1, per_page: int = 10, search_query: str = None, status: str = None) -> Dict[str, Any]:
        criteria = {}
        if status:
            criteria['status'] = status
        res = self.admission_repo.paginate(
            page=page,
            per_page=per_page,
            criteria=criteria,
            search_query=search_query,
            search_fields=['full_name', 'application_no', 'email'],
            sort_by='applied_date',
            order='desc'
        )
        for app in res['items']:
            course = self.course_repo.find_by_id(app.get('course_id'))
            app['course_name'] = course.get('name') if course else 'N/A'
        return res

    def apply(self, data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        email = data.get('email', '').strip().lower()
        full_name = data.get('full_name', '').strip()
        if not email or not full_name:
            return False, "Full Name and Email are required.", None

        count = self.admission_repo.count() + 1
        app_no = f"APP-2026-{count:04d}"
        app_data = {
            'id': f"adm-{count:04d}",
            'application_no': app_no,
            'full_name': full_name,
            'email': email,
            'phone': data.get('phone', ''),
            'course_id': data.get('course_id', ''),
            'status': Config.STATUS_APPLIED,
            'applied_date': data.get('applied_date', '2026-08-01'),
            'remarks': 'Application submitted'
        }
        created = self.admission_repo.create(app_data)
        return True, f"Application {app_no} submitted successfully.", created

    def update_status(self, admission_id: str, new_status: str, remarks: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        app = self.admission_repo.find_by_id(admission_id)
        if not app:
            return False, "Admission record not found."

        self.admission_repo.update(admission_id, {'status': new_status, 'remarks': remarks})
        self.audit_repo.log_action(actor_email, actor_role, 'UPDATE_ADMISSION_STATUS', 'ADMISSION', f"Updated admission {admission_id} to status {new_status}")
        return True, f"Application status updated to {new_status}."

    def enroll_applicant(self, admission_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        app = self.admission_repo.find_by_id(admission_id)
        if not app:
            return False, "Admission record not found."
        if app.get('status') not in [Config.STATUS_APPROVED, 'APPROVED']:
            return False, "Applicant must be APPROVED before enrollment."

        email = app['email']
        full_name = app['full_name']

        if self.user_repo.find_by_email(email):
            self.admission_repo.update(admission_id, {'status': Config.STATUS_ENROLLED})
            return True, f"Applicant {full_name} enrolled successfully."

        user_count = self.user_repo.count() + 1
        username = email.split('@')[0]
        user_data = {
            'id': f"usr-std-{user_count:04d}",
            'username': username,
            'email': email,
            'password': PasswordSecurity.hash_password('student123'),
            'role': Config.ROLE_STUDENT,
            'full_name': full_name,
            'status': 'ACTIVE',
            'created_at': '2026-08-31'
        }
        self.user_repo.create(user_data)

        std_count = self.student_repo.count() + 1
        student_id_code = IDGenerator.generate_student_id(std_count)
        student_data = {
            'id': f"std-{std_count:04d}",
            'student_id': student_id_code,
            'user_id': user_data['id'],
            'full_name': full_name,
            'email': email,
            'course_id': app.get('course_id', ''),
            'class_name': 'CS-101',
            'section': 'A',
            'semester': 1,
            'academic_year': '2026',
            'status': 'ACTIVE',
            'enrollment_date': '2026-08-31'
        }
        self.student_repo.create(student_data)
        self.admission_repo.update(admission_id, {'status': Config.STATUS_ENROLLED})
        self.audit_repo.log_action(actor_email, actor_role, 'ENROLL_APPLICANT', 'ADMISSION', f"Enrolled applicant {admission_id} as student {student_id_code}")
        return True, f"Applicant {full_name} enrolled successfully as Student {student_id_code}."
