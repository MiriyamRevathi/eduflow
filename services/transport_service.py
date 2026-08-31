from typing import Optional, Dict, Any, List, Tuple
from repositories.transport_repository import TransportRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
import uuid

class TransportService:
    def __init__(self):
        self.transport_repo = TransportRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_all_routes(self) -> List[Dict[str, Any]]:
        return self.transport_repo.find_all()

    def create_route(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        route_name = data.get('route_name', '').strip()
        vehicle_no = data.get('vehicle_number', '').strip().upper()

        if not route_name or not vehicle_no:
            return False, "Route Name and Vehicle Number are required.", None

        if self.transport_repo.find_by_vehicle_number(vehicle_no):
            return False, "Vehicle number already registered.", None

        route_count = self.transport_repo.count() + 1
        stops_raw = data.get('stops', '')
        stops_list = [s.strip() for s in stops_raw.split(',') if s.strip()]

        route_data = {
            'id': f"trn-{route_count:04d}",
            'route_name': route_name,
            'vehicle_number': vehicle_no,
            'driver_name': data.get('driver_name', 'Driver'),
            'driver_phone': data.get('driver_phone', ''),
            'capacity': int(data.get('capacity', 30)),
            'current_capacity': 0,
            'monthly_fee': float(data.get('monthly_fee', 150.0)),
            'stops': stops_list,
            'assigned_student_ids': []
        }

        created = self.transport_repo.create(route_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_TRANSPORT_ROUTE', 'TRANSPORT', f"Created transport route {route_name} ({vehicle_no})")
        return True, f"Transport route {route_name} created.", created

    def assign_student(self, route_id: str, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        route = self.transport_repo.find_by_id(route_id)
        if not route:
            return False, "Transport route not found."

        student = self.student_repo.find_by_id(student_id)
        if not student:
            return False, "Student not found."

        assigned = route.get('assigned_student_ids', [])
        max_cap = int(route.get('capacity', 30))

        if len(assigned) >= max_cap:
            return False, f"Vehicle capacity limit ({max_cap} students) reached. Cannot assign student!"

        if student_id in assigned:
            return False, "Student is already assigned to this transport route."

        assigned.append(student_id)
        self.transport_repo.update(route_id, {
            'assigned_student_ids': assigned,
            'current_capacity': len(assigned)
        })

        self.audit_repo.log_action(actor_email, actor_role, 'ASSIGN_TRANSPORT', 'TRANSPORT', f"Assigned {student['full_name']} to route {route['route_name']}")
        return True, f"Student {student['full_name']} assigned to route {route['route_name']}."
