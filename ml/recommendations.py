from typing import List, Dict, Any

class RecommendationEngine:
    @staticmethod
    def generate_recommendations(features: Dict[str, float], risk_level: str) -> List[str]:
        recs = []

        if features['attendance_pct'] < 75.0:
            recs.append("⚠️ Attendance is below recommended institutional threshold (75%). Schedule counseling.")

        if features['marks_pct'] < 60.0:
            recs.append("📉 Examination performance has declined. Recommend remedial tutoring in core subjects.")

        if features['assignment_pct'] < 70.0:
            recs.append("📝 Assignment submission completion rate is low. Assign mentor follow-up.")

        if features['leave_count'] >= 3:
            recs.append("🩺 Frequent leave applications detected. Verify health/personal leave documentation.")

        if features['fee_pending_ratio'] > 0.3:
            recs.append("💳 Outstanding tuition fee balance detected. Send payment installment reminder.")

        if not recs:
            recs.append("✅ Student is maintaining excellent academic and attendance standards!")

        return recs
