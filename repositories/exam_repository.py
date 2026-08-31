from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class ExamRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.EXAMS_FILE, id_field='id')

    def find_by_course(self, course_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('course_id', course_id)
