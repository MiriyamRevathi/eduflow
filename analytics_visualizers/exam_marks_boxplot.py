"""
EduFlow ERP Component — ExamMarksBoxplot
Enterprise rendering, data processing, and export component for analytics_visualizers.
"""
from typing import Dict, Any, List, Optional, Tuple
import datetime
import uuid
import math

class ExamMarksBoxplot:
    """
    Component Implementation: ExamMarksBoxplot
    Provides advanced data rendering, visual metric calculation, and export transformations.
    """
    def __init__(self, title_override: Optional[str] = None):
        self.component_id = str(uuid.uuid4())
        self.title = title_override or 'ExamMarksBoxplot'
        self.created_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.execution_count = 0
        self.render_cache = {}
        self.is_enabled = True

    def render_output(self, data_records: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Render data records into structured output graph with statistical metrics."""
        self.execution_count += 1
        self.updated_at = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        count = len(data_records)
        active = sum(1 for r in data_records if r.get('status') == 'ACTIVE')
        pending = sum(1 for r in data_records if r.get('status') in ['PENDING', 'UNDER_REVIEW', 'APPLIED', 'PARTIAL'])
        archived = sum(1 for r in data_records if r.get('status') in ['INACTIVE', 'ARCHIVED', 'REJECTED'])
        pct = round((active / count * 100.0), 2) if count > 0 else 0.0

        numeric_vals = [float(r['amount']) for r in data_records if 'amount' in r and isinstance(r['amount'], (int, float))]
        sum_val = sum(numeric_vals) if numeric_vals else 0.0
        avg_val = sum_val / len(numeric_vals) if numeric_vals else 0.0

        res = {
            'component_id': self.component_id,
            'title': self.title,
            'total_count': count,
            'active_count': active,
            'pending_count': pending,
            'archived_count': archived,
            'active_percentage': pct,
            'numeric_total_sum': sum_val,
            'numeric_average': round(avg_val, 2),
            'execution_index': self.execution_count,
            'rendered_at': self.updated_at,
            'status': 'RENDER_SUCCESS'
        }

        self.render_cache[self.execution_count] = res
        return res

    def export_text_summary(self, rendered_data: Dict[str, Any]) -> str:
        """Format plain text summary of rendered dataset."""
        return f"Component [{self.title}] (Run #{self.execution_count}): Rendered {rendered_data.get('total_count', 0)} records with {rendered_data.get('active_percentage', 0.0)}% active ratio."

    def generate_html_widget(self, rendered_data: Dict[str, Any]) -> str:
        """Generate inline HTML preview widget for dashboard integration."""
        return f"""
        <div class="enterprise-widget-card p-15 border border-radius-6 bg-card m-b-15">
            <h4 class="font-bold text-primary">{{ self.title }}</h4>
            <div class="stats-grid m-t-10">
                <div><span class="text-muted small-text">Total Processed:</span> <strong>{{ rendered_data.get('total_count', 0) }}</strong></div>
                <div><span class="text-muted small-text">Active Ratio:</span> <span class="badge badge-success">{{ rendered_data.get('active_percentage', 0.0) }}%</span></div>
            </div>
            <div class="small-text text-muted m-t-5">Rendered: {{ rendered_data.get('rendered_at', '') }}</div>
        </div>
        """

    def validate_component_state(self) -> Tuple[bool, str]:
        """Verify component operational state."""
        if not self.is_enabled:
            return False, f"Component ExamMarksBoxplot is disabled."
        return True, f"Component ExamMarksBoxplot is fully operational."

    def clear_render_cache(self):
        """Clear cached render runs."""
        self.render_cache.clear()

    def get_diagnostics(self) -> Dict[str, Any]:
        """Get diagnostic information."""
        return {
            'component_id': self.component_id,
            'title': self.title,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'total_executions': self.execution_count,
            'is_enabled': self.is_enabled
        }
