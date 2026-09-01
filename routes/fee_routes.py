from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.fee_service import FeeService
from repositories.student_repository import StudentRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

fees_bp = Blueprint('fees', __name__, url_prefix='/fees')
fee_service = FeeService()
student_repo = StudentRepository()

@fees_bp.route('/super-admin/fees')
@fees_bp.route('/')
@login_required
def index():
    selected_inst_id = session.get('selected_institution_id', 'ALL')
    fees = fee_service.get_all_fees()
    if selected_inst_id != 'ALL':
        fees = [f for f in fees if f.get('institution_id') == selected_inst_id]
    return render_template('fees/index.html', fees=fees)

@fees_bp.route('/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_fee():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'student_id': request.form.get('student_id'),
            'title': request.form.get('title'),
            'total_amount': request.form.get('total_amount'),
            'discount_amount': request.form.get('discount_amount', 0),
            'due_date': request.form.get('due_date')
        }

        success, msg, created = fee_service.create_fee_invoice(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('fees.index'))
        else:
            flash(msg, 'danger')

    students = student_repo.find_all()
    return render_template('fees/form.html', students=students)

@fees_bp.route('/<fee_id>/pay', methods=['GET', 'POST'])
@login_required
def pay_modal(fee_id):
    fee = fee_service.fee_repo.find_by_id(fee_id)
    if not fee:
        flash('Fee invoice not found.', 'danger')
        return redirect(url_for('fees.index'))

    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        amount = float(request.form.get('amount', 0))
        method = request.form.get('payment_method', 'CARD')
        ref = request.form.get('transaction_ref', '')

        success, msg, payment = fee_service.process_payment(fee_id, amount, method, ref, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('fees.view_receipt', payment_id=payment['id']))
        else:
            flash(msg, 'danger')

    student = student_repo.find_by_id(fee.get('student_id'))
    return render_template('fees/pay_modal.html', fee=fee, student=student)

@fees_bp.route('/receipt/<payment_id>')
@login_required
def view_receipt(payment_id):
    payment = fee_service.payment_repo.find_by_id(payment_id)
    if not payment:
        flash('Payment receipt not found.', 'danger')
        return redirect(url_for('fees.index'))

    fee = fee_service.fee_repo.find_by_id(payment.get('fee_id'))
    student = student_repo.find_by_id(payment.get('student_id'))
    return render_template('fees/receipt.html', payment=payment, fee=fee, student=student)
