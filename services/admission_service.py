from typing import Optional, Dict, Any, List, Tuple
from repositories.admission_repository import AdmissionRepository
from repositories.course_repository import CourseRepository
from services.student_service import StudentService
from repositories.audit_repository import AuditRepository
from utils.id_generator import IDGenerator
from utils.datetime_utils import DateTimeUtils

class AdmissionService:
    def __init__(self):
        self.admission_repo = AdmissionRepository()
        self.course_repo = CourseRepository()
        self.student_service = StudentService()
        self.audit_repo = AuditRepository()

    def get_paginated_admissions(self, page: int = 1, per_page: int = 10, search_query: str = None, status: str = None) -> Dict[str, Any]:
        criteria = {}
        if status:
            criteria['status'] = status

        result = self.admission_repo.paginate(
            page=page,
            per_page=per_page,
            criteria=criteria,
            search_query=search_query,
            search_fields=['application_no', 'applicant_name', 'email', 'phone'],
            sort_by='applied_date',
            order='desc'
        )

        for item in result['items']:
            course = self.course_repo.find_by_id(item.get('course_id'))
            item['course_name'] = course.get('name') if course else 'N/A'

        return result

    def apply(self, data: Dict[str, Any]) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        name = data.get('applicant_name', '').strip()
        email = data.get('email', '').strip().lower()

        if not name or not email:
            return False, "Applicant Name and Email are required.", None

        adm_count = self.admission_repo.count() + 1
        app_no = IDGenerator.generate_admission_id(adm_count)

        admission_record = {
            'id': f"adm-{adm_count:04d}",
            'application_no': app_no,
            'applicant_name': name,
            'email': email,
            'phone': data.get('phone', ''),
            'course_id': data.get('course_id', ''),
            'previous_qualification': data.get('previous_qualification', ''),
            'status': 'APPLIED',
            'applied_date': DateTimeUtils.current_date_str(),
            'remarks': data.get('remarks', 'Application submitted.')
        }

        created = self.admission_repo.create(admission_record)
        self.audit_repo.log_action(email, 'APPLICANT', 'ADMISSION_APPLIED', 'ADMISSION', f"Submitted application {app_no}")
        return True, f"Application {app_no} submitted successfully.", created

    def update_status(self, admission_id: str, new_status: str, remarks: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        admission = self.admission_repo.find_by_id(admission_id)
        if not admission:
            return False, "Admission record not found."

        allowed_statuses = ['APPLIED', 'UNDER_REVIEW', 'APPROVED', 'REJECTED', 'WAITLISTED', 'ENROLLED']
        if new_status not in allowed_statuses:
            return False, "Invalid status value."

        self.admission_repo.update(admission_id, {'status': new_status, 'remarks': remarks})
        self.audit_repo.log_action(actor_email, actor_role, 'ADMISSION_STATUS_CHANGE', 'ADMISSION', f"Changed status of {admission['application_no']} to {new_status}")
        return True, f"Status updated to {new_status}."

    def enroll_applicant(self, admission_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        admission = self.admission_repo.find_by_id(admission_id)
        if not admission:
            return False, "Admission record not found."

        if admission.get('status') == 'ENROLLED':
            return False, "Applicant is already enrolled."

        # Convert to real student
        student_payload = {
            'full_name': admission['applicant_name'],
            'email': admission['email'],
            'phone': admission.get('phone', ''),
            'gender': 'Male',
            'dob': '2005-01-01',
            'course_id': admission.get('course_id', ''),
            'class_name': 'CS-101',
            'section': 'A',
            'semester': 1,
            'academic_year': '2026',
            'guardian_name': 'Parent of ' + admission['applicant_name'],
            'guardian_phone': admission.get('phone', ''),
            'address': 'Enrolled via Admissions Pipeline',
            'enrollment_date': DateTimeUtils.current_date_str()
        }

        success, msg, created_std = self.student_service.create_student(student_payload, actor_email, actor_role)
        if success:
            self.admission_repo.update(admission_id, {'status': 'ENROLLED', 'remarks': f"Enrolled as Student ID: {created_std['student_id']}"})
            self.audit_repo.log_action(actor_email, actor_role, 'ENROLL_APPLICANT', 'ADMISSION', f"Enrolled applicant {admission['application_no']} as student {created_std['student_id']}")
            return True, f"Applicant enrolled successfully as Student {created_std['student_id']}."
        else:
            return False, f"Failed to enroll: {msg}"
