from typing import Optional, Dict, Any, List, Tuple
from repositories.fee_repository import FeeRepository
from repositories.payment_repository import PaymentRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.id_generator import IDGenerator
from utils.datetime_utils import DateTimeUtils
import uuid

class FeeService:
    def __init__(self):
        self.fee_repo = FeeRepository()
        self.payment_repo = PaymentRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_all_fees(self) -> List[Dict[str, Any]]:
        fees = self.fee_repo.find_all()
        for f in fees:
            student = self.student_repo.find_by_id(f.get('student_id'))
            f['student_name'] = student.get('full_name') if student else 'N/A'
            f['student_code'] = student.get('student_id') if student else 'N/A'
        return fees

    def create_fee_invoice(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        student_id = data.get('student_id')
        title = data.get('title', '').strip()
        total_amount = float(data.get('total_amount', 0))
        discount_amount = float(data.get('discount_amount', 0))

        if not student_id or not title or total_amount <= 0:
            return False, "Student, Invoice Title, and valid Amount are required.", None

        net_amount = max(0.0, total_amount - discount_amount)
        fee_count = self.fee_repo.count() + 1
        fee_code = IDGenerator.generate_fee_id(fee_count)

        fee_record = {
            'id': f"fee-{fee_count:04d}",
            'fee_code': fee_code,
            'student_id': student_id,
            'title': title,
            'total_amount': total_amount,
            'discount_amount': discount_amount,
            'net_amount': net_amount,
            'paid_amount': 0.0,
            'pending_amount': net_amount,
            'due_date': data.get('due_date', DateTimeUtils.current_date_str()),
            'status': 'PENDING'
        }

        created = self.fee_repo.create(fee_record)
        self.audit_repo.log_action(actor_email, actor_role, 'CREATE_FEE_INVOICE', 'FEES', f"Created fee invoice {fee_code} for ${net_amount}")
        return True, f"Fee invoice {fee_code} created successfully.", created

    def process_payment(self, fee_id: str, amount: float, method: str, ref: str, actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        fee = self.fee_repo.find_by_id(fee_id)
        if not fee:
            return False, "Fee record not found.", None

        if amount <= 0:
            return False, "Payment amount must be greater than zero.", None

        pending = float(fee.get('pending_amount', 0))
        if amount > pending:
            return False, f"Payment amount exceeds outstanding balance of ${pending:.2f}.", None

        new_paid = float(fee.get('paid_amount', 0)) + amount
        new_pending = pending - amount
        new_status = 'PAID' if new_pending <= 0.01 else 'PARTIAL'

        # Update fee record
        self.fee_repo.update(fee_id, {
            'paid_amount': round(new_paid, 2),
            'pending_amount': round(new_pending, 2),
            'status': new_status
        })

        # Create payment receipt
        pay_count = self.payment_repo.count() + 1
        pay_code = IDGenerator.generate_payment_id(pay_count)

        payment_record = {
            'id': f"pay-{pay_count:05d}",
            'payment_code': pay_code,
            'fee_id': fee_id,
            'student_id': fee.get('student_id'),
            'amount': amount,
            'payment_method': method,
            'transaction_ref': ref or 'SIMULATED-TXN',
            'payment_date': DateTimeUtils.current_datetime_str(),
            'receipt_no': f"RCP-2026-{pay_count:03d}",
            'remarks': f"Simulated {method} payment of ${amount:.2f}"
        }

        created_pay = self.payment_repo.create(payment_record)
        self.audit_repo.log_action(actor_email, actor_role, 'FEE_PAYMENT', 'FEES', f"Processed ${amount:.2f} payment for fee {fee.get('fee_code')} via {method}")
        return True, f"Payment of ${amount:.2f} processed successfully. Receipt {created_pay['receipt_no']} issued.", created_pay
