from typing import Optional, Dict, Any, List, Tuple
from repositories.student_repository import StudentRepository
from repositories.user_repository import UserRepository
from repositories.course_repository import CourseRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.marks_repository import MarksRepository
from repositories.fee_repository import FeeRepository
from repositories.library_repository import LibraryRepository
from repositories.hostel_repository import HostelRepository
from repositories.transport_repository import TransportRepository
from repositories.leave_repository import LeaveRepository
from repositories.audit_repository import AuditRepository
from utils.id_generator import IDGenerator
from security.password import PasswordSecurity
from config import Config

class StudentService:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.user_repo = UserRepository()
        self.course_repo = CourseRepository()
        self.attendance_repo = AttendanceRepository()
        self.marks_repo = MarksRepository()
        self.fee_repo = FeeRepository()
        self.library_repo = LibraryRepository()
        self.hostel_repo = HostelRepository()
        self.transport_repo = TransportRepository()
        self.leave_repo = LeaveRepository()
        self.audit_repo = AuditRepository()

    def get_paginated_students(self, page: int = 1, per_page: int = 10, search_query: str = None, course_id: str = None, status: str = None) -> Dict[str, Any]:
        criteria = {}
        if course_id:
            criteria['course_id'] = course_id
        if status:
            criteria['status'] = status

        result = self.student_repo.paginate(
            page=page,
            per_page=per_page,
            criteria=criteria,
            search_query=search_query,
            search_fields=['full_name', 'student_id', 'email', 'class_name'],
            sort_by='student_id',
            order='asc'
        )

        # Enhance with course details
        for std in result['items']:
            course = self.course_repo.find_by_id(std.get('course_id'))
            std['course_name'] = course.get('name') if course else 'N/A'
            std['attendance_pct'] = self.attendance_repo.get_attendance_percentage(std['id'])

        return result

    def get_student_full_profile(self, student_id: str) -> Optional[Dict[str, Any]]:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            return None

        # Course details
        course = self.course_repo.find_by_id(student.get('course_id'))
        student['course'] = course

        # Attendance stats
        att_records = self.attendance_repo.find_by_student(student_id)
        student['attendance_records'] = sorted(att_records, key=lambda x: x.get('date', ''), reverse=True)
        student['attendance_pct'] = self.attendance_repo.get_attendance_percentage(student_id)

        # Marks & GPA
        marks = self.marks_repo.find_by_student(student_id)
        student['marks'] = marks
        if marks:
            total_gpa = sum(m.get('gpa', 0) for m in marks)
            student['avg_gpa'] = round(total_gpa / len(marks), 2)
        else:
            student['avg_gpa'] = 0.0

        # Fees
        fees = self.fee_repo.find_by_student(student_id)
        student['fees'] = fees
        student['total_pending_fee'] = sum(f.get('pending_amount', 0) for f in fees)

        # Library
        library_txns = self.library_repo.find_all_by_student(student_id)
        student['library_txns'] = library_txns

        # Hostel
        student['hostel_info'] = self.hostel_repo.find_by_student(student_id)

        # Transport
        student['transport_info'] = self.transport_repo.find_by_student(student_id)

        # Leave history
        student['leaves'] = self.leave_repo.find_by_applicant(student_id)

        return student

    def create_student(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        email = data.get('email', '').strip().lower()
        full_name = data.get('full_name', '').strip()

        if not email or not full_name:
            return False, "Full Name and Email are required.", None

        if self.user_repo.find_by_email(email):
            return False, "A user with this email address already exists.", None

        # 1. Create User Account
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
            'created_at': data.get('enrollment_date', '')
        }
        self.user_repo.create(user_data)

        # 2. Create Student Record
        std_count = self.student_repo.count() + 1
        student_id_code = IDGenerator.generate_student_id(std_count)
        student_data = {
            'id': f"std-{std_count:04d}",
            'student_id': student_id_code,
            'user_id': user_data['id'],
            'full_name': full_name,
            'email': email,
            'phone': data.get('phone', ''),
            'gender': data.get('gender', 'Male'),
            'dob': data.get('dob', ''),
            'course_id': data.get('course_id', ''),
            'class_name': data.get('class_name', 'CS-101'),
            'section': data.get('section', 'A'),
            'semester': int(data.get('semester', 1)),
            'academic_year': data.get('academic_year', '2026'),
            'guardian_name': data.get('guardian_name', ''),
            'guardian_phone': data.get('guardian_phone', ''),
            'address': data.get('address', ''),
            'status': 'ACTIVE',
            'enrollment_date': data.get('enrollment_date', '')
        }

        created = self.student_repo.create(student_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_STUDENT', 'STUDENT', f"Created student {student_id_code} - {full_name}")
        return True, f"Student {full_name} ({student_id_code}) created successfully.", created

    def update_student(self, student_id: str, updates: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str]:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            return False, "Student record not found."

        self.student_repo.update(student_id, updates)
        
        # Also sync full name if changed
        if 'full_name' in updates and student.get('user_id'):
            self.user_repo.update(student['user_id'], {'full_name': updates['full_name']})

        self.audit_repo.log_action(actor_email, actor_role, 'UPDATE_STUDENT', 'STUDENT', f"Updated student {student_id}")
        return True, "Student updated successfully."

    def delete_student(self, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            return False, "Student not found."

        # Soft delete / set to ARCHIVED
        self.student_repo.update(student_id, {'status': 'ARCHIVED'})
        if student.get('user_id'):
            self.user_repo.update(student['user_id'], {'status': 'INACTIVE'})

        self.audit_repo.log_action(actor_email, actor_role, 'DELETE_STUDENT', 'STUDENT', f"Archived student {student_id}")
        return True, "Student record archived successfully."
