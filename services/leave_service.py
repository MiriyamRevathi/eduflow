from typing import Optional, Dict, Any, List, Tuple
from repositories.leave_repository import LeaveRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils
import uuid

class LeaveService:
    def __init__(self):
        self.leave_repo = LeaveRepository()
        self.audit_repo = AuditRepository()

    def get_all_leaves(self) -> List[Dict[str, Any]]:
        return self.leave_repo.find_all()

    def apply_leave(self, data: Dict[str, Any], actor_id: str, actor_name: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        leave_type = data.get('leave_type', 'Sick Leave')
        reason = data.get('reason', '').strip()

        if not reason:
            return False, "Leave reason is required.", None

        leave_record = {
            'id': str(uuid.uuid4()),
            'applicant_id': actor_id,
            'applicant_name': actor_name,
            'role': actor_role,
            'leave_type': leave_type,
            'start_date': data.get('start_date', DateTimeUtils.current_date_str()),
            'end_date': data.get('end_date', DateTimeUtils.current_date_str()),
            'reason': reason,
            'status': 'PENDING',
            'approved_by': None,
            'created_at': DateTimeUtils.current_date_str()
        }

        created = self.leave_repo.create(leave_record)
        self.audit_repo.log_action(actor_name, actor_role, 'APPLY_LEAVE', 'LEAVE', f"Submitted leave request for {leave_type}")
        return True, "Leave application submitted successfully.", created

    def update_leave_status(self, leave_id: str, new_status: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        leave = self.leave_repo.find_by_id(leave_id)
        if not leave:
            return False, "Leave application not found."

        self.leave_repo.update(leave_id, {'status': new_status, 'approved_by': actor_email})
        self.audit_repo.log_action(actor_email, actor_role, 'APPROVE_LEAVE', 'LEAVE', f"Updated leave status to {new_status}")
        return True, f"Leave application status updated to {new_status}."
