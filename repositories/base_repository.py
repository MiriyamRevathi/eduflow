import math
from typing import List, Dict, Any, Optional, Callable
from storage.json_storage import JSONStorage

class BaseRepository:
    def __init__(self, file_path: str, id_field: str = 'id'):
        self.storage = JSONStorage(file_path)
        self.id_field = id_field

    def find_all(self) -> List[Dict[str, Any]]:
        return self.storage.read_all()

    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        records = self.find_all()
        for item in records:
            if str(item.get(self.id_field)) == str(item_id):
                return item
        return None

    def find_by_field(self, field_name: str, value: Any) -> List[Dict[str, Any]]:
        records = self.find_all()
        return [item for item in records if item.get(field_name) == value]

    def find_one_by_field(self, field_name: str, value: Any) -> Optional[Dict[str, Any]]:
        records = self.find_all()
        for item in records:
            if item.get(field_name) == value:
                return item
        return None

    def find_where(self, criteria: Dict[str, Any]) -> List[Dict[str, Any]]:
        records = self.find_all()
        result = []
        for item in records:
            match = True
            for key, val in criteria.items():
                if item.get(key) != val:
                    match = False
                    break
            if match:
                result.append(item)
        return result

    def create(self, item: Dict[str, Any]) -> Dict[str, Any]:
        return self.storage.append_one(item)

    def update(self, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        return self.storage.update_one(item_id, updates, id_field=self.id_field)

    def delete(self, item_id: str) -> bool:
        return self.storage.delete_one(item_id, id_field=self.id_field)

    def count(self, criteria: Optional[Dict[str, Any]] = None) -> int:
        if not criteria:
            return len(self.find_all())
        return len(self.find_where(criteria))

    def search(self, query: str, search_fields: List[str]) -> List[Dict[str, Any]]:
        if not query:
            return self.find_all()
        query_lower = str(query).strip().lower()
        records = self.find_all()
        results = []
        for item in records:
            matched = False
            for field in search_fields:
                val = item.get(field)
                if val is not None and query_lower in str(val).lower():
                    matched = True
                    break
            if matched:
                results.append(item)
        return results

    def paginate(
        self,
        page: int = 1,
        per_page: int = 10,
        criteria: Optional[Dict[str, Any]] = None,
        search_query: Optional[str] = None,
        search_fields: Optional[List[str]] = None,
        sort_by: Optional[str] = None,
        order: str = 'asc'
    ) -> Dict[str, Any]:
        records = self.find_all()

        if criteria:
            filtered = []
            for item in records:
                match = True
                for k, v in criteria.items():
                    if v is not None and item.get(k) != v:
                        match = False
                        break
                if match:
                    filtered.append(item)
            records = filtered

        if search_query and search_fields:
            sq_lower = search_query.strip().lower()
            searched = []
            for item in records:
                matched = False
                for field in search_fields:
                    val = item.get(field)
                    if val is not None and sq_lower in str(val).lower():
                        matched = True
                        break
                if matched:
                    searched.append(item)
            records = searched

        if sort_by:
            reverse = (order.lower() == 'desc')
            records = sorted(
                records,
                key=lambda x: (x.get(sort_by) is None, x.get(sort_by)),
                reverse=reverse
            )

        total_items = len(records)
        total_pages = max(1, math.ceil(total_items / per_page))
        page = max(1, min(page, total_pages))
        
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        items_page = records[start_idx:end_idx]

        return {
            'items': items_page,
            'total': total_items,
            'page': page,
            'per_page': per_page,
            'total_pages': total_pages,
            'has_prev': page > 1,
            'has_next': page < total_pages
        }
