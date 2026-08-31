from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.event_service import EventService
from security.rbac import login_required, admin_required
from security.session import SessionManager

events_bp = Blueprint('events', __name__, url_prefix='/events')
event_service = EventService()

@events_bp.route('/')
@login_required
def index():
    events = event_service.get_all_events()
    return render_template('events/index.html', events=events)

@events_bp.route('/new', methods=['POST'])
@login_required
@admin_required
def new_event():
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    data = {
        'title': request.form.get('title'),
        'category': request.form.get('category'),
        'target_audience': request.form.get('target_audience'),
        'event_date': request.form.get('event_date'),
        'location': request.form.get('location'),
        'description': request.form.get('description')
    }

    success, msg, created = event_service.create_event(data, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('events.index'))
