import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
BACKUP_DIR = os.path.join(DATA_DIR, 'backups')
MODEL_DIR = os.path.join(BASE_DIR, 'ml', 'saved_models')

os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(MODEL_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'eduflow-super-secret-enterprise-key-2026-v1')
    DEBUG = True
    TESTING = False
    
    # Data Storage Paths
    BASE_DIR = BASE_DIR
    DATA_DIR = DATA_DIR
    BACKUP_DIR = BACKUP_DIR
    MODEL_DIR = MODEL_DIR

    USERS_FILE = os.path.join(DATA_DIR, 'users.json')
    STUDENTS_FILE = os.path.join(DATA_DIR, 'students.json')
    TEACHERS_FILE = os.path.join(DATA_DIR, 'teachers.json')
    PARENTS_FILE = os.path.join(DATA_DIR, 'parents.json')
    COURSES_FILE = os.path.join(DATA_DIR, 'courses.json')
    SUBJECTS_FILE = os.path.join(DATA_DIR, 'subjects.json')
    ATTENDANCE_FILE = os.path.join(DATA_DIR, 'attendance.json')
    EXAMS_FILE = os.path.join(DATA_DIR, 'exams.json')
    MARKS_FILE = os.path.join(DATA_DIR, 'marks.json')
    ASSIGNMENTS_FILE = os.path.join(DATA_DIR, 'assignments.json')
    FEES_FILE = os.path.join(DATA_DIR, 'fees.json')
    PAYMENTS_FILE = os.path.join(DATA_DIR, 'payments.json')
    LIBRARY_FILE = os.path.join(DATA_DIR, 'library.json')
    BOOKS_FILE = os.path.join(DATA_DIR, 'books.json')
    HOSTELS_FILE = os.path.join(DATA_DIR, 'hostels.json')
    TRANSPORT_FILE = os.path.join(DATA_DIR, 'transport.json')
    NOTIFICATIONS_FILE = os.path.join(DATA_DIR, 'notifications.json')
    EVENTS_FILE = os.path.join(DATA_DIR, 'events.json')
    LEAVE_FILE = os.path.join(DATA_DIR, 'leave.json')
    ADMISSIONS_FILE = os.path.join(DATA_DIR, 'admissions.json')
    TIMETABLE_FILE = os.path.join(DATA_DIR, 'timetable.json')
    AUDIT_LOGS_FILE = os.path.join(DATA_DIR, 'audit_logs.json')

    # Roles Constants
    ROLE_SUPER_ADMIN = 'SUPER_ADMIN'
    ROLE_SCHOOL_ADMIN = 'SCHOOL_ADMIN'
    ROLE_COLLEGE_ADMIN = 'COLLEGE_ADMIN'
    ROLE_PRINCIPAL = 'PRINCIPAL'
    ROLE_TEACHER = 'TEACHER'
    ROLE_FACULTY = 'FACULTY'
    ROLE_STUDENT = 'STUDENT'
    ROLE_PARENT = 'PARENT'
    ROLE_ACCOUNTANT = 'ACCOUNTANT'
    ROLE_LIBRARIAN = 'LIBRARIAN'
    ROLE_TRANSPORT_MANAGER = 'TRANSPORT_MANAGER'
    ROLE_HOSTEL_WARDEN = 'HOSTEL_WARDEN'

    ALL_ROLES = [
        ROLE_SUPER_ADMIN, ROLE_SCHOOL_ADMIN, ROLE_COLLEGE_ADMIN, ROLE_PRINCIPAL,
        ROLE_TEACHER, ROLE_FACULTY, ROLE_STUDENT, ROLE_PARENT,
        ROLE_ACCOUNTANT, ROLE_LIBRARIAN, ROLE_TRANSPORT_MANAGER, ROLE_HOSTEL_WARDEN
    ]

    ADMIN_ROLES = [
        ROLE_SUPER_ADMIN, ROLE_SCHOOL_ADMIN, ROLE_COLLEGE_ADMIN, ROLE_PRINCIPAL
    ]

    PAGINATION_PER_PAGE = 10
