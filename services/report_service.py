from typing import List, Dict, Any
from repositories.student_repository import StudentRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.exam_repository import ExamRepository
from repositories.fee_repository import FeeRepository
from reporting.csv_exporter import CSVExporter

class ReportService:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.attendance_repo = AttendanceRepository()
        self.exam_repo = ExamRepository()
        self.fee_repo = FeeRepository()

    def export_students_csv(self) -> str:
        students = self.student_repo.find_all()
        fields = ['student_id', 'full_name', 'email', 'class_name', 'section', 'academic_year', 'status']
        return CSVExporter.export_to_csv(students, fields)

    def export_attendance_csv(self) -> str:
        att = self.attendance_repo.find_all()
        fields = ['date', 'class_name', 'section', 'student_id', 'status', 'remarks']
        return CSVExporter.export_to_csv(att, fields)

    def export_exams_csv(self) -> str:
        exams = self.exam_repo.find_all()
        fields = ['exam_id', 'title', 'exam_date', 'start_time', 'end_time', 'room', 'max_marks', 'status']
        return CSVExporter.export_to_csv(exams, fields)

    def export_fees_csv(self) -> str:
        fees = self.fee_repo.find_all()
        fields = ['fee_code', 'title', 'total_amount', 'paid_amount', 'pending_amount', 'due_date', 'status']
        return CSVExporter.export_to_csv(fees, fields)
