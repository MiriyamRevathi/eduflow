from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class AdmissionRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.ADMISSIONS_FILE, id_field='id')

    def find_by_application_number(self, application_no: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('application_no', application_no)

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        return self.find_by_field('status', status)
