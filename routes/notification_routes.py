from flask import Blueprint, render_template, jsonify, request
from repositories.notification_repository import NotificationRepository
from security.rbac import login_required
from security.session import SessionManager

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')
notification_repo = NotificationRepository()

@notifications_bp.route('/')
@login_required
def index():
    user_id = SessionManager.get_current_user_id()
    notifications = notification_repo.find_by_user(user_id)
    return render_template('notifications/index.html', notifications=notifications)

@notifications_bp.route('/api/unread')
@login_required
def get_unread_api():
    user_id = SessionManager.get_current_user_id()
    all_notifs = notification_repo.find_by_user(user_id)
    unread = [n for n in all_notifs if not n.get('read', False)]
    return jsonify({
        'count': len(unread),
        'items': all_notifs[:5]
    })

@notifications_bp.route('/api/mark-all-read', methods=['POST'])
@login_required
def mark_all_read_api():
    user_id = SessionManager.get_current_user_id()
    count = notification_repo.mark_all_as_read(user_id)
    return jsonify({'success': True, 'count': count})
