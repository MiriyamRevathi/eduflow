import csv
import io
from typing import List, Dict, Any

class CSVExporter:
    @staticmethod
    def export_to_csv(data: List[Dict[str, Any]], fieldnames: List[str]) -> str:
        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()
        for row in data:
            writer.writerow(row)
        return output.getvalue()
