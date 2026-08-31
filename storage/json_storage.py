import json
import os
import threading
import tempfile
from typing import List, Dict, Any, Optional
from storage.base_storage import BaseStorage

class JSONStorage(BaseStorage):
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._lock = threading.RLock()
        self._ensure_file_exists()

    def _ensure_file_exists(self):
        dir_name = os.path.dirname(self.file_path)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        if not os.path.exists(self.file_path):
            with self._lock:
                with open(self.file_path, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=2)

    def read_all(self) -> List[Dict[str, Any]]:
        with self._lock:
            if not os.path.exists(self.file_path):
                return []
            try:
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error reading JSON from {self.file_path}: {e}")
                return []

    def write_all(self, data: List[Dict[str, Any]]) -> bool:
        with self._lock:
            try:
                dir_name = os.path.dirname(self.file_path) or '.'
                fd, temp_path = tempfile.mkstemp(dir=dir_name, suffix='.tmp')
                with os.fdopen(fd, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2, ensure_ascii=False)
                os.replace(temp_path, self.file_path)
                return True
            except Exception as e:
                print(f"Error atomic writing JSON to {self.file_path}: {e}")
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                return False

    def append_one(self, item: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            current_data = self.read_all()
            current_data.append(item)
            self.write_all(current_data)
            return item

    def update_one(self, item_id: str, updates: Dict[str, Any], id_field: str = 'id') -> Optional[Dict[str, Any]]:
        with self._lock:
            current_data = self.read_all()
            updated_item = None
            for idx, item in enumerate(current_data):
                if str(item.get(id_field)) == str(item_id):
                    item.update(updates)
                    updated_item = item
                    current_data[idx] = item
                    break
            if updated_item:
                self.write_all(current_data)
            return updated_item

    def delete_one(self, item_id: str, id_field: str = 'id') -> bool:
        with self._lock:
            current_data = self.read_all()
            filtered_data = [item for item in current_data if str(item.get(id_field)) != str(item_id)]
            if len(filtered_data) < len(current_data):
                self.write_all(filtered_data)
                return True
            return False
