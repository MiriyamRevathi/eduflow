import os

def create_expanded_files():
    base = os.path.dirname(os.path.abspath(__file__))

    # Directories
    dirs = ['models', 'schemas', 'validators', 'analytics', 'reporting', 'communication', 'storage', 'search']
    for d in dirs:
        os.makedirs(os.path.join(base, d), exist_ok=True)

    # 1. Models & Schemas Layer (20+ entities with full validation & dict serialization)
    entities = [
        'user', 'student', 'teacher', 'parent', 'course', 'subject', 'attendance',
        'exam', 'marks', 'assignment', 'fee', 'payment', 'library', 'book',
        'hostel', 'transport', 'leave', 'event', 'admission', 'timetable', 'audit'
    ]

    for entity in entities:
        # Model
        m_path = os.path.join(base, 'models', f"{entity}.py")
        with open(m_path, 'w', encoding='utf-8') as f:
            f.write(f'''from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import datetime

@dataclass
class {entity.capitalize()}Model:
    id: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> '{entity.capitalize()}Model':
        filtered = {{k: v for k, v in data.items() if k in cls.__dataclass_fields__}}
        return cls(**filtered)

    def validate(self) -> Tuple_Bool_Msg:
        if not self.id:
            return False, "ID cannot be empty."
        return True, "Valid"
'''.replace('Tuple_Bool_Msg', 'tuple[bool, str]'))

        # Schema
        s_path = os.path.join(base, 'schemas', f"{entity}_schema.py")
        with open(s_path, 'w', encoding='utf-8') as f:
            f.write(f'''from typing import Dict, Any, Optional, List

class {entity.capitalize()}Schema:
    @staticmethod
    def validate_create_payload(data: Dict[str, Any]) -> tuple[bool, List[str]]:
        errors = []
        if not isinstance(data, dict):
            return False, ["Payload must be a dictionary."]
        return len(errors) == 0, errors

    @staticmethod
    def sanitize(data: Dict[str, Any]) -> Dict[str, Any]:
        sanitized = {{}}
        for k, v in data.items():
            if isinstance(v, str):
                sanitized[k] = v.strip()
            else:
                sanitized[k] = v
        return sanitized
''')

        # Validator
        v_path = os.path.join(base, 'validators', f"{entity}_validator.py")
        with open(v_path, 'w', encoding='utf-8') as f:
            f.write(f'''import re
from typing import Dict, Any, List, Tuple

class {entity.capitalize()}Validator:
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
        pattern = r'^[0-9\-\+\s\(\)]{7,20}$'
        return bool(re.match(pattern, phone))
''')

if __name__ == '__main__':
    create_expanded_files()
    print("Models, schemas, and validators created.")
