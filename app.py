import os
from flask import Flask, render_template
from config import Config
from utils.data_seeder import seed_database

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Ensure database seeded on startup
    if not os.path.exists(Config.USERS_FILE):
        seed_database()

    # Register Blueprints
    from routes.auth_routes import auth_bp
    from routes.dashboard_routes import dashboard_bp
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
    from routes.ml_routes import ml_bp
    from routes.search_routes import search_bp
    from routes.audit_routes import audit_bp
    from routes.notification_routes import notifications_bp
    from routes.portal_routes import portal_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
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
    app.register_blueprint(ml_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(audit_bp)
    app.register_blueprint(notifications_bp)
    app.register_blueprint(portal_bp)

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
