"""
EduFlow ERP Schema — StudentSchema
Payload validation, sanitization, and data transformation rules for Student.
"""
from typing import Dict, Any, List, Tuple, Optional

class StudentSchema:
    REQUIRED_FIELDS = ['id']
    OPTIONAL_FIELDS = ['code', 'name', 'status', 'tags', 'metadata', 'created_at', 'updated_at', 'created_by', 'updated_by', 'notes', 'version']

    @classmethod
    def validate_create_payload(cls, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate input payload prior to entity creation in JSON storage."""
        errors = []
        if not isinstance(data, dict):
            return False, ["Payload must be a dictionary object."]

        for field_name in cls.REQUIRED_FIELDS:
            if field_name not in data or data[field_name] is None or str(data[field_name]).strip() == '':
                errors.append(f"Required field '{field_name}' is missing or blank for Student.")

        if 'email' in data and data['email']:
            if '@' not in str(data['email']):
                errors.append("Email property must be a valid email address.")

        return len(errors) == 0, errors

    @classmethod
    def validate_update_payload(cls, data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate update dictionary prior to record mutation."""
        errors = []
        if not isinstance(data, dict):
            return False, ["Update payload must be a dictionary object."]
        if len(data) == 0:
            errors.append("Update payload cannot be empty.")
        return len(errors) == 0, errors

    @classmethod
    def sanitize_payload(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """Recursively trim whitespace and sanitize input attributes."""
        cleaned = {}
        for k, v in data.items():
            if isinstance(v, str):
                cleaned[k] = v.strip()
            elif isinstance(v, list):
                cleaned[k] = [item.strip() if isinstance(item, str) else item for item in v]
            elif isinstance(v, dict):
                cleaned[k] = cls.sanitize_payload(v)
            else:
                cleaned[k] = v
        return cleaned

    @classmethod
    def format_for_display(cls, record_dict: Dict[str, Any]) -> Dict[str, Any]:
        """Decorate dictionary with Jinja2 UI CSS badge classes and formatted values."""
        formatted = dict(record_dict)
        if 'status' in formatted:
            formatted['status_badge_class'] = cls.get_status_badge_class(formatted['status'])
        formatted['display_title'] = formatted.get('name') or formatted.get('code') or formatted.get('id')
        formatted['is_archived'] = (formatted.get('status') == 'ARCHIVED')
        return formatted

    @staticmethod
    def get_status_badge_class(status_str: str) -> str:
        """Map status token string to enterprise CSS theme badge class."""
        mapping = {
            'ACTIVE': 'badge-success',
            'APPROVED': 'badge-success',
            'COMPLETED': 'badge-success',
            'ENROLLED': 'badge-primary',
            'PAID': 'badge-success',
            'PARTIAL': 'badge-warning',
            'PENDING': 'badge-warning',
            'UNDER_REVIEW': 'badge-warning',
            'WAITLISTED': 'badge-secondary',
            'INACTIVE': 'badge-secondary',
            'ARCHIVED': 'badge-secondary',
            'REJECTED': 'badge-danger',
            'FAILED': 'badge-danger'
        }
        return mapping.get(status_str, 'badge-light')

    @classmethod
    def generate_json_schema(cls) -> Dict[str, Any]:
        """Generate JSON Schema definition object for API endpoints."""
        return {
            '$schema': 'http://json-schema.org/draft-07/schema#',
            'title': 'StudentSchema',
            'type': 'object',
            'properties': {
                'id': {'type': 'string', 'description': 'Primary Key UUID/Identifier'},
                'code': {'type': ['string', 'null'], 'description': 'Unique Entity Code'},
                'name': {'type': ['string', 'null'], 'description': 'Full Display Name'},
                'status': {'type': 'string', 'enum': ['ACTIVE', 'INACTIVE', 'ARCHIVED', 'PENDING', 'APPROVED', 'REJECTED']},
                'created_at': {'type': 'string', 'format': 'date-time'},
                'updated_at': {'type': 'string', 'format': 'date-time'}
            },
            'required': cls.REQUIRED_FIELDS
        }
