import os
from flask import Flask, render_template, request, session, redirect, url_for
from config import Config
from utils.data_seeder import seed_database
from repositories.institution_repository import InstitutionRepository

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database seeded on startup
    if not os.path.exists(Config.USERS_FILE):
        seed_database()

    inst_repo = InstitutionRepository()

    # Context Processor & Middleware for Global Institution Selector
    @app.before_request
    def handle_institution_context():
        inst_id = request.args.get('inst_id')
        if inst_id:
            session['selected_institution_id'] = inst_id
        elif 'selected_institution_id' not in session:
            session['selected_institution_id'] = 'ALL'

    @app.context_processor
    def inject_institution_context():
        institutions = inst_repo.find_all()
        selected_id = session.get('selected_institution_id', 'ALL')
        selected_name = "All Institutions"
        if selected_id != 'ALL':
            found = inst_repo.find_by_id(selected_id)
            if found:
                selected_name = found.get('name')

        return {
            'all_institutions': institutions,
            'selected_institution_id': selected_id,
            'selected_institution_name': selected_name
        }

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
    from routes.institution_routes import institutions_bp
    from routes.user_routes import users_bp
    from routes.student_routes import students_bp
    from routes.faculty_routes import faculty_bp
    from routes.academic_routes import academics_bp
    from routes.admission_routes import admissions_bp
    from routes.attendance_routes import attendance_bp
    from routes.timetable_routes import timetable_bp
    from routes.exam_routes import exams_bp
    from routes.fee_routes import fees_bp
    from routes.library_routes import library_bp
    from routes.hostel_routes import hostel_bp
    from routes.transport_routes import transport_bp
    from routes.leave_routes import leave_bp
    from routes.event_routes import events_bp
    from routes.analytics_routes import analytics_bp, reporting_bp
    from routes.reports_routes import reports_bp
    from routes.search_routes import search_bp
    from routes.audit_routes import audit_bp
    from routes.notification_routes import notifications_bp
    from routes.portal_routes import portal_bp
    from routes.settings_routes import settings_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(institutions_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(faculty_bp)
    app.register_blueprint(academics_bp)
    app.register_blueprint(admissions_bp)
    app.register_blueprint(attendance_bp)
    app.register_blueprint(timetable_bp)
    app.register_blueprint(exams_bp)
    app.register_blueprint(fees_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(hostel_bp)
    app.register_blueprint(transport_bp)
    app.register_blueprint(leave_bp)
    app.register_blueprint(events_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(reporting_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(portal_bp)
    app.register_blueprint(settings_bp)

    # Super Admin URL Route Aliases
    @app.route('/super-admin/dashboard')
    def sa_dashboard(): return redirect(url_for('dashboard.index'))
    @app.route('/super-admin/institutions')
    @app.route('/super-admin/institutions/')
    def sa_institutions(): return redirect(url_for('institutions.index'))
    @app.route('/super-admin/users')
    @app.route('/super-admin/users/')
    def sa_users(): return redirect(url_for('users.index'))
    @app.route('/super-admin/students')
    @app.route('/super-admin/students/')
    def sa_students(): return redirect(url_for('students.index'))
    @app.route('/super-admin/faculty')
    @app.route('/super-admin/faculty/')
    def sa_faculty(): return redirect(url_for('faculty.index'))
    @app.route('/super-admin/programs')
    @app.route('/super-admin/programs/')
    def sa_programs(): return redirect(url_for('academics.index'))
    @app.route('/super-admin/attendance')
    @app.route('/super-admin/attendance/')
    def sa_attendance(): return redirect(url_for('attendance.index'))
    @app.route('/super-admin/fees')
    @app.route('/super-admin/fees/')
    def sa_fees(): return redirect(url_for('fees.index'))
    @app.route('/super-admin/reports')
    @app.route('/super-admin/reports/')
    def sa_reports(): return redirect(url_for('reports.index'))
    @app.route('/super-admin/audit-logs')
    @app.route('/super-admin/audit-logs/')
    def sa_audit(): return redirect(url_for('audit.index'))
    @app.route('/super-admin/settings')
    @app.route('/super-admin/settings/')
    def sa_settings(): return redirect(url_for('settings.index'))

    # Error Handlers
    @app.errorhandler(403)
    def forbidden(e):
        return render_template('errors/403.html'), 403

    @app.errorhandler(404)
    def not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(e):
        return render_template('errors/500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5005))
    print(f"Starting EduFlow ERP Web Server at http://127.0.0.1:{port} ...")
    app.run(host='127.0.0.1', port=port, debug=True)
