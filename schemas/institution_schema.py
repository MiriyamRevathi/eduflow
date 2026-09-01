"""
EduFlow ERP Schema — InstitutionSchema
"""
from typing import Dict, Any

class InstitutionSchema:
    def sanitize_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for k, v in payload.items():
            if isinstance(v, str):
                sanitized[k] = v.strip()
            else:
                sanitized[k] = v
        return sanitized
