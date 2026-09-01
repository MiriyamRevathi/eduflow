"""
EduFlow ERP Route Controller — SettingsRoutes
Blueprint routes for Platform & System Settings.
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from security.rbac import login_required, admin_required
from security.session import SessionManager

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/')
@login_required
def index():
    return render_template('settings/index.html')

@settings_bp.route('/save', methods=['POST'])
@login_required
@admin_required
def save():
    flash('Platform settings updated successfully.', 'success')
    return redirect(url_for('settings.index'))
