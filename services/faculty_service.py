from typing import Optional, Dict, Any, List, Tuple
from repositories.teacher_repository import TeacherRepository
from repositories.user_repository import UserRepository
from repositories.subject_repository import SubjectRepository
from repositories.timetable_repository import TimetableRepository
from repositories.audit_repository import AuditRepository
from utils.id_generator import IDGenerator
from security.password import PasswordSecurity
from config import Config

class FacultyService:
    def __init__(self):
        self.teacher_repo = TeacherRepository()
        self.user_repo = UserRepository()
        self.subject_repo = SubjectRepository()
        self.timetable_repo = TimetableRepository()
        self.audit_repo = AuditRepository()

    def get_paginated_faculty(self, page: int = 1, per_page: int = 10, search_query: str = None, department: str = None) -> Dict[str, Any]:
        criteria = {}
        if department:
            criteria['department'] = department

        result = self.teacher_repo.paginate(
            page=page,
            per_page=per_page,
            criteria=criteria,
            search_query=search_query,
            search_fields=['full_name', 'faculty_id', 'email', 'department', 'designation'],
            sort_by='faculty_id',
            order='asc'
        )

        for teacher in result['items']:
            assigned_sub_ids = teacher.get('assigned_subject_ids', [])
            teacher['subjects'] = [self.subject_repo.find_by_id(s_id) for s_id in assigned_sub_ids if self.subject_repo.find_by_id(s_id)]

        return result

    def get_faculty_profile(self, teacher_id: str) -> Optional[Dict[str, Any]]:
        teacher = self.teacher_repo.find_by_id(teacher_id)
        if not teacher:
            return None

        # Subjects
        assigned_sub_ids = teacher.get('assigned_subject_ids', [])
        teacher['subjects'] = [self.subject_repo.find_by_id(s_id) for s_id in assigned_sub_ids if self.subject_repo.find_by_id(s_id)]

        # Timetable slots
        teacher['timetable'] = self.timetable_repo.find_by_teacher(teacher_id)

        return teacher

    def create_faculty(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        email = data.get('email', '').strip().lower()
        full_name = data.get('full_name', '').strip()

        if not email or not full_name:
            return False, "Full Name and Email are required.", None

        if self.user_repo.find_by_email(email):
            return False, "A user with this email address already exists.", None

        # 1. User
        user_count = self.user_repo.count() + 1
        username = email.split('@')[0]
        role = data.get('role', Config.ROLE_TEACHER)
        user_data = {
            'id': f"usr-fac-{user_count:04d}",
            'username': username,
            'email': email,
            'password': PasswordSecurity.hash_password('teacher123'),
            'role': role,
            'full_name': full_name,
            'status': 'ACTIVE',
            'created_at': '2026-01-01 09:00:00'
        }
        self.user_repo.create(user_data)

        # 2. Teacher Record
        t_count = self.teacher_repo.count() + 1
        faculty_id_code = IDGenerator.generate_faculty_id(t_count)
        teacher_data = {
            'id': f"tch-{t_count:04d}",
            'faculty_id': faculty_id_code,
            'user_id': user_data['id'],
            'full_name': full_name,
            'email': email,
            'phone': data.get('phone', ''),
            'department': data.get('department', 'Computer Science'),
            'designation': data.get('designation', 'Professor'),
            'assigned_subject_ids': data.get('assigned_subject_ids', []),
            'assigned_classes': data.get('assigned_classes', []),
            'status': 'ACTIVE'
        }

        created = self.teacher_repo.create(teacher_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_FACULTY', 'FACULTY', f"Created faculty member {faculty_id_code} - {full_name}")
        return True, f"Faculty member {full_name} ({faculty_id_code}) added successfully.", created

    def update_faculty(self, teacher_id: str, updates: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str]:
        teacher = self.teacher_repo.find_by_id(teacher_id)
        if not teacher:
            return False, "Faculty record not found."

        self.teacher_repo.update(teacher_id, updates)
        if 'full_name' in updates and teacher.get('user_id'):
            self.user_repo.update(teacher['user_id'], {'full_name': updates['full_name']})

        self.audit_repo.log_action(actor_email, actor_role, 'UPDATE_FACULTY', 'FACULTY', f"Updated faculty member {teacher_id}")
        return True, "Faculty record updated successfully."

    def delete_faculty(self, teacher_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        teacher = self.teacher_repo.find_by_id(teacher_id)
        if not teacher:
            return False, "Faculty member not found."

        self.teacher_repo.update(teacher_id, {'status': 'INACTIVE'})
        if teacher.get('user_id'):
            self.user_repo.update(teacher['user_id'], {'status': 'INACTIVE'})

        self.audit_repo.log_action(actor_email, actor_role, 'DELETE_FACULTY', 'FACULTY', f"Archived faculty member {teacher_id}")
        return True, "Faculty member status set to INACTIVE."
