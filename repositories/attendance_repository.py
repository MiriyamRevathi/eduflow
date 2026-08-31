from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class AttendanceRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.ATTENDANCE_FILE, id_field='id')

    def find_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)

    def find_by_date(self, date_str: str) -> List[Dict[str, Any]]:
        return self.find_by_field('date', date_str)

    def find_by_student_and_date(self, student_id: str, date_str: str) -> Optional[Dict[str, Any]]:
        records = self.find_where({'student_id': student_id, 'date': date_str})
        return records[0] if records else None

    def get_attendance_percentage(self, student_id: str) -> float:
        records = self.find_by_student(student_id)
        if not records:
            return 100.0
        present_count = sum(1 for r in records if r.get('status') in ['PRESENT', 'LATE', 'EXCUSED'])
        return round((present_count / len(records)) * 100.0, 2)
