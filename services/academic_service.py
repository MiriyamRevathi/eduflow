from typing import Optional, Dict, Any, List, Tuple
from repositories.course_repository import CourseRepository
from repositories.subject_repository import SubjectRepository
from repositories.audit_repository import AuditRepository
import uuid

class AcademicService:
    def __init__(self):
        self.course_repo = CourseRepository()
        self.subject_repo = SubjectRepository()
        self.audit_repo = AuditRepository()

    def get_all_courses_with_subjects((self)) -> List[Dict[str, Any]]:
        courses = self.course_repo.find_all()
        for c in courses:
            c['subjects'] = self.subject_repo.find_by_course(c['id'])
        return courses

    def create_course(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        code = data.get('code', '').strip().upper()
        name = data.get('name', '').strip()

        if not code or not name:
            return False, "Course Code and Name are required.", None

        if self.course_repo.find_by_code(code):
            return False, "A course with this code already exists.", None

        course_data = {
            'id': f"crs-{uuid.uuid4().hex[:6]}",
            'code': code,
            'name': name,
            'department': data.get('department', 'General'),
            'duration_years': int(data.get('duration_years', 4)),
            'total_semesters': int(data.get('total_semesters', 8)),
            'status': 'ACTIVE'
        }

        created = self.course_repo.create(course_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_COURSE', 'ACADEMICS', f"Created course {code} - {name}")
        return True, f"Course {name} ({code}) created successfully.", created

    def create_subject(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        code = data.get('code', '').strip().upper()
        name = data.get('name', '').strip()

        if not code or not name:
            return False, "Subject Code and Name are required.", None

        subject_data = {
            'id': f"sbj-{uuid.uuid4().hex[:6]}",
            'code': code,
            'name': name,
            'course_id': data.get('course_id', ''),
            'credits': int(data.get('credits', 3)),
            'semester': int(data.get('semester', 1))
        }

        created = self.subject_repo.create(subject_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_SUBJECT', 'ACADEMICS', f"Created subject {code} - {name}")
        return True, f"Subject {name} ({code}) created successfully.", created
