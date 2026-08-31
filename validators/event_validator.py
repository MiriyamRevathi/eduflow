"""
EduFlow ERP Validator — EventValidator
Data constraint checks and business rule enforcement for Event.
"""
import re
from typing import Dict, Any, List, Tuple

class EventValidator:
    @staticmethod
    def check_integrity(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        """Validate attribute constraints and data integrity for Event."""
        errors = []
        if not data:
            return False, ["Input record object cannot be null or empty."]

        if 'email' in data and data['email']:
            email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(email_pattern, str(data['email']).strip()):
                errors.append(f"Invalid email address format: {data['email']}")

        if 'phone' in data and data['phone']:
            phone_pattern = r'^[0-9\-\+\s\(\)\%]{7,20}$'
            if not re.match(phone_pattern, str(data['phone']).strip()):
                errors.append(f"Invalid phone number syntax: {data['phone']}")

        if 'amount' in data and data['amount'] is not None:
            try:
                val = float(data['amount'])
                if val < 0:
                    errors.append("Financial amount property cannot be negative.")
            except (ValueError, TypeError):
                errors.append("Financial amount must be a valid float/integer number.")

        if 'date' in data and data['date']:
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            if not re.match(date_pattern, str(data['date']).strip()):
                errors.append("Date format must strictly follow ISO YYYY-MM-DD.")

        return len(errors) == 0, errors

    @staticmethod
    def validate_id_format(entity_id: str) -> bool:
        """Validate primary key string format."""
        if not entity_id:
            return False
        return len(entity_id.strip()) >= 3

    @staticmethod
    def validate_status_transition(current_status: str, target_status: str) -> tuple[bool, str]:
        """Verify if status transition is allowed in domain state machine."""
        allowed_transitions = {
            'PENDING': ['APPROVED', 'REJECTED', 'UNDER_REVIEW', 'ARCHIVED'],
            'UNDER_REVIEW': ['APPROVED', 'REJECTED', 'WAITLISTED', 'ARCHIVED'],
            'APPROVED': ['ENROLLED', 'COMPLETED', 'ACTIVE', 'ARCHIVED'],
            'ACTIVE': ['INACTIVE', 'ARCHIVED', 'COMPLETED'],
            'INACTIVE': ['ACTIVE', 'ARCHIVED'],
            'ISSUED': ['RETURNED', 'OVERDUE', 'ARCHIVED'],
            'PAID': ['ARCHIVED'],
            'PARTIAL': ['PAID', 'ARCHIVED']
        }
        valid_targets = allowed_transitions.get(current_status, ['ACTIVE', 'INACTIVE', 'ARCHIVED'])
        if target_status in valid_targets:
            return True, f"Transition from {current_status} to {target_status} is valid."
        return False, f"Invalid status transition from {current_status} to {target_status}."
