from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class FeeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.FEES_FILE, id_field='id')

    def find_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)

    def find_pending_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        records = self.find_by_student(student_id)
        return [r for r in records if r.get('status') in ['PENDING', 'PARTIAL']]
