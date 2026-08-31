from typing import Optional, Dict, Any, List, Tuple
from repositories.event_repository import EventRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils
import uuid

class EventService:
    def __init__(self):
        self.event_repo = EventRepository()
        self.audit_repo = AuditRepository()

    def get_all_events((self)) -> List[Dict[str, Any]]:
        return self.event_repo.find_upcoming()

    def create_event(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()

        if not title:
            return False, "Title is required.", None

        event_data = {
            'id': str(uuid.uuid4()),
            'title': title,
            'category': data.get('category', 'EVENT'),
            'target_audience': data.get('target_audience', 'EVERYONE'),
            'event_date': data.get('event_date', DateTimeUtils.current_date_str()),
            'location': data.get('location', 'Main Campus'),
            'description': description,
            'created_by': actor_email
        }

        created = self.event_repo.create(event_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_EVENT', 'EVENTS', f"Published event '{title}' for {event_data['target_audience']}")
        return True, f"Event '{title}' created successfully.", created
