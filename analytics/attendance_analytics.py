"""
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
