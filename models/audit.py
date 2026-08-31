"""
EduFlow ERP Domain Model - Audit
System activity logging, security audit trail, login events, and record mutation tracking.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Tuple
import datetime

@dataclass
class AuditEntity:
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
    def from_dict(cls, data: Dict[str, Any]) -> 'AuditEntity':
        valid_fields = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**valid_fields)

    def validate_entity(self) -> Tuple[bool, List[str]]:
        errors = []
        if not self.id:
            errors.append("Audit ID cannot be blank.")
        if self.status not in ['ACTIVE', 'INACTIVE', 'ARCHIVED', 'PENDING', 'APPROVED', 'REJECTED', 'COMPLETED', 'SCHEDULED', 'ISSUED', 'RETURNED', 'APPLIED', 'UNDER_REVIEW', 'WAITLISTED', 'ENROLLED', 'PAID', 'PARTIAL']:
            errors.append(f"Invalid status: {self.status}")
        return len(errors) == 0, errors

    def update_timestamp(self):
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def get_summary(self) -> str:
        return f"Audit [{self.id}] - {self.name or self.code or 'Unnamed'} ({self.status})"
