from functools import wraps
from flask import redirect, url_for, flash, render_template, request
from security.session import SessionManager
from config import Config

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not SessionManager.is_authenticated():
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def roles_required(*allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not SessionManager.is_authenticated():
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            user_role = SessionManager.get_current_role()
            if user_role not in allowed_roles and Config.ROLE_SUPER_ADMIN not in allowed_roles:
                if user_role != Config.ROLE_SUPER_ADMIN:
                    return render_template('errors/403.html'), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def admin_required(f):
    return roles_required(*Config.ADMIN_ROLES)(f)
