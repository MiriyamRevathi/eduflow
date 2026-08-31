from typing import Dict, Any, Optional, List

class TeacherSchema:
    @staticmethod
    def validate_create_payload(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        errors = []
        if not isinstance(data, dict):
            return False, ["Payload must be a dictionary."]
        return len(errors) == 0, errors

    @staticmethod
    def sanitize(data: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {}
        for k, v in data.items():
            if isinstance(v, str):
                sanitized[k] = v.strip()
            else:
                sanitized[k] = v
        return sanitized
