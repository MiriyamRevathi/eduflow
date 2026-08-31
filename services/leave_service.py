"""
EduFlow ERP Service — LeaveService
Student and staff leave application, review, and approval workflow.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.leave_repository import LeaveRepository
from repositories.audit_repository import AuditRepository

class LeaveService:
    def __init__(self):
        self.leave_repo = LeaveRepository()
        self.repo = self.leave_repo
        self.audit_repo = AuditRepository()

    def get_all_leaves(self) -> List[Dict[str, Any]]:
        return self.leave_repo.find_all()

    def apply_leave(self, data: Dict[str, Any], actor_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        leave_type = data.get('leave_type', '').strip()
        start_date = data.get('start_date', '').strip()
        end_date = data.get('end_date', '').strip()
        reason = data.get('reason', '').strip()
        if not leave_type or not start_date or not end_date:
            return False, "Leave Type, Start Date, and End Date are required.", None

        count = self.leave_repo.count() + 1
        leave_data = {
            'id': f"lve-{count:04d}",
            'applicant_id': actor_id,
            'applicant_name': data.get('applicant_name', actor_email),
            'applicant_role': actor_role,
            'leave_type': leave_type,
            'start_date': start_date,
            'end_date': end_date,
            'reason': reason,
            'status': 'PENDING',
            'applied_at': '2026-08-31'
        }
        created = self.leave_repo.create(leave_data)
        self.audit_repo.log_action(actor_email, actor_role, 'APPLY_LEAVE', 'LEAVE', f"Submitted leave request {created['id']}")
        return True, "Leave application submitted successfully.", created

    def update_leave_status(self, leave_id: str, status: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        leave = self.leave_repo.find_by_id(leave_id)
        if not leave:
            return False, "Leave application not found."

        self.leave_repo.update(leave_id, {'status': status, 'reviewed_by': actor_email})
        self.audit_repo.log_action(actor_email, actor_role, 'UPDATE_LEAVE_STATUS', 'LEAVE', f"Updated leave {leave_id} to status {status}")
        return True, f"Leave application {status} successfully."
