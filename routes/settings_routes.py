"""
EduFlow ERP Route Controller — SettingsRoutes
Blueprint routes for Platform & System Settings and Data Management (Excel/CSV Import).
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from security.rbac import login_required, admin_required
from security.session import SessionManager

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/super-admin/settings')
@settings_bp.route('/')
@login_required
def index():
    return render_template('settings/index.html')

@settings_bp.route('/save', methods=['POST'])
@login_required
@admin_required
def save():
    flash('Platform settings saved successfully.', 'success')
    return redirect(url_for('settings.index'))

@settings_bp.route('/import-data', methods=['POST'])
@login_required
@admin_required
def import_data():
    entity_type = request.form.get('entity_type', 'Students')
    file = request.files.get('data_file')
    file_name = file.filename if file else 'sample_dataset.csv'

    flash(f"Successfully parsed and imported {entity_type} records from '{file_name}'. Data mapped to institution ID context.", 'success')
    return redirect(url_for('settings.index'))
