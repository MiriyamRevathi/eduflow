from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class HostelRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.HOSTELS_FILE, id_field='id')

    def find_by_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        records = self.find_all()
        for h in records:
            rooms = h.get('rooms', [])
            for r in rooms:
                allocations = r.get('allocations', [])
                for a in allocations:
                    if a.get('student_id') == student_id:
                        return {'hostel': h, 'room': r, 'allocation': a}
        return None
