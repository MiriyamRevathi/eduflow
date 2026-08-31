from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

class BaseStorage(ABC):
    @abstractmethod
    def read_all(self) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def write_all(self, data: List[Dict[str, Any]]) -> bool:
        pass

    @abstractmethod
    def append_one(self, item: Dict[str, Any]) -> Dict[str, Any]:
        pass

    @abstractmethod
    def update_one(self, item_id: str, updates: Dict[str, Any], id_field: str = 'id') -> Optional[Dict[str, Any]]:
        pass

    @abstractmethod
    def delete_one(self, item_id: str, id_field: str = 'id') -> bool:
        pass
