import os

def patch_services():
    base = os.path.dirname(os.path.abspath(__file__))

    # 1. Auth Service
    with open(os.path.join(base, 'services', 'auth_service.py'), 'w', encoding='utf-8') as f:
        f.write('''"""
EduFlow ERP Service — AuthService
Authentication, role validation, session security, password hashing, and login audit trails.
"""
from typing import Optional, Dict, Any, Tuple
from repositories.user_repository import UserRepository
from security.password import PasswordSecurity
from security.session import SessionManager
from repositories.audit_repository import AuditRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.audit_repo = AuditRepository()

    def authenticate(self, email: str, plain_password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        if not email or not plain_password:
            return False, "Email and password credentials are required.", None

        user = self.user_repo.find_by_email(email)
        if not user:
            return False, "Invalid email address or password.", None

        if user.get('status') != 'ACTIVE':
            return False, "Account deactivated. Contact system administrator.", None

        if not PasswordSecurity.verify_password(plain_password, user.get('password')):
            return False, "Invalid email address or password.", None

        SessionManager.login_user(user)
        self.audit_repo.log_action(user['email'], user['role'], 'USER_LOGIN', 'AUTH', 'User logged in successfully.')
        return True, "Login successful.", user

    def logout(self):
        email = SessionManager.get_current_user_email()
        role = SessionManager.get_current_role()
        if email:
            self.audit_repo.log_action(email, role or 'UNKNOWN', 'USER_LOGOUT', 'AUTH', 'User logged out.')
        SessionManager.logout_user()

    def change_password(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return False, "User account not found."

        if not PasswordSecurity.verify_password(old_password, user.get('password')):
            return False, "Incorrect current password."

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long."

        hashed_pwd = PasswordSecurity.hash_password(new_password)
        self.user_repo.update(user_id, {'password': hashed_pwd})
        self.audit_repo.log_action(user['email'], user['role'], 'PASSWORD_CHANGE', 'USER', 'Password updated successfully.')
        return True, "Password changed successfully."
''')

    # 2. Student Service
    with open(os.path.join(base, 'services', 'student_service.py'), 'w', encoding='utf-8') as f:
        f.write('''"""
EduFlow ERP Service — StudentService
Student profiles, academic history, attendance summary, fee status, and parent association.
"""
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

        for std in result['items']:
            course = self.course_repo.find_by_id(std.get('course_id'))
            std['course_name'] = course.get('name') if course else 'N/A'
            std['attendance_pct'] = self.attendance_repo.get_attendance_percentage(std['id'])

        return result

    def get_student_full_profile(self, student_id: str) -> Optional[Dict[str, Any]]:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            return None

        course = self.course_repo.find_by_id(student.get('course_id'))
        student['course'] = course

        att_records = self.attendance_repo.find_by_student(student_id)
        student['attendance_records'] = sorted(att_records, key=lambda x: x.get('date', ''), reverse=True)
        student['attendance_pct'] = self.attendance_repo.get_attendance_percentage(student_id)

        marks = self.marks_repo.find_by_student(student_id)
        student['marks'] = marks
        if marks:
            total_gpa = sum(m.get('gpa', 0) for m in marks)
            student['avg_gpa'] = round(total_gpa / len(marks), 2)
        else:
            student['avg_gpa'] = 0.0

        fees = self.fee_repo.find_by_student(student_id)
        student['fees'] = fees
        student['total_pending_fee'] = sum(f.get('pending_amount', 0) for f in fees)

        library_txns = self.library_repo.find_all_by_student(student_id)
        student['library_txns'] = library_txns

        student['hostel_info'] = self.hostel_repo.find_by_student(student_id)
        student['transport_info'] = self.transport_repo.find_by_student(student_id)
        student['leaves'] = self.leave_repo.find_by_applicant(student_id)

        return student

    def create_student(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        email = data.get('email', '').strip().lower()
        full_name = data.get('full_name', '').strip()

        if not email or not full_name:
            return False, "Full Name and Email are required.", None

        if self.user_repo.find_by_email(email):
            return False, "A user with this email address already exists.", None

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
        if 'full_name' in updates and student.get('user_id'):
            self.user_repo.update(student['user_id'], {'full_name': updates['full_name']})

        self.audit_repo.log_action(actor_email, actor_role, 'UPDATE_STUDENT', 'STUDENT', f"Updated student {student_id}")
        return True, "Student updated successfully."

    def delete_student(self, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        student = self.student_repo.find_by_id(student_id)
        if not student:
            return False, "Student not found."

        self.student_repo.update(student_id, {'status': 'ARCHIVED'})
        if student.get('user_id'):
            self.user_repo.update(student['user_id'], {'status': 'INACTIVE'})

        self.audit_repo.log_action(actor_email, actor_role, 'DELETE_STUDENT', 'STUDENT', f"Archived student {student_id}")
        return True, "Student record archived successfully."
''')

    # 3. Attendance Service
    with open(os.path.join(base, 'services', 'attendance_service.py'), 'w', encoding='utf-8') as f:
        f.write('''"""
EduFlow ERP Service — AttendanceService
Daily & bulk classroom attendance marking and analytics.
"""
from typing import Optional, Dict, Any, List, Tuple
import datetime
import uuid
from repositories.attendance_repository import AttendanceRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_attendance_overview(self, date_str: str = None, class_name: str = 'CS-101', section: str = 'A') -> Dict[str, Any]:
        if not date_str:
            date_str = DateTimeUtils.current_date_str()

        students = self.student_repo.find_by_class_and_section(class_name, section)
        attendance_records = self.attendance_repo.find_by_date(date_str)
        att_map = {r['student_id']: r for r in attendance_records}

        student_list = []
        present_cnt = 0
        absent_cnt = 0
        late_cnt = 0
        excused_cnt = 0

        for std in students:
            att = att_map.get(std['id'])
            status = att.get('status') if att else 'PRESENT'
            remarks = att.get('remarks') if att else ''

            if status == 'PRESENT':
                present_cnt += 1
            elif status == 'ABSENT':
                absent_cnt += 1
            elif status == 'LATE':
                late_cnt += 1
            elif status == 'EXCUSED':
                excused_cnt += 1

            student_list.append({
                'student_id': std['id'],
                'student_code': std['student_id'],
                'full_name': std['full_name'],
                'status': status,
                'remarks': remarks,
                'overall_pct': self.attendance_repo.get_attendance_percentage(std['id'])
            })

        total = len(students)
        pct = round((present_cnt + late_cnt + excused_cnt) / total * 100.0, 1) if total > 0 else 100.0

        return {
            'date': date_str,
            'class_name': class_name,
            'section': section,
            'students': student_list,
            'stats': {
                'total': total,
                'present': present_cnt,
                'absent': absent_cnt,
                'late': late_cnt,
                'excused': excused_cnt,
                'attendance_pct': pct
            }
        }

    def save_bulk_attendance(self, date_str: str, class_name: str, section: str, attendance_data: List[Dict[str, Any]], actor_email: str, actor_role: str) -> Tuple[bool, str]:
        if not date_str:
            date_str = DateTimeUtils.current_date_str()

        for item in attendance_data:
            student_id = item.get('student_id')
            status = item.get('status', 'PRESENT')
            remarks = item.get('remarks', '')

            existing = self.attendance_repo.find_by_student_and_date(student_id, date_str)
            if existing:
                self.attendance_repo.update(existing['id'], {'status': status, 'remarks': remarks})
            else:
                new_record = {
                    'id': str(uuid.uuid4()),
                    'student_id': student_id,
                    'class_name': class_name,
                    'section': section,
                    'date': date_str,
                    'status': status,
                    'remarks': remarks
                }
                self.attendance_repo.create(new_record)

        self.audit_repo.log_action(actor_email, actor_role, 'MARK_ATTENDANCE', 'ATTENDANCE', f"Marked bulk attendance for {class_name}-{section} on {date_str}")
        return True, f"Attendance for {class_name}-{section} on {date_str} saved successfully."
''')

    # 4. Exam Service
    with open(os.path.join(base, 'services', 'exam_service.py'), 'w', encoding='utf-8') as f:
        f.write('''"""
EduFlow ERP Service — ExamService
Examination scheduling, marks entry, GPA and grade calculation engine.
"""
from typing import Optional, Dict, Any, List, Tuple
import uuid
from repositories.exam_repository import ExamRepository
from repositories.marks_repository import MarksRepository
from repositories.student_repository import StudentRepository
from repositories.course_repository import CourseRepository
from repositories.subject_repository import SubjectRepository
from repositories.audit_repository import AuditRepository
from utils.id_generator import IDGenerator

class ExamService:
    def __init__(self):
        self.exam_repo = ExamRepository()
        self.marks_repo = MarksRepository()
        self.student_repo = StudentRepository()
        self.course_repo = CourseRepository()
        self.subject_repo = SubjectRepository()
        self.audit_repo = AuditRepository()

    def get_all_exams(self) -> List[Dict[str, Any]]:
        exams = self.exam_repo.find_all()
        for e in exams:
            course = self.course_repo.find_by_id(e.get('course_id'))
            subject = self.subject_repo.find_by_id(e.get('subject_id'))
            e['course_name'] = course.get('name') if course else 'N/A'
            e['subject_name'] = subject.get('name') if subject else 'N/A'
        return exams

    def create_exam(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        title = data.get('title', '').strip()
        if not title:
            return False, "Exam title is required.", None

        exam_count = self.exam_repo.count() + 1
        exam_code = IDGenerator.generate_exam_id(exam_count)

        exam_data = {
            'id': f"exm-{exam_count:04d}",
            'exam_id': exam_code,
            'title': title,
            'course_id': data.get('course_id', ''),
            'subject_id': data.get('subject_id', ''),
            'exam_date': data.get('exam_date', ''),
            'start_time': data.get('start_time', '09:00'),
            'end_time': data.get('end_time', '12:00'),
            'room': data.get('room', 'Main Hall'),
            'max_marks': float(data.get('max_marks', 100)),
            'pass_marks': float(data.get('pass_marks', 40)),
            'status': 'SCHEDULED'
        }

        created = self.exam_repo.create(exam_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_EXAM', 'EXAMINATIONS', f"Created exam {exam_code} - {title}")
        return True, f"Exam {title} ({exam_code}) scheduled successfully.", created

    @staticmethod
    def calculate_grade_and_gpa(obtained: float, max_marks: float) -> Tuple[str, float, str]:
        if max_marks <= 0:
            return 'F', 0.0, 'FAILED'
        pct = (obtained / max_marks) * 100.0
        if pct >= 90:
            return 'A+', 4.0, 'PASSED'
        elif pct >= 80:
            return 'A', 3.7, 'PASSED'
        elif pct >= 70:
            return 'B', 3.0, 'PASSED'
        elif pct >= 60:
            return 'C', 2.0, 'PASSED'
        elif pct >= 40:
            return 'D', 1.0, 'PASSED'
        else:
            return 'F', 0.0, 'FAILED'

    def save_bulk_marks(self, exam_id: str, marks_list: List[Dict[str, Any]], actor_email: str, actor_role: str) -> Tuple[bool, str]:
        exam = self.exam_repo.find_by_id(exam_id)
        if not exam:
            return False, "Exam record not found."

        max_marks = float(exam.get('max_marks', 100))
        for item in marks_list:
            std_id = item['student_id']
            obtained = float(item.get('marks_obtained', 0))
            grade, gpa, status = self.calculate_grade_and_gpa(obtained, max_marks)

            existing = self.marks_repo.find_by_student_and_exam(std_id, exam_id)
            if existing:
                self.marks_repo.update(existing['id'], {
                    'marks_obtained': obtained,
                    'max_marks': max_marks,
                    'grade': grade,
                    'gpa': gpa,
                    'status': status,
                    'remarks': item.get('remarks', '')
                })
            else:
                mark_record = {
                    'id': str(uuid.uuid4()),
                    'exam_id': exam_id,
                    'student_id': std_id,
                    'subject_id': exam.get('subject_id'),
                    'marks_obtained': obtained,
                    'max_marks': max_marks,
                    'grade': grade,
                    'gpa': gpa,
                    'status': status,
                    'remarks': item.get('remarks', '')
                }
                self.marks_repo.create(mark_record)

        self.exam_repo.update(exam_id, {'status': 'COMPLETED'})
        self.audit_repo.log_action(actor_email, actor_role, 'SUBMIT_MARKS', 'EXAMINATIONS', f"Submitted marks for exam {exam.get('exam_id')}")
        return True, "Marks submitted and GPA results published successfully."
''')

    # 5. Fee Service
    with open(os.path.join(base, 'services', 'fee_service.py'), 'w', encoding='utf-8') as f:
        f.write('''"""
EduFlow ERP Service — FeeService
Fee invoices, discount calculations, partial payment handling, and receipt generation.
"""
from typing import Optional, Dict, Any, List, Tuple
import uuid
from repositories.fee_repository import FeeRepository
from repositories.payment_repository import PaymentRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.id_generator import IDGenerator
from utils.datetime_utils import DateTimeUtils

class FeeService:
    def __init__(self):
        self.fee_repo = FeeRepository()
        self.payment_repo = PaymentRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_all_fees(self) -> List[Dict[str, Any]]:
        fees = self.fee_repo.find_all()
        for f in fees:
            student = self.student_repo.find_by_id(f.get('student_id'))
            f['student_name'] = student.get('full_name') if student else 'N/A'
            f['student_code'] = student.get('student_id') if student else 'N/A'
        return fees

    def create_fee_invoice(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        student_id = data.get('student_id')
        title = data.get('title', '').strip()
        total_amount = float(data.get('total_amount', 0))
        discount_amount = float(data.get('discount_amount', 0))

        if not student_id or not title or total_amount <= 0:
            return False, "Student, Invoice Title, and valid Amount are required.", None

        net_amount = max(0.0, total_amount - discount_amount)
        fee_count = self.fee_repo.count() + 1
        fee_code = IDGenerator.generate_fee_id(fee_count)

        fee_record = {
            'id': f"fee-{fee_count:04d}",
            'fee_code': fee_code,
            'student_id': student_id,
            'title': title,
            'total_amount': total_amount,
            'discount_amount': discount_amount,
            'net_amount': net_amount,
            'paid_amount': 0.0,
            'pending_amount': net_amount,
            'due_date': data.get('due_date', DateTimeUtils.current_date_str()),
            'status': 'PENDING'
        }

        created = self.fee_repo.create(fee_record)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_FEE_INVOICE', 'FEES', f"Created fee invoice {fee_code} for ${net_amount}")
        return True, f"Fee invoice {fee_code} created successfully.", created

    def process_payment(self, fee_id: str, amount: float, method: str, ref: str, actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        fee = self.fee_repo.find_by_id(fee_id)
        if not fee:
            return False, "Fee record not found.", None

        if amount <= 0:
            return False, "Payment amount must be greater than zero.", None

        pending = float(fee.get('pending_amount', 0))
        if amount > pending:
            return False, f"Payment amount exceeds outstanding balance of ${pending:.2f}.", None

        new_paid = float(fee.get('paid_amount', 0)) + amount
        new_pending = pending - amount
        new_status = 'PAID' if new_pending <= 0.01 else 'PARTIAL'

        self.fee_repo.update(fee_id, {
            'paid_amount': round(new_paid, 2),
            'pending_amount': round(new_pending, 2),
            'status': new_status
        })

        pay_count = self.payment_repo.count() + 1
        pay_code = IDGenerator.generate_payment_id(pay_count)

        payment_record = {
            'id': f"pay-{pay_count:05d}",
            'payment_code': pay_code,
            'fee_id': fee_id,
            'student_id': fee.get('student_id'),
            'amount': amount,
            'payment_method': method,
            'transaction_ref': ref or 'SIMULATED-TXN',
            'payment_date': DateTimeUtils.current_datetime_str(),
            'receipt_no': f"RCP-2026-{pay_count:03d}",
            'remarks': f"Simulated {method} payment of ${amount:.2f}"
        }

        created_pay = self.payment_repo.create(payment_record)
        self.audit_repo.log_action(actor_email, actor_role, 'FEE_PAYMENT', 'FEES', f"Processed ${amount:.2f} payment for fee {fee.get('fee_code')} via {method}")
        return True, f"Payment of ${amount:.2f} processed successfully. Receipt {created_pay['receipt_no']} issued.", created_pay
''')

    print("Specialized services patched.")

if __name__ == '__main__':
    patch_services()
