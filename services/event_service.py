"""
EduFlow ERP Service — EventService
Campus events, announcements, and activity calendar.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.event_repository import EventRepository
from repositories.audit_repository import AuditRepository

class EventService:
    def __init__(self):
        self.event_repo = EventRepository()
        self.repo = self.event_repo
        self.audit_repo = AuditRepository()

    def get_all_events(self) -> List[Dict[str, Any]]:
        return self.event_repo.find_all()

    def create_event(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        title = data.get('title', '').strip()
        event_date = data.get('event_date', '').strip()
        if not title or not event_date:
            return False, "Title and Event Date are required.", None

        count = self.event_repo.count() + 1
        event_data = {
            'id': f"evt-{count:03d}",
            'title': title,
            'event_date': event_date,
            'time': data.get('time', '10:00 AM'),
            'venue': data.get('venue', 'Main Auditorium'),
            'target_audience': data.get('target_audience', 'ALL'),
            'description': data.get('description', ''),
            'organizer': data.get('organizer', 'Student Affairs'),
            'status': 'ACTIVE'
        }
        created = self.event_repo.create(event_data)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_EVENT', 'EVENT', f"Created campus event {title}")
        return True, "Event created successfully.", created
