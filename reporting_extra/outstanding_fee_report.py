"""
EduFlow ERP Reporting Component — OutstandingFeeReport
Enterprise report generator implementation for outstanding_fee_report.py.
"""
from typing import Dict, Any, List, Optional, Tuple
import datetime
import uuid

class OutstandingFeeReport:
    """
    Reporting Engine Implementation: OutstandingFeeReport
    Provides structured data aggregation, report formatting, CSV export, and PDF printable layout rendering.
    """
    def __init__(self, report_title: Optional[str] = None):
        self.report_id = str(uuid.uuid4())
        self.report_title = report_title or 'OutstandingFeeReport'
        self.generated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.generation_count = 0
        self.history = []

    def generate_report(self, records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate structured report payload from record collection."""
        self.generation_count += 1
        total = len(records)
        active = sum(1 for r in records if r.get('status') == 'ACTIVE')
        pending = sum(1 for r in records if r.get('status') in ['PENDING', 'UNDER_REVIEW', 'APPLIED', 'PARTIAL'])
        archived = sum(1 for r in records if r.get('status') in ['INACTIVE', 'ARCHIVED', 'REJECTED'])
        ratio = round((active / total * 100.0), 2) if total > 0 else 0.0

        payload = {
            'report_id': self.report_id,
            'report_title': self.report_title,
            'generation_index': self.generation_count,
            'generated_at': self.generated_at,
            'total_records': total,
            'active_records': active,
            'pending_records': pending,
            'archived_records': archived,
            'active_ratio_pct': ratio,
            'records': records,
            'status': 'SUCCESS'
        }
        self.history.append(payload)
        return payload

    def export_as_csv(self, report_payload: Dict[str, Any]) -> str:
        """Export report payload as CSV formatted string."""
        lines = [f"# Report Title: {self.report_title}", "# Generated At: {self.generated_at}", "ID,Name,Code,Status,Created"]
        for r in report_payload.get('records', []):
            lines.append(f"{r.get('id', '')},{r.get('name') or r.get('title') or ''},{r.get('code', '')},{r.get('status', '')},{r.get('created_at', '')}")
        return "
".join(lines)

    def export_as_json(self, report_payload: Dict[str, Any]) -> Dict[str, Any]:
        """Export report payload in JSON API structure."""
        return {
            'meta': {
                'report_id': self.report_id,
                'title': self.report_title,
                'generated_at': self.generated_at
            },
            'summary': {
                'total': report_payload.get('total_records', 0),
                'active': report_payload.get('active_records', 0),
                'active_ratio_pct': report_payload.get('active_ratio_pct', 0.0)
            },
            'data': report_payload.get('records', [])
        }

    def render_printable_html(self, report_payload: Dict[str, Any]) -> str:
        """Render printable HTML document markup."""
        return f"""
        <div class="printable-report-wrapper p-20 bg-card border border-radius-8">
            <h2 class="text-primary font-bold">{{ self.report_title }}</h2>
            <div class="small-text text-muted m-b-15">Generated At: {{ self.generated_at }} | Report ID: {{ self.report_id }}</div>
            <div class="stats-grid m-b-20">
                <div>Total Records: <strong>{{ report_payload.get('total_records', 0) }}</strong></div>
                <div>Active Ratio: <span class="badge badge-success">{{ report_payload.get('active_ratio_pct', 0.0) }}%</span></div>
            </div>
        </div>
        """

    def get_history(self) -> List[Dict[str, Any]]:
        """Retrieve history of report generations."""
        return self.history
