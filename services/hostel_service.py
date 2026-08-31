from typing import Optional, Dict, Any, List, Tuple
from repositories.hostel_repository import HostelRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils

class HostelService:
    def __init__(self):
        self.hostel_repo = HostelRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_hostels_summary(self) -> List[Dict[str, Any]]:
        return self.hostel_repo.find_all()

    def allocate_bed(self, hostel_id: str, room_no: str, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        hostel = self.hostel_repo.find_by_id(hostel_id)
        if not hostel:
            return False, "Hostel record not found."

        student = self.student_repo.find_by_id(student_id)
        if not student:
            return False, "Student not found."

        rooms = hostel.get('rooms', [])
        target_room = None
        for r in rooms:
            if r.get('room_no') == room_no:
                target_room = r
                break

        if not target_room:
            return False, f"Room {room_no} does not exist in {hostel['name']}."

        if target_room.get('occupied', 0) >= target_room.get('capacity', 2):
            return False, f"Room {room_no} is fully occupied."

        allocations = target_room.get('allocations', [])
        for a in allocations:
            if a.get('student_id') == student_id:
                return False, "Student is already allocated a bed in this room."

        allocations.append({
            'student_id': student_id,
            'student_name': student.get('full_name'),
            'allocated_at': DateTimeUtils.current_date_str()
        })

        target_room['occupied'] = len(allocations)
        self.hostel_repo.update(hostel_id, {'rooms': rooms})
        self.audit_repo.log_action(actor_email, actor_role, 'ALLOCATE_HOSTEL_BED', 'HOSTEL', f"Allocated bed in room {room_no} of {hostel['name']} to {student['full_name']}")
        return True, f"Bed in Room {room_no} allocated to {student['full_name']} successfully."
