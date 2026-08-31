"""
EduFlow ERP Service — HostelService
Hostel building management, room bed allocation, and occupant tracking.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.hostel_repository import HostelRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils
import uuid

class HostelService:
    def __init__(self):
        self.hostel_repo = HostelRepository()
        self.repo = self.hostel_repo
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_all(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        return self.hostel_repo.find_all()

    def get_hostels_summary(self) -> List[Dict[str, Any]]:
        return self.hostel_repo.get_hostels_summary()

    def allocate_bed(self, hostel_id: str, room_no: str, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        if not hostel_id or not room_no or not student_id:
            return False, "Hostel, Room Number, and Student are required."
        success, msg = self.hostel_repo.allocate_bed(hostel_id, room_no, student_id)
        if success:
            self.audit_repo.log_action(actor_email, actor_role, 'ALLOCATE_HOSTEL_BED', 'HOSTEL', f"Allocated bed in hostel {hostel_id} room {room_no} to student {student_id}")
        return success, msg

    def get_dashboard_summary(self) -> Dict[str, Any]:
        return self.hostel_repo.get_summary_stats()
