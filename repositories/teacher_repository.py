from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class TeacherRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.TEACHERS_FILE, id_field='id')

    def find_by_faculty_id(self, faculty_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('faculty_id', faculty_id)

    def find_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('user_id', user_id)

    def find_by_department(self, department: str) -> List[Dict[str, Any]]:
        return self.find_by_field('department', department)
