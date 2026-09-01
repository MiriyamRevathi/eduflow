"""
EduFlow ERP Service — InstitutionService
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.institution_repository import InstitutionRepository
from repositories.audit_repository import AuditRepository
from validators.institution_validator import InstitutionValidator
from schemas.institution_schema import InstitutionSchema
from utils.datetime_utils import DateTimeUtils
import uuid

class InstitutionService:
    def __init__(self):
        self.repo = InstitutionRepository()
        self.audit_repo = AuditRepository()
        self.validator = InstitutionValidator()
        self.schema = InstitutionSchema()

    def get_all(self, status_filter: Optional[str] = None, type_filter: Optional[str] = None) -> List[Dict[str, Any]]:
        records = self.repo.find_all()
        if status_filter:
            records = [r for r in records if r.get('status') == status_filter]
        if type_filter:
            records = [r for r in records if r.get('type') == type_filter]
        return records

    def get_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        return self.repo.find_by_id(item_id)

    def create_institution(self, payload: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        sanitized = self.schema.sanitize_payload(payload)
        is_valid, errors = self.validator.check_integrity(sanitized)
        if not is_valid:
            return False, f"Validation failed: {', '.join(errors)}", None

        count = self.repo.count() + 1
        inst_id = f"inst-{count:03d}"
        code = sanitized.get('code') or f"INS-{count:03d}"

        sanitized['id'] = inst_id
        sanitized['code'] = code
        sanitized['status'] = sanitized.get('status', 'ACTIVE')
        sanitized['students_count'] = int(sanitized.get('students_count', 0))
        sanitized['faculty_count'] = int(sanitized.get('faculty_count', 0))
        sanitized['attendance_rate'] = float(sanitized.get('attendance_rate', 95.0))
        sanitized['fee_collection'] = float(sanitized.get('fee_collection', 0.0))
        sanitized['pending_fees'] = float(sanitized.get('pending_fees', 0.0))
        sanitized['created_at'] = DateTimeUtils.current_datetime_str()

        created = self.repo.create(sanitized)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_INSTITUTION', 'INSTITUTION', f"Created Institution {created['name']} ({inst_id})")
        return True, f"Institution '{created['name']}' created successfully.", created

    def update_institution(self, item_id: str, updates: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        existing = self.repo.find_by_id(item_id)
        if not existing:
            return False, "Institution record not found.", None

        sanitized = self.schema.sanitize_payload(updates)
        if 'students_count' in sanitized: sanitized['students_count'] = int(sanitized['students_count'])
        if 'faculty_count' in sanitized: sanitized['faculty_count'] = int(sanitized['faculty_count'])
        if 'attendance_rate' in sanitized: sanitized['attendance_rate'] = float(sanitized['attendance_rate'])
        if 'fee_collection' in sanitized: sanitized['fee_collection'] = float(sanitized['fee_collection'])
        if 'pending_fees' in sanitized: sanitized['pending_fees'] = float(sanitized['pending_fees'])

        updated = self.repo.update(item_id, sanitized)
        self.audit_repo.log_action(actor_email, actor_role, 'UPDATE_INSTITUTION', 'INSTITUTION', f"Updated Institution {item_id}")
        return True, f"Institution updated successfully.", updated

    def set_status(self, item_id: str, status: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        existing = self.repo.find_by_id(item_id)
        if not existing:
            return False, "Institution record not found."
        self.repo.update(item_id, {'status': status})
        self.audit_repo.log_action(actor_email, actor_role, f'STATUS_{status}_INSTITUTION', 'INSTITUTION', f"Set Institution {item_id} status to {status}")
        return True, f"Institution status updated to {status}."

    def delete_institution(self, item_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        existing = self.repo.find_by_id(item_id)
        if not existing:
            return False, "Institution record not found."
        name = existing.get('name')
        self.repo.delete(item_id)
        self.audit_repo.log_action(actor_email, actor_role, 'DELETE_INSTITUTION', 'INSTITUTION', f"Permanently deleted Institution {name} ({item_id})")
        return True, f"Institution '{name}' permanently deleted."

    def get_summary_stats(self) -> Dict[str, Any]:
        records = self.repo.find_all()
        total_inst = len(records)
        active_cnt = sum(1 for r in records if r.get('status') == 'ACTIVE')
        pending_cnt = sum(1 for r in records if r.get('status') == 'PENDING')
        suspended_cnt = sum(1 for r in records if r.get('status') == 'SUSPENDED')

        total_students = sum(r.get('students_count', 0) for r in records)
        total_faculty = sum(r.get('faculty_count', 0) for r in records)
        total_fee_coll = sum(r.get('fee_collection', 0.0) for r in records)
        total_pending_fees = sum(r.get('pending_fees', 0.0) for r in records)

        att_rates = [r.get('attendance_rate', 95.0) for r in records]
        avg_att = round(sum(att_rates) / len(att_rates), 1) if att_rates else 95.0

        return {
            'total_institutions': total_inst,
            'active_institutions': active_cnt,
            'pending_institutions': pending_cnt,
            'suspended_institutions': suspended_cnt,
            'total_students': total_students,
            'total_faculty': total_faculty,
            'total_fee_collection': total_fee_coll,
            'total_pending_fees': total_pending_fees,
            'avg_attendance_rate': avg_att
        }

    def export_csv(self) -> str:
        records = self.repo.find_all()
        lines = ["ID,Code,Name,Type,City,State,Students,Faculty,Attendance%,FeeCollection,PendingFees,Status"]
        for r in records:
            lines.append(f"{r.get('id')},{r.get('code')},\"{r.get('name')}\",{r.get('type')},{r.get('city')},{r.get('state')},{r.get('students_count')},{r.get('faculty_count')},{r.get('attendance_rate')},{r.get('fee_collection')},{r.get('pending_fees')},{r.get('status')}")
        return "\n".join(lines)
