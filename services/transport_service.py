"""
EduFlow ERP Service — TransportService
Bus route management, vehicle fleet capacity, and student commute passes.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.transport_repository import TransportRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
import uuid

class TransportService:
    def __init__(self):
        self.transport_repo = TransportRepository()
        self.repo = self.transport_repo
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_all_routes(self) -> List[Dict[str, Any]]:
        return self.transport_repo.find_all()

    def create_route(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        route_name = data.get('route_name', '').strip()
        vehicle_no = data.get('vehicle_no', '').strip()
        if not route_name or not vehicle_no:
            return False, "Route Name and Vehicle Number are required.", None

        count = self.transport_repo.count() + 1
        route_data = {
            'id': f"route-{count:03d}",
            'route_name': route_name,
            'vehicle_no': vehicle_no,
            'driver_name': data.get('driver_name', ''),
            'driver_phone': data.get('driver_phone', ''),
            'capacity': int(data.get('capacity', 40)),
            'allocated_students': [],
            'status': 'ACTIVE'
        }
        created = self.transport_repo.create(route_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_ROUTE', 'TRANSPORT', f"Created route {route_name}")
        return True, "Transport route created successfully.", created

    def assign_student(self, route_id: str, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        if not route_id or not student_id:
            return False, "Route and Student are required."
        success, msg = self.transport_repo.assign_student(route_id, student_id)
        if success:
            self.audit_repo.log_action(actor_email, actor_role, 'ASSIGN_TRANSPORT_ROUTE', 'TRANSPORT', f"Assigned student {student_id} to route {route_id}")
        return success, msg
