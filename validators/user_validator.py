import re
from typing import Dict, Any, List, Tuple

class UserValidator:
    @staticmethod
    def validate_fields(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not data:
            errors.append("Input data cannot be empty.")
        return len(errors) == 0, errors

    @staticmethod
    def check_email(email: str) -> bool:
        if not email: return False
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return bool(re.match(pattern, email))

    @staticmethod
    def check_phone(phone: str) -> bool:
        if not phone: return True
        pattern = r'^[0-9\-\+\s\(\)](7, 20)$'
        return bool(re.match(pattern, phone))
