from typing import Optional, Dict, Any, List
import datetime
from config import Config
from repositories.base_repository import BaseRepository

class AuditRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.AUDIT_LOGS_FILE, id_field='id')

    def log_action(self, user_email: str, user_role: str, action: str, entity: str, details: str = ''):
        import uuid
        log_entry = {
            'id': str(uuid.uuid4()),
            'user': user_email,
            'role': user_role,
            'action': action,
            'entity': entity,
            'details': details,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.create(log_entry)

    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        logs = self.find_all()
        return sorted(logs, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]
