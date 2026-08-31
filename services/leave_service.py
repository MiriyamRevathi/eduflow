"""
EduFlow ERP Enterprise Service — LeaveService
Business logic layer managing data operations, auditing, validation, and analytics for Leave.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.leave_repository import LeaveRepository
from repositories.audit_repository import AuditRepository
from validators.leave_validator import LeaveValidator
from schemas.leave_schema import LeaveSchema
from models.leave import LeaveModel
from utils.datetime_utils import DateTimeUtils
import uuid

class LeaveService:
    def __init__(self):
        self.repo = LeaveRepository()
        self.audit_repo = AuditRepository()
        self.validator = LeaveValidator()
        self.schema = LeaveSchema()

    def get_all(self, status_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        """Retrieve all records with optional status filtering."""
        if status_filter:
            return self.repo.find_by_status(status_filter)
        return self.repo.find_all()

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        """Get single record by primary key."""
        if not item_id:
            return None
        return self.repo.find_by_id(item_id)

    def get_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Find record by unique code string."""
        if not code:
            return None
        return self.repo.find_by_code(code)

    def get_paginated(
        self,
        page: int = 1,
        per_page: int = 10,
        query: Optional[str] = None,
        status: Optional[str] = None,
        sort_by: str = 'id',
        order: str = 'asc'
    ) -> Dict[str, Any]:
        """Fetch paginated records with text query and status filters."""
        return self.repo.get_paginated_filtered(
            page=page,
            per_page=per_page,
            status=status,
            query=query,
            sort_by=sort_by,
            order=order
        )

    def create_record(self, payload: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Create new record with schema sanitization and audit logging."""
        sanitized = self.schema.sanitize_payload(payload)
        is_valid, errors = self.validator.check_integrity(sanitized)
        if not is_valid:
            return False, f"Validation failed: {', '.join(errors)}", None

        if 'id' not in sanitized or not sanitized['id']:
            sanitized['id'] = f"lea-{uuid.uuid4().hex[:6]}"

        if 'status' not in sanitized:
            sanitized['status'] = 'ACTIVE'

        sanitized['created_at'] = DateTimeUtils.current_datetime_str()
        sanitized['updated_at'] = DateTimeUtils.current_datetime_str()
        sanitized['created_by'] = actor_email

        created = self.repo.create(sanitized)
        self.audit_repo.log_action(
            actor_email, actor_role, f"CREATE_LEAVE", m_name.upper(),
            f"Created Leave record ID: {created['id']}"
        )
        return True, f"Leave record created successfully.", created

    def update_record(self, item_id: str, updates: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        """Update existing record with validation checks."""
        existing = self.repo.find_by_id(item_id)
        if not existing:
            return False, f"Leave record not found.", None

        sanitized = self.schema.sanitize_payload(updates)
        sanitized['updated_at'] = DateTimeUtils.current_datetime_str()
        sanitized['updated_by'] = actor_email

        updated = self.repo.update(item_id, sanitized)
        self.audit_repo.log_action(
            actor_email, actor_role, f"UPDATE_LEAVE", m_name.upper(),
            f"Updated Leave record ID: {item_id}"
        )
        return True, f"Leave record updated successfully.", updated

    def archive_record(self, item_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        """Soft delete/archive record."""
        existing = self.repo.find_by_id(item_id)
        if not existing:
            return False, f"Leave record not found."

        self.repo.update(item_id, {'status': 'ARCHIVED', 'updated_at': DateTimeUtils.current_datetime_str()})
        self.audit_repo.log_action(
            actor_email, actor_role, f"ARCHIVE_LEAVE", m_name.upper(),
            f"Archived Leave record ID: {item_id}"
        )
        return True, f"Leave record archived successfully."

    def hard_delete_record(self, item_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        """Permanently delete record from JSON storage."""
        existing = self.repo.find_by_id(item_id)
        if not existing:
            return False, f"Leave record not found."

        success = self.repo.delete(item_id)
        if success:
            self.audit_repo.log_action(
                actor_email, actor_role, f"DELETE_LEAVE", m_name.upper(),
                f"Permanently deleted Leave record ID: {item_id}"
            )
            return True, f"Leave record deleted permanently."
        return False, "Delete operation failed."

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Calculate statistics summary for Leave module."""
        return self.repo.get_summary_stats()

    def export_as_csv_rows(self) -> List[List[str]]:
        """Export collection records as CSV rows."""
        records = self.get_all()
        rows = [['ID', 'Name/Title', 'Code', 'Status', 'Created At']]
        for r in records:
            rows.append([
                str(r.get('id', '')),
                str(r.get('name') or r.get('title') or ''),
                str(r.get('code', '')),
                str(r.get('status', '')),
                str(r.get('created_at', ''))
            ])
        return rows
