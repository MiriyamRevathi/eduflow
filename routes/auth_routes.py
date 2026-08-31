from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.auth_service import AuthService
from security.session import SessionManager
from security.rbac import login_required
from repositories.user_repository import UserRepository

auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()
user_repo = UserRepository()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if SessionManager.is_authenticated():
        return redirect(url_for('dashboard.index'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        success, message, user = auth_service.authenticate(email, password)

        if success:
            flash(message, 'success')
            next_url = request.args.get('next')
            return redirect(next_url or url_for('dashboard.index'))
        else:
            flash(message, 'danger')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    auth_service.logout()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

@auth_bp.route('/profile')
@login_required
def profile():
    user_id = SessionManager.get_current_user_id()
    user = user_repo.find_by_id(user_id)
    return render_template('auth/profile.html', user=user)

@auth_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        user_id = SessionManager.get_current_user_id()
        old_pwd = request.form.get('old_password', '')
        new_pwd = request.form.get('new_password', '')
        confirm_pwd = request.form.get('confirm_password', '')

        if new_pwd != confirm_pwd:
            flash('New passwords do not match.', 'danger')
            return render_template('auth/change_password.html')

        success, msg = auth_service.change_password(user_id, old_pwd, new_pwd)
        if success:
            flash(msg, 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash(msg, 'danger')

    return render_template('auth/change_password.html')

@auth_bp.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        user = user_repo.find_by_email(email)
        if user:
            flash(f'Password reset link has been dispatched to {email}. (Local Simulation)', 'info')
        else:
            flash('If an account exists for that email, a password reset link has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/forgot_password.html')
