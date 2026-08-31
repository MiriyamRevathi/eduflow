"""
EduFlow ERP Enterprise Domain Model — AdmissionModel
Applicant pipeline, application review, multi-stage status changes, and enrollment.
"""
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any, Tuple
import datetime
import uuid

@dataclass
class AdmissionModel:
    id: str
    code: Optional[str] = None
    name: Optional[str] = None
    status: str = 'ACTIVE'
    created_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    created_by: Optional[str] = 'system'
    updated_by: Optional[str] = 'system'
    notes: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    version: int = 1
    priority: int = 1
    department: Optional[str] = 'General'
    academic_year: Optional[str] = '2026'
    is_archived: bool = False
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert domain entity instance to a serializable dictionary format."""
        data = asdict(self)
        data['is_active'] = (self.status == 'ACTIVE')
        data['display_name'] = self.get_display_name()
        data['formatted_created_at'] = self.created_at
        data['formatted_updated_at'] = self.updated_at
        data['version_tag'] = f"v{self.version}.0"
        data['audit_count'] = len(self.audit_trail)
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AdmissionModel':
        """Construct domain entity from dictionary object safely."""
        if not data:
            raise ValueError("Admission input dictionary cannot be empty.")
        valid_keys = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        if 'id' not in valid_keys or not valid_keys['id']:
            valid_keys['id'] = str(uuid.uuid4())
        return cls(**valid_keys)

    def get_display_name(self) -> str:
        """Construct human-readable identifier for display in UI controls."""
        if self.name and self.code:
            return f"{self.name} ({self.code})"
        elif self.name:
            return self.name
        elif self.code:
            return self.code
        return f"Admission Record #{self.id}"

    def validate(self) -> tuple[bool, List[str]]:
        """Perform comprehensive data integrity checks on domain object."""
        errors = []
        if not self.id or len(str(self.id).strip()) == 0:
            errors.append("Admission Primary Key identifier (id) cannot be blank.")
        allowed_statuses = [
            'ACTIVE', 'INACTIVE', 'ARCHIVED', 'PENDING', 'APPROVED', 'REJECTED',
            'COMPLETED', 'SCHEDULED', 'ISSUED', 'RETURNED', 'APPLIED',
            'UNDER_REVIEW', 'WAITLISTED', 'ENROLLED', 'PAID', 'PARTIAL'
        ]
        if self.status not in allowed_statuses:
            errors.append(f"Invalid status specification: {self.status}. Must be one of {allowed_statuses}")
        if self.priority < 1 or self.priority > 10:
            errors.append(f"Priority value {self.priority} out of range (1-10).")
        return len(errors) == 0, errors

    def set_status(self, new_status: str, actor_id: str = 'system'):
        """Update domain entity status and touch modification timestamp."""
        old_status = self.status
        self.status = new_status
        self.updated_by = actor_id
        self.version += 1
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_mutation('STATUS_CHANGE', f"Changed status from {old_status} to {new_status}", actor_id)

    def add_tag(self, tag_name: str, actor_id: str = 'system'):
        """Append tag label if not already associated."""
        if tag_name and tag_name not in self.tags:
            self.tags.append(tag_name)
            self.version += 1
            self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_mutation('ADD_TAG', f"Added tag: {tag_name}", actor_id)

    def remove_tag(self, tag_name: str, actor_id: str = 'system'):
        """Detach tag label from domain entity."""
        if tag_name in self.tags:
            self.tags.remove(tag_name)
            self.version += 1
            self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.log_mutation('REMOVE_TAG', f"Removed tag: {tag_name}", actor_id)

    def set_attribute(self, key: str, value: Any, actor_id: str = 'system'):
        """Store dynamic key-value property inside metadata dictionary."""
        self.metadata[key] = value
        self.version += 1
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.log_mutation('UPDATE_METADATA', f"Set attribute {key}={value}", actor_id)

    def get_attribute(self, key: str, default_val: Any = None) -> Any:
        """Fetch dynamic key-value property from metadata dictionary."""
        return self.metadata.get(key, default_val)

    def is_active_status(self) -> bool:
        """Check if domain entity is active."""
        return self.status == 'ACTIVE' and not self.is_archived

    def archive_record(self, actor_id: str = 'system'):
        """Mark record as archived."""
        self.is_archived = True
        self.set_status('ARCHIVED', actor_id)

    def restore_record(self, actor_id: str = 'system'):
        """Restore record to active status."""
        self.is_archived = False
        self.set_status('ACTIVE', actor_id)

    def log_mutation(self, action: str, details: str, actor_id: str = 'system'):
        """Log state change event in audit trail list."""
        self.audit_trail.append({
            'action': action,
            'details': details,
            'actor': actor_id,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        })

    def clone(self) -> 'AdmissionModel':
        """Create a deep copy clone of the domain entity with a new UUID."""
        d = self.to_dict()
        d['id'] = str(uuid.uuid4())
        d['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        d['version'] = 1
        d['audit_trail'] = []
        return AdmissionModel.from_dict(d)

    def export_summary(self) -> str:
        """Export text representation summary of entity."""
        return f"Admission Entity ID: {self.id} | Name: {self.get_display_name()} | Status: {self.status} | Version: v{self.version}"

    def matches_search(self, query: str) -> bool:
        """Check if entity fields match search query string."""
        if not query:
            return True
        q = query.lower().strip()
        searchable = f"{self.id} {self.name or ''} {self.code or ''} {self.status} {' '.join(self.tags)} {self.department or ''}".lower()
        return q in searchable

    def __repr__(self) -> str:
        return f"<AdmissionModel id={self.id} name={self.name} status={self.status} v={self.version}>"
