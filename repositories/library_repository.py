from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class LibraryRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.LIBRARY_FILE, id_field='id')

    def find_issued_to_student(self, student_id: str) -> List[Dict[str, Any]]:
        records = self.find_by_field('student_id', student_id)
        return [r for r in records if r.get('status') == 'ISSUED']

    def find_all_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)
