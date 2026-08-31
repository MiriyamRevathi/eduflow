import json
from typing import List, Dict, Any

class JSONExporter:
    @staticmethod
    def export_to_json(data: List[Dict[str, Any]]) -> str:
        return json.dumps(data, indent=2, ensure_ascii=False)
