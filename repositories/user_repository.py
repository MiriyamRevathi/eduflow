from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class UserRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.USERS_FILE, id_field='id')

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            return None
        return self.find_one_by_field('email', email.strip().lower())

    def find_by_role(self, role: str) -> List[Dict[str, Any]]:
        return self.find_by_field('role', role)

    def find_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('username', username)
