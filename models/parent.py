from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
import datetime

@dataclass
class ParentModel:
    id: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    updated_at: str = field(default_factory=lambda: datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ParentModel':
        filtered = {k: v for k, v in data.items() if k in cls.__dataclass_fields__}
        return cls(**filtered)

    def validate(self) -> tuple[bool, str]:
        if not self.id:
            return False, "ID cannot be empty."
        return True, "Valid"
