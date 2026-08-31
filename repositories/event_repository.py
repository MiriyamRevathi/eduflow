from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class EventRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.EVENTS_FILE, id_field='id')

    def find_upcoming(self) -> List[Dict[str, Any]]:
        records = self.find_all()
        return sorted(records, key=lambda x: x.get('event_date', ''), reverse=False)
