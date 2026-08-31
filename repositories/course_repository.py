from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class CourseRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.COURSES_FILE, id_field='id')

    def find_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('code', code)
