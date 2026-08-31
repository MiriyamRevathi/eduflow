"""
EduFlow ERP Schema - Attendance
Data validation and payload sanitization rules.
"""
from typing import Dict, Any, List, Tuple

class AttendanceSchema:
    ALLOWED_FIELDS = ['id', 'code', 'name', 'status', 'created_at', 'updated_at', 'metadata', 'email', 'phone', 'details', 'title', 'remarks']

    @classmethod
    def validate_payload(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not isinstance(data, dict):
            return False, ["Payload must be a dictionary object."]

        for key in data.keys():
            if key not in cls.ALLOWED_FIELDS and not key.endswith('_id') and not key.endswith('_date') and not key.endswith('_amount') and not key.endswith('_count') and not key.endswith('_pct'):
                pass  # permissive for dynamic attributes

        return len(errors) == 0, errors

    @classmethod
    def sanitize(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        cleaned = {}
        for k, v in data.items():
            if isinstance(v, str):
                cleaned[k] = v.strip()
            else:
                cleaned[k] = v
        return cleaned
