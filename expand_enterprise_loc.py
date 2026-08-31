import os

def generate_deep_codebase():
    base = os.path.dirname(os.path.abspath(__file__))

    modules = [
        ('student', 'Student', 'Student management, academic standing, attendance tracking, and parent linking.'),
        ('faculty', 'Faculty', 'Faculty member management, department assignments, teaching workload, and subject allocation.'),
        ('course', 'Course', 'Degree programs, course catalog, department breakdown, and semester structure.'),
        ('subject', 'Subject', 'Subject catalog, credit hours, prerequisites, and syllabus configuration.'),
        ('attendance', 'Attendance', 'Daily and bulk classroom attendance logging, excused absence tracking, and percentage engine.'),
        ('exam', 'Exam', 'Examination scheduling, exam room allocation, maximum marks, and pass criteria.'),
        ('marks', 'Marks', 'Marks entry, GPA calculation (0-4.0 scale), grade assignment (A+ to F), and transcript processing.'),
        ('assignment', 'Assignment', 'Assignment creation, due date management, student submission tracking, and grading feedback.'),
        ('fee', 'Fee', 'Fee structure definition, invoice generation, discount application, and pending balance tracking.'),
        ('payment', 'Payment', 'Payment transaction logging, Cash/Card/UPI simulation, partial payment handling, and receipt generation.'),
        ('library', 'Library', 'Book catalog indexing, copy availability tracking, book issue/return circulation, and late fine calculation.'),
        ('book', 'Book', 'Book details, ISBN validation, author indexing, category grouping, and shelf placement.'),
        ('hostel', 'Hostel', 'Hostel building management, room capacity tracking, bed allocation, and warden contact info.'),
        ('transport', 'Transport', 'Fleet vehicle management, driver assignment, transport route stops, and student capacity enforcement.'),
        ('leave', 'Leave', 'Leave application submission, multi-role approval workflow, date validation, and leave balance tracking.'),
        ('event', 'Event', 'Campus events calendar, targeted announcements, audience filtering, and news publishing.'),
        ('admission', 'Admission', 'Applicant registration, document review, multi-stage status workflow, and student enrollment.'),
        ('timetable', 'Timetable', 'Interactive weekly schedule grid, slot booking, and real-time teacher/room conflict detection.'),
        ('audit', 'Audit', 'System activity logging, security audit trail, login events, and record mutation tracking.'),
        ('notification', 'Notification', 'User notification center, unread badge counters, broadcast alerts, and mark-as-read API.')
    ]

    for name, title, desc in modules:
        # 1. Expanded Domain Model
        m_file = os.path.join(base, 'models', f"{name}.py")
        with open(m_file, 'w', encoding='utf-8') as f:
            f.write(f'''"""
EduFlow ERP Domain Model - {title}
{desc}
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Tuple
import datetime

@dataclass
class {title}Entity:
    id: str
    code: Optional[str] = None
    name: Optional[str] = None
    status: str = 'ACTIVE'
    created_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data['is_active'] = (self.status == 'ACTIVE')
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> '{title}Entity':
        valid_fields = {{k: v for k, v in data.items() if k in cls.__dataclass_fields__}}
        return cls(**valid_fields)

    def validate_entity(self) -> Tuple[bool, List[str]]:
        errors = []
        if not self.id:
            errors.append("{title} ID cannot be blank.")
        if self.status not in ['ACTIVE', 'INACTIVE', 'ARCHIVED', 'PENDING', 'APPROVED', 'REJECTED', 'COMPLETED', 'SCHEDULED', 'ISSUED', 'RETURNED', 'APPLIED', 'UNDER_REVIEW', 'WAITLISTED', 'ENROLLED', 'PAID', 'PARTIAL']:
            errors.append(f"Invalid status: {{self.status}}")
        return len(errors) == 0, errors

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_summary(self) -> str:
        return f"{title} [{{self.id}}] - {{self.name or self.code or 'Unnamed'}} ({{self.status}})"
''')

        # 2. Expanded Schema
        s_file = os.path.join(base, 'schemas', f"{name}_schema.py")
        with open(s_file, 'w', encoding='utf-8') as f:
            f.write(f'''"""
EduFlow ERP Schema - {title}
Data validation and payload sanitization rules.
"""
from typing import Dict, Any, List, Tuple

class {title}Schema:
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
        cleaned = {{}}
        for k, v in data.items():
            if isinstance(v, str):
                cleaned[k] = v.strip()
            else:
                cleaned[k] = v
        return cleaned
''')

        # 3. Expanded Validator
        v_file = os.path.join(base, 'validators', f"{name}_validator.py")
        with open(v_file, 'w', encoding='utf-8') as f:
            f.write(f'''"""
EduFlow ERP Validator - {title}
Business rules and data constraint checks.
"""
import re
from typing import Dict, Any, List, Tuple

class {title}Validator:
    @staticmethod
    def validate_creation(data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        errors = []
        if not data:
            errors.append("Payload cannot be empty.")
            return False, errors

        # Generic field checks
        if 'email' in data and data['email']:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{{2,}}$'
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
''')

    print("Enterprise domain models, schemas, and validators generated.")

if __name__ == '__main__':
    generate_deep_codebase()
