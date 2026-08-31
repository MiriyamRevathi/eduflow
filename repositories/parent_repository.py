from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class ParentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.PARENTS_FILE, id_field='id')

    def find_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('user_id', user_id)

    def find_by_student_id(self, student_id: str) -> List[Dict[str, Any]]:
        parents = self.find_all()
        results = []
        for p in parents:
            student_ids = p.get('student_ids', [])
            if student_id in student_ids or p.get('student_id') == student_id:
                results.append(p)
        return results
