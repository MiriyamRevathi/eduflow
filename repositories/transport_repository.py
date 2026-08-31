from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class TransportRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.TRANSPORT_FILE, id_field='id')

    def find_by_vehicle_number(self, vehicle_number: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('vehicle_number', vehicle_number)

    def find_by_student(self, student_id: str) -> Optional[Dict[str, Any]]:
        records = self.find_all()
        for route in records:
            assigned_students = route.get('assigned_student_ids', [])
            if student_id in assigned_students:
                return route
        return None
