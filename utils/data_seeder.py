import os
import json
import uuid
import datetime
from config import Config
from security.password import PasswordSecurity

def seed_database():
    os.makedirs(Config.DATA_DIR, exist_ok=True)

    # 1. Users
    pwd_hash_admin = PasswordSecurity.hash_password('admin123')
    pwd_hash_teacher = PasswordSecurity.hash_password('teacher123')
    pwd_hash_student = PasswordSecurity.hash_password('student123')
    pwd_hash_parent = PasswordSecurity.hash_password('parent123')
    pwd_hash_acct = PasswordSecurity.hash_password('accountant123')
    pwd_hash_lib = PasswordSecurity.hash_password('librarian123')
    pwd_hash_trans = PasswordSecurity.hash_password('transport123')
    pwd_hash_warden = PasswordSecurity.hash_password('warden123')
    pwd_hash_principal = PasswordSecurity.hash_password('principal123')

    u_admin = {'id': 'usr-001', 'username': 'superadmin', 'email': 'admin@eduflow.local', 'password': pwd_hash_admin, 'role': Config.ROLE_SUPER_ADMIN, 'full_name': 'Eleanor Vance', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_school_admin = {'id': 'usr-002', 'username': 'schooladmin', 'email': 'schooladmin@eduflow.local', 'password': pwd_hash_admin, 'role': Config.ROLE_SCHOOL_ADMIN, 'full_name': 'Marcus Vance', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_college_admin = {'id': 'usr-003', 'username': 'collegeadmin', 'email': 'collegeadmin@eduflow.local', 'password': pwd_hash_admin, 'role': Config.ROLE_COLLEGE_ADMIN, 'full_name': 'Sophia Sterling', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_principal = {'id': 'usr-004', 'username': 'principal', 'email': 'principal@eduflow.local', 'password': pwd_hash_principal, 'role': Config.ROLE_PRINCIPAL, 'full_name': 'Dr. Arthur Pendelton', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_teacher1 = {'id': 'usr-005', 'username': 'teacher', 'email': 'teacher@eduflow.local', 'password': pwd_hash_teacher, 'role': Config.ROLE_TEACHER, 'full_name': 'Dr. Robert Langdon', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_faculty1 = {'id': 'usr-006', 'username': 'faculty', 'email': 'faculty@eduflow.local', 'password': pwd_hash_teacher, 'role': Config.ROLE_FACULTY, 'full_name': 'Prof. Sarah Connor', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_student1 = {'id': 'usr-007', 'username': 'student', 'email': 'student@eduflow.local', 'password': pwd_hash_student, 'role': Config.ROLE_STUDENT, 'full_name': 'Alexander Wright', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_student2 = {'id': 'usr-008', 'username': 'student2', 'email': 'student2@eduflow.local', 'password': pwd_hash_student, 'role': Config.ROLE_STUDENT, 'full_name': 'Beatrix Potter', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_student3 = {'id': 'usr-009', 'username': 'student3', 'email': 'student3@eduflow.local', 'password': pwd_hash_student, 'role': Config.ROLE_STUDENT, 'full_name': 'Charles Darwin', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_parent1 = {'id': 'usr-010', 'username': 'parent', 'email': 'parent@eduflow.local', 'password': pwd_hash_parent, 'role': Config.ROLE_PARENT, 'full_name': 'Jonathan Wright', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_acct = {'id': 'usr-011', 'username': 'accountant', 'email': 'accountant@eduflow.local', 'password': pwd_hash_acct, 'role': Config.ROLE_ACCOUNTANT, 'full_name': 'Laura Croft', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_lib = {'id': 'usr-012', 'username': 'librarian', 'email': 'librarian@eduflow.local', 'password': pwd_hash_lib, 'role': Config.ROLE_LIBRARIAN, 'full_name': 'Gutenberg Smith', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_trans = {'id': 'usr-013', 'username': 'transport', 'email': 'transport@eduflow.local', 'password': pwd_hash_trans, 'role': Config.ROLE_TRANSPORT_MANAGER, 'full_name': 'Dominic Toretto', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}
    u_warden = {'id': 'usr-014', 'username': 'warden', 'email': 'warden@eduflow.local', 'password': pwd_hash_warden, 'role': Config.ROLE_HOSTEL_WARDEN, 'full_name': 'Argus Filch', 'status': 'ACTIVE', 'created_at': '2026-01-01 09:00:00'}

    users = [u_admin, u_school_admin, u_college_admin, u_principal, u_teacher1, u_faculty1, u_student1, u_student2, u_student3, u_parent1, u_acct, u_lib, u_trans, u_warden]
    with open(Config.USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

    # 2. Courses
    courses = [
        {'id': 'crs-001', 'code': 'CS-101', 'name': 'Computer Science & Engineering', 'department': 'Computer Science', 'duration_years': 4, 'total_semesters': 8, 'status': 'ACTIVE'},
        {'id': 'crs-002', 'code': 'ECE-101', 'name': 'Electronics & Communication', 'department': 'Electronics', 'duration_years': 4, 'total_semesters': 8, 'status': 'ACTIVE'},
        {'id': 'crs-003', 'code': 'BUS-101', 'name': 'Business Administration', 'department': 'Management', 'duration_years': 3, 'total_semesters': 6, 'status': 'ACTIVE'}
    ]
    with open(Config.COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2)

    # 3. Subjects
    subjects = [
        {'id': 'sbj-001', 'code': 'CS101-PY', 'name': 'Python Programming & Data Structures', 'course_id': 'crs-001', 'credits': 4, 'semester': 1},
        {'id': 'sbj-002', 'code': 'CS102-DB', 'name': 'Database Systems & Architecture', 'course_id': 'crs-001', 'credits': 3, 'semester': 1},
        {'id': 'sbj-003', 'code': 'CS103-MATH', 'name': 'Discrete Mathematics', 'course_id': 'crs-001', 'credits': 4, 'semester': 1},
        {'id': 'sbj-004', 'code': 'ECE101-CKT', 'name': 'Circuit Theory', 'course_id': 'crs-002', 'credits': 4, 'semester': 1}
    ]
    with open(Config.SUBJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(subjects, f, indent=2)

    # 4. Teachers
    teachers = [
        {'id': 'tch-001', 'faculty_id': 'FAC-2026-0001', 'user_id': 'usr-005', 'full_name': 'Dr. Robert Langdon', 'email': 'teacher@eduflow.local', 'phone': '+1 555-0199', 'department': 'Computer Science', 'designation': 'Senior Professor', 'assigned_subject_ids': ['sbj-001', 'sbj-002'], 'assigned_classes': ['CS-101-A', 'CS-101-B'], 'status': 'ACTIVE'},
        {'id': 'tch-002', 'faculty_id': 'FAC-2026-0002', 'user_id': 'usr-006', 'full_name': 'Prof. Sarah Connor', 'email': 'faculty@eduflow.local', 'phone': '+1 555-0288', 'department': 'Electronics', 'designation': 'Associate Professor', 'assigned_subject_ids': ['sbj-004'], 'assigned_classes': ['ECE-101-A'], 'status': 'ACTIVE'}
    ]
    with open(Config.TEACHERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(teachers, f, indent=2)

    # 5. Students
    students = [
        {'id': 'std-001', 'student_id': 'STU-2026-0001', 'user_id': 'usr-007', 'full_name': 'Alexander Wright', 'email': 'student@eduflow.local', 'phone': '+1 555-0101', 'gender': 'Male', 'dob': '2004-05-15', 'course_id': 'crs-001', 'class_name': 'CS-101', 'section': 'A', 'semester': 1, 'academic_year': '2026', 'guardian_name': 'Jonathan Wright', 'guardian_phone': '+1 555-0909', 'address': '124 Innovation Way, Tech City', 'status': 'ACTIVE', 'enrollment_date': '2026-01-10'},
        {'id': 'std-002', 'student_id': 'STU-2026-0002', 'user_id': 'usr-008', 'full_name': 'Beatrix Potter', 'email': 'student2@eduflow.local', 'phone': '+1 555-0102', 'gender': 'Female', 'dob': '2005-02-20', 'course_id': 'crs-001', 'class_name': 'CS-101', 'section': 'A', 'semester': 1, 'academic_year': '2026', 'guardian_name': 'Helen Potter', 'guardian_phone': '+1 555-0910', 'address': '45 Meadow Lane, Green Valley', 'status': 'ACTIVE', 'enrollment_date': '2026-01-11'},
        {'id': 'std-003', 'student_id': 'STU-2026-0003', 'user_id': 'usr-009', 'full_name': 'Charles Darwin', 'email': 'student3@eduflow.local', 'phone': '+1 555-0103', 'gender': 'Male', 'dob': '2004-11-12', 'course_id': 'crs-002', 'class_name': 'ECE-101', 'section': 'A', 'semester': 1, 'academic_year': '2026', 'guardian_name': 'Robert Darwin', 'guardian_phone': '+1 555-0911', 'address': '88 Evolution St, Discovery Town', 'status': 'ACTIVE', 'enrollment_date': '2026-01-12'}
    ]
    with open(Config.STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2)

    # 6. Parents
    parents = [
        {'id': 'prn-001', 'user_id': 'usr-010', 'full_name': 'Jonathan Wright', 'email': 'parent@eduflow.local', 'phone': '+1 555-0909', 'occupation': 'Senior Engineer', 'student_ids': ['std-001'], 'address': '124 Innovation Way, Tech City'}
    ]
    with open(Config.PARENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(parents, f, indent=2)

    # 7. Attendance (Past 10 days seed)
    attendance = []
    base_date = datetime.date.today() - datetime.timedelta(days=10)
    for i in range(10):
        d = (base_date + datetime.timedelta(days=i)).isoformat()
        attendance.append({'id': str(uuid.uuid4()), 'student_id': 'std-001', 'class_name': 'CS-101', 'section': 'A', 'date': d, 'status': 'PRESENT', 'remarks': 'On time'})
        attendance.append({'id': str(uuid.uuid4()), 'student_id': 'std-002', 'class_name': 'CS-101', 'section': 'A', 'date': d, 'status': 'PRESENT' if i % 3 != 0 else 'ABSENT', 'remarks': 'Regular' if i % 3 != 0 else 'Sick leave'})
        attendance.append({'id': str(uuid.uuid4()), 'student_id': 'std-003', 'class_name': 'ECE-101', 'section': 'A', 'date': d, 'status': 'PRESENT' if i % 2 == 0 else 'LATE', 'remarks': 'Normal'})
    with open(Config.ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(attendance, f, indent=2)

    # 8. Exams
    exams = [
        {'id': 'exm-001', 'exam_id': 'EXM-2026-0001', 'title': 'Mid-Term Examinations 2026', 'course_id': 'crs-001', 'subject_id': 'sbj-001', 'exam_date': '2026-09-15', 'start_time': '09:00', 'end_time': '12:00', 'room': 'Auditorium A', 'max_marks': 100, 'pass_marks': 40, 'status': 'SCHEDULED'},
        {'id': 'exm-002', 'exam_id': 'EXM-2026-0002', 'title': 'Database Systems Quiz 1', 'course_id': 'crs-001', 'subject_id': 'sbj-002', 'exam_date': '2026-08-20', 'start_time': '10:00', 'end_time': '11:00', 'room': 'Lab 3', 'max_marks': 50, 'pass_marks': 20, 'status': 'COMPLETED'}
    ]
    with open(Config.EXAMS_FILE, 'w', encoding='utf-8') as f:
        json.dump(exams, f, indent=2)

    # 9. Marks
    marks = [
        {'id': 'mrk-001', 'exam_id': 'exm-002', 'student_id': 'std-001', 'subject_id': 'sbj-002', 'marks_obtained': 46, 'max_marks': 50, 'grade': 'A+', 'gpa': 4.0, 'status': 'PASSED', 'remarks': 'Excellent performance'},
        {'id': 'mrk-002', 'exam_id': 'exm-002', 'student_id': 'std-002', 'subject_id': 'sbj-002', 'marks_obtained': 38, 'max_marks': 50, 'grade': 'A', 'gpa': 3.7, 'status': 'PASSED', 'remarks': 'Very Good'},
        {'id': 'mrk-003', 'exam_id': 'exm-002', 'student_id': 'std-003', 'subject_id': 'sbj-004', 'marks_obtained': 22, 'max_marks': 50, 'grade': 'C', 'gpa': 2.0, 'status': 'PASSED', 'remarks': 'Needs improvement'}
    ]
    with open(Config.MARKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(marks, f, indent=2)

    # 10. Assignments
    assignments = [
        {'id': 'asg-001', 'title': 'Flask Web Architecture Project', 'course_id': 'crs-001', 'subject_id': 'sbj-001', 'teacher_id': 'tch-001', 'due_date': '2026-09-10', 'description': 'Build a multi-tier Flask web app with clean repository architecture.', 'max_points': 100, 'submissions': [
            {'student_id': 'std-001', 'submitted_at': '2026-08-28 14:00:00', 'content': 'https://github.com/demo/flask-app', 'status': 'GRADED', 'grade': 95, 'feedback': 'Outstanding code structure!'}
        ]},
        {'id': 'asg-002', 'title': 'SQL Query Optimization Problem Set', 'course_id': 'crs-001', 'subject_id': 'sbj-002', 'teacher_id': 'tch-001', 'due_date': '2026-09-15', 'description': 'Optimize indexing and join strategies for 1M records.', 'max_points': 50, 'submissions': []}
    ]
    with open(Config.ASSIGNMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(assignments, f, indent=2)

    # 11. Fees
    fees = [
        {'id': 'fee-001', 'fee_code': 'FEE-2026-0001', 'student_id': 'std-001', 'title': 'Fall 2026 Tuition Fee', 'total_amount': 2500.0, 'discount_amount': 200.0, 'net_amount': 2300.0, 'paid_amount': 1500.0, 'pending_amount': 800.0, 'due_date': '2026-09-30', 'status': 'PARTIAL'},
        {'id': 'fee-002', 'fee_code': 'FEE-2026-0002', 'student_id': 'std-002', 'title': 'Fall 2026 Tuition Fee', 'total_amount': 2500.0, 'discount_amount': 0.0, 'net_amount': 2500.0, 'paid_amount': 2500.0, 'pending_amount': 0.0, 'due_date': '2026-09-30', 'status': 'PAID'},
        {'id': 'fee-003', 'fee_code': 'FEE-2026-0003', 'student_id': 'std-003', 'title': 'Fall 2026 Tuition Fee', 'total_amount': 2500.0, 'discount_amount': 0.0, 'net_amount': 2500.0, 'paid_amount': 0.0, 'pending_amount': 2500.0, 'due_date': '2026-09-30', 'status': 'PENDING'}
    ]
    with open(Config.FEES_FILE, 'w', encoding='utf-8') as f:
        json.dump(fees, f, indent=2)

    # 12. Payments
    payments = [
        {'id': 'pay-001', 'payment_code': 'PAY-2026-00001', 'fee_id': 'fee-001', 'student_id': 'std-001', 'amount': 1500.0, 'payment_method': 'CARD', 'transaction_ref': 'TXN-998811', 'payment_date': '2026-08-15 11:30:00', 'receipt_no': 'RCP-2026-001', 'remarks': 'Initial installment paid via Card simulation'}
    ]
    with open(Config.PAYMENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(payments, f, indent=2)

    # 13. Books
    books = [
        {'id': 'bk-001', 'isbn': '978-0131103627', 'title': 'The C Programming Language', 'author': 'Brian Kernighan & Dennis Ritchie', 'category': 'Computer Science', 'total_copies': 10, 'available_copies': 8, 'rack_number': 'CS-01'},
        {'id': 'bk-002', 'isbn': '978-0262033848', 'title': 'Introduction to Algorithms', 'author': 'Thomas H. Cormen', 'category': 'Computer Science', 'total_copies': 5, 'available_copies': 4, 'rack_number': 'CS-02'},
        {'id': 'bk-003', 'isbn': '978-0134685991', 'title': 'Effective Java', 'author': 'Joshua Bloch', 'category': 'Programming', 'total_copies': 7, 'available_copies': 7, 'rack_number': 'CS-04'}
    ]
    with open(Config.BOOKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(books, f, indent=2)

    # 14. Library Transactions
    library_txns = [
        {'id': 'lib-001', 'book_id': 'bk-001', 'book_title': 'The C Programming Language', 'student_id': 'std-001', 'issue_date': '2026-08-10', 'due_date': '2026-08-24', 'return_date': None, 'status': 'ISSUED', 'fine_amount': 0.0}
    ]
    with open(Config.LIBRARY_FILE, 'w', encoding='utf-8') as f:
        json.dump(library_txns, f, indent=2)

    # 15. Hostels
    hostels = [
        {'id': 'hst-001', 'name': 'Newton Hall (Boys)', 'type': 'BOYS', 'warden_name': 'Argus Filch', 'warden_phone': '+1 555-9090', 'total_rooms': 20, 'rooms': [
            {'room_no': '101', 'capacity': 2, 'occupied': 1, 'fee_per_term': 1200.0, 'allocations': [{'student_id': 'std-001', 'student_name': 'Alexander Wright', 'allocated_at': '2026-01-15'}]},
            {'room_no': '102', 'capacity': 2, 'occupied': 0, 'fee_per_term': 1200.0, 'allocations': []}
        ]},
        {'id': 'hst-002', 'name': 'Curie House (Girls)', 'type': 'GIRLS', 'warden_name': 'Minerva McGonagall', 'warden_phone': '+1 555-9091', 'total_rooms': 20, 'rooms': [
            {'room_no': '201', 'capacity': 2, 'occupied': 1, 'fee_per_term': 1200.0, 'allocations': [{'student_id': 'std-002', 'student_name': 'Beatrix Potter', 'allocated_at': '2026-01-16'}]}
        ]}
    ]
    with open(Config.HOSTELS_FILE, 'w', encoding='utf-8') as f:
        json.dump(hostels, f, indent=2)

    # 16. Transport Routes
    transport = [
        {'id': 'trn-001', 'route_name': 'North Campus Express (Route A)', 'vehicle_number': 'BUS-101', 'driver_name': 'Dominic Toretto', 'driver_phone': '+1 555-7788', 'capacity': 30, 'current_capacity': 2, 'monthly_fee': 150.0, 'stops': ['Central Station', 'Green Valley Park', 'EduFlow Gate 1'], 'assigned_student_ids': ['std-001', 'std-003']}
    ]
    with open(Config.TRANSPORT_FILE, 'w', encoding='utf-8') as f:
        json.dump(transport, f, indent=2)

    # 17. Leave Applications
    leave = [
        {'id': 'lve-001', 'applicant_id': 'std-002', 'applicant_name': 'Beatrix Potter', 'role': 'STUDENT', 'leave_type': 'Medical Leave', 'start_date': '2026-09-01', 'end_date': '2026-09-03', 'reason': 'Dental surgery recovery', 'status': 'APPROVED', 'approved_by': 'Dr. Robert Langdon', 'created_at': '2026-08-25'}
    ]
    with open(Config.LEAVE_FILE, 'w', encoding='utf-8') as f:
        json.dump(leave, f, indent=2)

    # 18. Events & Announcements
    events = [
        {'id': 'evt-001', 'title': 'Annual EduFlow Tech Hackathon 2026', 'category': 'EVENT', 'target_audience': 'EVERYONE', 'event_date': '2026-10-12', 'location': 'Main Auditorium', 'description': '48-hour competitive innovation hackathon open to all faculties and students.', 'created_by': 'Super Admin'},
        {'id': 'evt-002', 'title': 'Fall Semester Mid-Term Examination Schedule', 'category': 'ANNOUNCEMENT', 'target_audience': 'STUDENTS', 'event_date': '2026-09-15', 'location': 'Exam Halls', 'description': 'Official timetable published. Please inspect your individual portal for room seating.', 'created_by': 'School Admin'}
    ]
    with open(Config.EVENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(events, f, indent=2)

    # 19. Notifications
    notifications = [
        {'id': 'ntf-001', 'recipient_id': 'usr-007', 'recipient_role': 'STUDENT', 'title': 'Fee Payment Received', 'message': 'Payment of $1,500.00 received for Fall 2026 Tuition Fee.', 'type': 'INFO', 'read': False, 'timestamp': '2026-08-15 11:30:00'},
        {'id': 'ntf-002', 'recipient_id': 'usr-007', 'recipient_role': 'STUDENT', 'title': 'New Assignment Posted', 'message': 'Flask Web Architecture Project assigned in Python Programming.', 'type': 'WARNING', 'read': True, 'timestamp': '2026-08-20 10:00:00'}
    ]
    with open(Config.NOTIFICATIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(notifications, f, indent=2)

    # 20. Admissions
    admissions = [
        {'id': 'adm-001', 'application_no': 'ADM-2026-0001', 'applicant_name': 'Eleanor Vance', 'email': 'eleanor.applicant@example.com', 'phone': '+1 555-0333', 'course_id': 'crs-001', 'previous_qualification': 'High School Diploma (GPA 3.9)', 'status': 'UNDER_REVIEW', 'applied_date': '2026-08-20', 'remarks': 'Transcripts verified'},
        {'id': 'adm-002', 'application_no': 'ADM-2026-0002', 'applicant_name': 'Julian Casablancas', 'email': 'julian.applicant@example.com', 'phone': '+1 555-0444', 'course_id': 'crs-002', 'previous_qualification': 'Diploma in Electronics', 'status': 'APPROVED', 'applied_date': '2026-08-18', 'remarks': 'Ready for fee enrollment'}
    ]
    with open(Config.ADMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(admissions, f, indent=2)

    # 21. Timetable
    timetable = [
        {'id': 'tt-001', 'class_name': 'CS-101', 'section': 'A', 'day': 'Monday', 'start_time': '09:00', 'end_time': '10:00', 'subject_id': 'sbj-001', 'subject_name': 'Python Programming', 'teacher_id': 'tch-001', 'teacher_name': 'Dr. Robert Langdon', 'room': 'Room 101'},
        {'id': 'tt-002', 'class_name': 'CS-101', 'section': 'A', 'day': 'Monday', 'start_time': '10:00', 'end_time': '11:00', 'subject_id': 'sbj-002', 'subject_name': 'Database Systems', 'teacher_id': 'tch-001', 'teacher_name': 'Dr. Robert Langdon', 'room': 'Lab 2'},
        {'id': 'tt-003', 'class_name': 'ECE-101', 'section': 'A', 'day': 'Tuesday', 'start_time': '11:00', 'end_time': '12:00', 'subject_id': 'sbj-004', 'subject_name': 'Circuit Theory', 'teacher_id': 'tch-002', 'teacher_name': 'Prof. Sarah Connor', 'room': 'Room 204'}
    ]
    with open(Config.TIMETABLE_FILE, 'w', encoding='utf-8') as f:
        json.dump(timetable, f, indent=2)

    # 22. Audit Logs
    audit = [
        {'id': 'aud-001', 'user': 'admin@eduflow.local', 'role': 'SUPER_ADMIN', 'action': 'SYSTEM_SEED', 'entity': 'SYSTEM', 'details': 'Initial system data seeded successfully.', 'timestamp': '2026-01-01 09:00:00'}
    ]
    with open(Config.AUDIT_LOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2)

    print("EduFlow ERP database seeded successfully with demo accounts!")

if __name__ == '__main__':
    seed_database()
