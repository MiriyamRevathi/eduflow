from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class MarksRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.MARKS_FILE, id_field='id')

    def find_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)

    def find_by_exam(self, exam_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('exam_id', exam_id)

    def find_by_student_and_exam(self, student_id: str, exam_id: str) -> Optional[Dict[str, Any]]:
        records = self.find_where({'student_id': student_id, 'exam_id': exam_id})
        return records[0] if records else None
