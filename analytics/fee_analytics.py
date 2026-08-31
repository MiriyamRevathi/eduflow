"""
EduFlow ERP Fee Analytics
Generates financial ledgers and collection summaries.
"""
from typing import Dict, Any, List
from repositories.fee_repository import FeeRepository
from repositories.payment_repository import PaymentRepository

class FeeAnalytics:
    def __init__(self):
        self.fee_repo = FeeRepository()
        self.payment_repo = PaymentRepository()

    def get_financial_summary(self) -> Dict[str, Any]:
        fees = self.fee_repo.find_all()
        payments = self.payment_repo.find_all()

        total_invoiced = sum(f.get('net_amount', 0) for f in fees)
        total_collected = sum(p.get('amount', 0) for p in payments)
        total_outstanding = total_invoiced - total_collected

        method_breakdown = {}
        for p in payments:
            m = p.get('payment_method', 'CARD')
            method_breakdown[m] = method_breakdown.get(m, 0.0) + float(p.get('amount', 0))

        return {
            'total_invoiced': total_invoiced,
            'total_collected': total_collected,
            'total_outstanding': total_outstanding,
            'method_breakdown': method_breakdown
        }
