"""
EduFlow ERP Validator — InstitutionValidator
"""
from typing import Dict, Any, Tuple, List

class InstitutionValidator:
    def check_integrity(self, payload: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not payload.get('name'):
            errors.append("Institution Name is required.")
        if not payload.get('type'):
            errors.append("Institution Type is required.")
        if not payload.get('email'):
            errors.append("Contact Email is required.")
        return len(errors) == 0, errors
