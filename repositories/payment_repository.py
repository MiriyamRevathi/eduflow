from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class PaymentRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.PAYMENTS_FILE, id_field='id')

    def find_by_fee_id(self, fee_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('fee_id', fee_id)

    def find_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)
