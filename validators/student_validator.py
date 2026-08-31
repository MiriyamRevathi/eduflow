"""
EduFlow ERP Validator - Student
Business rules and data constraint checks.
"""
import re
from typing import Dict, Any, List, Tuple

class StudentValidator:
    @staticmethod
    def validate_creation(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not data:
            errors.append("Payload cannot be empty.")
            return False, errors

        # Generic field checks
        if 'email' in data and data['email']:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, str(data['email']).strip()):
                errors.append("Invalid email address format.")

        if 'amount' in data and data['amount'] is not None:
            try:
                val = float(data['amount'])
                if val < 0:
                    errors.append("Amount cannot be negative.")
            except ValueError:
                errors.append("Amount must be a numeric value.")

        return len(errors) == 0, errors

    @staticmethod
    def validate_update(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not data:
            errors.append("Update payload cannot be empty.")
        return len(errors) == 0, errors
