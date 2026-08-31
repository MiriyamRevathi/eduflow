from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class BookRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.BOOKS_FILE, id_field='id')

    def find_by_isbn(self, isbn: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('isbn', isbn)

    def find_available(self) -> List[Dict[str, Any]]:
        records = self.find_all()
        return [r for r in records if int(r.get('available_copies', 0)) > 0]
