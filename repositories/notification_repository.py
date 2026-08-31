from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class NotificationRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.NOTIFICATIONS_FILE, id_field='id')

    def find_by_user(self, user_id: str) -> List[Dict[str, Any]]:
        records = self.find_all()
        return [r for r in records if r.get('recipient_id') == user_id or r.get('recipient_role') == 'ALL']

    def mark_as_read(self, notification_id: str) -> Optional[Dict[str, Any]]:
        return self.update(notification_id, {'read': True})

    def mark_all_as_read(self, user_id: str) -> int:
        records = self.find_by_user(user_id)
        count = 0
        for r in records:
            if not r.get('read', False):
                self.update(r['id'], {'read': True})
                count += 1
        return count
