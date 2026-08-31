from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class AssignmentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.ASSIGNMENTS_FILE, id_field='id')

    def find_by_course(self, course_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('course_id', course_id)

    def find_by_subject(self, subject_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('subject_id', subject_id)
