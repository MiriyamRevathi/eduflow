from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class LeaveRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.LEAVE_FILE, id_field='id')

    def find_by_applicant(self, applicant_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('applicant_id', applicant_id)

    def find_pending(self) -> List[Dict[str, Any]]:
        return self.find_by_field('status', 'PENDING')
