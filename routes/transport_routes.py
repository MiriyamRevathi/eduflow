from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.transport_service import TransportService
from repositories.student_repository import StudentRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

transport_bp = Blueprint('transport', __name__, url_prefix='/transport')
transport_service = TransportService()
student_repo = StudentRepository()

@transport_bp.route('/')
@login_required
def index():
    routes = transport_service.get_all_routes()
    students = student_repo.find_all()
    return render_template('transport/index.html', routes=routes, students=students)

@transport_bp.route('/routes/new', methods=['POST'])
@login_required
@admin_required
def new_route():
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    data = {
        'route_name': request.form.get('route_name'),
        'vehicle_number': request.form.get('vehicle_number'),
        'driver_name': request.form.get('driver_name'),
        'driver_phone': request.form.get('driver_phone'),
        'capacity': request.form.get('capacity'),
        'monthly_fee': request.form.get('monthly_fee'),
        'stops': request.form.get('stops')
    }

    success, msg, created = transport_service.create_route(data, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('transport.index'))

@transport_bp.route('/assign', methods=['POST'])
@login_required
@admin_required
def assign_student():
    route_id = request.form.get('route_id')
    student_id = request.form.get('student_id')
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = transport_service.assign_student(route_id, student_id, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('transport.index'))
