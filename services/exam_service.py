"""
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
