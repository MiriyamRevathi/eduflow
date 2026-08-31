from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class StudentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.STUDENTS_FILE, id_field='id')

    def find_by_student_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('student_id', student_id)

    def find_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('user_id', user_id)

    def find_by_course(self, course_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('course_id', course_id)

    def find_by_class_and_section(self, class_name: str, section: str) -> List[Dict[str, Any]]:
        return self.find_where({'class_name': class_name, 'section': section})
