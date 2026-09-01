import os
import sys
import json
import uuid
import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import Config
from security.password import PasswordSecurity

def seed_database():
    os.makedirs(Config.DATA_DIR, exist_ok=True)

    # 1. Institutions
    institutions = [
        {'id': 'inst-001', 'code': 'GIS-101', 'name': 'Greenfield International School', 'type': 'School', 'email': 'info@greenfield.edu', 'phone': '+1 (555) 234-5678', 'address': '100 Education Way', 'city': 'Boston', 'state': 'MA', 'country': 'USA', 'established_year': 2008, 'students_count': 1450, 'faculty_count': 92, 'attendance_rate': 96.4, 'fee_collection': 485000.0, 'pending_fees': 24500.0, 'status': 'ACTIVE', 'admin_name': 'Dr. Arthur Pendelton', 'admin_email': 'admin@greenfield.edu', 'created_at': '2026-01-15 09:00:00'},
        {'id': 'inst-002', 'code': 'SXU-202', 'name': 'St. Xavier University', 'type': 'University', 'email': 'contact@stxavier.edu', 'phone': '+1 (555) 876-5432', 'address': '500 University Ave', 'city': 'Chicago', 'state': 'IL', 'country': 'USA', 'established_year': 1995, 'students_count': 8420, 'faculty_count': 410, 'attendance_rate': 93.8, 'fee_collection': 3850000.0, 'pending_fees': 210000.0, 'status': 'ACTIVE', 'admin_name': 'Prof. Sarah Jenkins', 'admin_email': 's.jenkins@stxavier.edu', 'created_at': '2026-01-16 10:30:00'},
        {'id': 'inst-003', 'code': 'AIT-303', 'name': 'Apex Institute of Technology', 'type': 'College', 'email': 'admissions@apextech.edu', 'phone': '+1 (555) 345-6789', 'address': '75 Innovation Blvd', 'city': 'Austin', 'state': 'TX', 'country': 'USA', 'established_year': 2012, 'students_count': 3250, 'faculty_count': 185, 'attendance_rate': 91.5, 'fee_collection': 1420000.0, 'pending_fees': 98000.0, 'status': 'ACTIVE', 'admin_name': 'Dr. Marcus Vance', 'admin_email': 'm.vance@apextech.edu', 'created_at': '2026-01-20 14:15:00'},
        {'id': 'inst-004', 'code': 'MSA-404', 'name': 'Metro Science Academy', 'type': 'School', 'email': 'office@metroscience.edu', 'phone': '+1 (555) 456-7890', 'address': '220 Science Park Rd', 'city': 'Seattle', 'state': 'WA', 'country': 'USA', 'established_year': 2018, 'students_count': 890, 'faculty_count': 58, 'attendance_rate': 88.4, 'fee_collection': 290000.0, 'pending_fees': 45000.0, 'status': 'PENDING', 'admin_name': 'Elena Rostova', 'admin_email': 'e.rostova@metroscience.edu', 'created_at': '2026-02-01 11:20:00'},
        {'id': 'inst-005', 'code': 'HCA-505', 'name': 'Horizon College of Arts', 'type': 'College', 'email': 'admin@horizonarts.edu', 'phone': '+1 (555) 567-8901', 'address': '410 Creative Lane', 'city': 'Denver', 'state': 'CO', 'country': 'USA', 'established_year': 2010, 'students_count': 2100, 'faculty_count': 115, 'attendance_rate': 84.1, 'fee_collection': 680000.0, 'pending_fees': 142000.0, 'status': 'SUSPENDED', 'admin_name': 'Julian Thorne', 'admin_email': 'j.thorne@horizonarts.edu', 'created_at': '2026-02-05 16:45:00'},
        {'id': 'inst-006', 'code': 'PIM-606', 'name': 'Pacific Institute of Management', 'type': 'Institute', 'email': 'contact@pacificmgmt.edu', 'phone': '+1 (555) 678-9012', 'address': '800 Bay Street', 'city': 'San Francisco', 'state': 'CA', 'country': 'USA', 'established_year': 2005, 'students_count': 1850, 'faculty_count': 98, 'attendance_rate': 94.7, 'fee_collection': 920000.0, 'pending_fees': 38000.0, 'status': 'ACTIVE', 'admin_name': 'Dr. Robert Sterling', 'admin_email': 'r.sterling@pacificmgmt.edu', 'created_at': '2026-02-10 08:30:00'},
        {'id': 'inst-007', 'code': 'RAH-707', 'name': 'Royal Academy High', 'type': 'School', 'email': 'admissions@royalacademy.edu', 'phone': '+1 (555) 789-0123', 'address': '330 Crestview Dr', 'city': 'Atlanta', 'state': 'GA', 'country': 'USA', 'established_year': 2015, 'students_count': 1120, 'faculty_count': 74, 'attendance_rate': 95.2, 'fee_collection': 410000.0, 'pending_fees': 18500.0, 'status': 'ACTIVE', 'admin_name': 'Victoria Sterling', 'admin_email': 'v.sterling@royalacademy.edu', 'created_at': '2026-02-14 13:10:00'},
        {'id': 'inst-008', 'code': 'TGU-808', 'name': 'Trinity Global University', 'type': 'University', 'email': 'info@trinityglobal.edu', 'phone': '+1 (555) 890-1234', 'address': '1000 Metropolitan Plaza', 'city': 'New York', 'state': 'NY', 'country': 'USA', 'established_year': 1988, 'students_count': 12400, 'faculty_count': 650, 'attendance_rate': 92.9, 'fee_collection': 5200000.0, 'pending_fees': 310000.0, 'status': 'ACTIVE', 'admin_name': 'Prof. David Kingsley', 'admin_email': 'd.kingsley@trinityglobal.edu', 'created_at': '2026-02-18 15:00:00'}
    ]
    with open(os.path.join(Config.DATA_DIR, 'institutions.json'), 'w', encoding='utf-8') as f:
        json.dump(institutions, f, indent=2)

    # 2. Users
    pwd_hash_admin = PasswordSecurity.hash_password('admin123')
    pwd_hash_teacher = PasswordSecurity.hash_password('teacher123')
    pwd_hash_student = PasswordSecurity.hash_password('student123')

    users = [
        {'id': 'usr-001', 'user_id': 'USR-2026-0001', 'institution_id': 'inst-001', 'username': 'superadmin', 'email': 'admin@eduflow.local', 'password': pwd_hash_admin, 'role': Config.ROLE_SUPER_ADMIN, 'full_name': 'Eleanor Vance', 'status': 'ACTIVE', 'last_login': '2026-09-01 10:15:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-002', 'user_id': 'USR-2026-0002', 'institution_id': 'inst-001', 'username': 'schooladmin', 'email': 'schooladmin@eduflow.local', 'password': pwd_hash_admin, 'role': Config.ROLE_SCHOOL_ADMIN, 'full_name': 'Arthur Pendelton', 'status': 'ACTIVE', 'last_login': '2026-09-01 09:30:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-003', 'user_id': 'USR-2026-0003', 'institution_id': 'inst-002', 'username': 'collegeadmin', 'email': 'collegeadmin@eduflow.local', 'password': pwd_hash_admin, 'role': Config.ROLE_COLLEGE_ADMIN, 'full_name': 'Sophia Sterling', 'status': 'ACTIVE', 'last_login': '2026-08-31 16:45:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-004', 'user_id': 'USR-2026-0004', 'institution_id': 'inst-003', 'username': 'teacher', 'email': 'teacher@eduflow.local', 'password': pwd_hash_teacher, 'role': Config.ROLE_TEACHER, 'full_name': 'Dr. Robert Langdon', 'status': 'ACTIVE', 'last_login': '2026-09-01 08:20:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-005', 'user_id': 'USR-2026-0005', 'institution_id': 'inst-001', 'username': 'student', 'email': 'student@eduflow.local', 'password': pwd_hash_student, 'role': Config.ROLE_STUDENT, 'full_name': 'Alexander Wright', 'status': 'ACTIVE', 'last_login': '2026-09-01 11:10:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-006', 'user_id': 'USR-2026-0006', 'institution_id': 'inst-002', 'username': 'student2', 'email': 'student2@eduflow.local', 'password': pwd_hash_student, 'role': Config.ROLE_STUDENT, 'full_name': 'Beatrix Potter', 'status': 'ACTIVE', 'last_login': '2026-08-30 14:00:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-007', 'user_id': 'USR-2026-0007', 'institution_id': 'inst-003', 'username': 'student3', 'email': 'student3@eduflow.local', 'password': pwd_hash_student, 'role': Config.ROLE_STUDENT, 'full_name': 'Charles Darwin', 'status': 'ACTIVE', 'last_login': '2026-08-29 15:30:00', 'created_at': '2026-01-01 09:00:00'},
        {'id': 'usr-008', 'user_id': 'USR-2026-0008', 'institution_id': 'inst-008', 'username': 'faculty2', 'email': 'david@trinityglobal.edu', 'password': pwd_hash_teacher, 'role': Config.ROLE_FACULTY, 'full_name': 'Prof. David Kingsley', 'status': 'ACTIVE', 'last_login': '2026-09-01 07:45:00', 'created_at': '2026-01-01 09:00:00'}
    ]
    with open(Config.USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=2)

    # 3. Courses / Programs
    courses = [
        {'id': 'crs-001', 'program_code': 'PROG-CS-001', 'institution_id': 'inst-001', 'code': 'CS-101', 'name': 'Computer Science & Engineering', 'department': 'Computer Science', 'duration_years': 4, 'total_semesters': 8, 'status': 'ACTIVE'},
        {'id': 'crs-002', 'program_code': 'PROG-ECE-001', 'institution_id': 'inst-002', 'code': 'ECE-101', 'name': 'Electronics & Communication', 'department': 'Electronics', 'duration_years': 4, 'total_semesters': 8, 'status': 'ACTIVE'},
        {'id': 'crs-003', 'program_code': 'PROG-BUS-001', 'institution_id': 'inst-003', 'code': 'BUS-101', 'name': 'Business Administration', 'department': 'Management', 'duration_years': 3, 'total_semesters': 6, 'status': 'ACTIVE'},
        {'id': 'crs-004', 'program_code': 'PROG-ENG-001', 'institution_id': 'inst-008', 'code': 'ENG-101', 'name': 'Software Engineering', 'department': 'Computer Science', 'duration_years': 4, 'total_semesters': 8, 'status': 'ACTIVE'}
    ]
    with open(Config.COURSES_FILE, 'w', encoding='utf-8') as f:
        json.dump(courses, f, indent=2)

    # 4. Subjects
    subjects = [
        {'id': 'sbj-001', 'subject_code': 'SUB-CS101-001', 'institution_id': 'inst-001', 'code': 'CS101-PY', 'name': 'Python Programming & Data Structures', 'course_id': 'crs-001', 'credits': 4, 'semester': 1},
        {'id': 'sbj-002', 'subject_code': 'SUB-CS102-001', 'institution_id': 'inst-001', 'code': 'CS102-DB', 'name': 'Database Systems & Architecture', 'course_id': 'crs-001', 'credits': 3, 'semester': 1},
        {'id': 'sbj-003', 'subject_code': 'SUB-CS103-001', 'institution_id': 'inst-002', 'code': 'CS103-MATH', 'name': 'Discrete Mathematics', 'course_id': 'crs-002', 'credits': 4, 'semester': 1},
        {'id': 'sbj-004', 'subject_code': 'SUB-ECE101-001', 'institution_id': 'inst-003', 'code': 'ECE101-CKT', 'name': 'Circuit Theory', 'course_id': 'crs-003', 'credits': 4, 'semester': 1}
    ]
    with open(Config.SUBJECTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(subjects, f, indent=2)

    # 5. Teachers / Faculty
    teachers = [
        {'id': 'tch-001', 'faculty_id': 'FAC-2026-0001', 'institution_id': 'inst-001', 'user_id': 'usr-004', 'full_name': 'Dr. Robert Langdon', 'email': 'teacher@eduflow.local', 'phone': '+1 555-0199', 'department': 'Computer Science', 'designation': 'Senior Professor', 'assigned_subject_ids': ['sbj-001', 'sbj-002'], 'assigned_classes': ['CS-101-A', 'CS-101-B'], 'status': 'ACTIVE'},
        {'id': 'tch-002', 'faculty_id': 'FAC-2026-0002', 'institution_id': 'inst-002', 'user_id': 'usr-008', 'full_name': 'Prof. Sarah Connor', 'email': 'faculty@eduflow.local', 'phone': '+1 555-0288', 'department': 'Electronics', 'designation': 'Associate Professor', 'assigned_subject_ids': ['sbj-004'], 'assigned_classes': ['ECE-101-A'], 'status': 'ACTIVE'},
        {'id': 'tch-003', 'faculty_id': 'FAC-2026-0003', 'institution_id': 'inst-008', 'user_id': 'usr-008', 'full_name': 'Prof. David Kingsley', 'email': 'd.kingsley@trinityglobal.edu', 'phone': '+1 555-8901', 'department': 'Computer Science', 'designation': 'Dean of Faculty', 'assigned_subject_ids': ['sbj-001'], 'assigned_classes': ['ENG-101-A'], 'status': 'ACTIVE'}
    ]
    with open(Config.TEACHERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(teachers, f, indent=2)

    # 6. Students
    students = [
        {'id': 'std-001', 'student_id': 'STU-2026-0001', 'institution_id': 'inst-001', 'user_id': 'usr-005', 'full_name': 'Alexander Wright', 'email': 'student@eduflow.local', 'phone': '+1 555-0101', 'gender': 'Male', 'dob': '2004-05-15', 'course_id': 'crs-001', 'class_name': 'CS-101', 'section': 'A', 'semester': 1, 'academic_year': '2026', 'attendance_pct': 96.4, 'guardian_name': 'Jonathan Wright', 'guardian_phone': '+1 555-0909', 'address': '124 Innovation Way, Tech City', 'status': 'ACTIVE', 'enrollment_date': '2026-01-10'},
        {'id': 'std-002', 'student_id': 'STU-2026-0002', 'institution_id': 'inst-002', 'user_id': 'usr-006', 'full_name': 'Beatrix Potter', 'email': 'student2@eduflow.local', 'phone': '+1 555-0102', 'gender': 'Female', 'dob': '2005-02-20', 'course_id': 'crs-002', 'class_name': 'CS-101', 'section': 'A', 'semester': 1, 'academic_year': '2026', 'attendance_pct': 93.8, 'guardian_name': 'Helen Potter', 'guardian_phone': '+1 555-0910', 'address': '45 Meadow Lane, Green Valley', 'status': 'ACTIVE', 'enrollment_date': '2026-01-11'},
        {'id': 'std-003', 'student_id': 'STU-2026-0003', 'institution_id': 'inst-003', 'user_id': 'usr-007', 'full_name': 'Charles Darwin', 'email': 'student3@eduflow.local', 'phone': '+1 555-0103', 'gender': 'Male', 'dob': '2004-11-12', 'course_id': 'crs-003', 'class_name': 'ECE-101', 'section': 'A', 'semester': 1, 'academic_year': '2026', 'attendance_pct': 91.5, 'guardian_name': 'Robert Darwin', 'guardian_phone': '+1 555-0911', 'address': '88 Evolution St, Discovery Town', 'status': 'ACTIVE', 'enrollment_date': '2026-01-12'}
    ]
    with open(Config.STUDENTS_FILE, 'w', encoding='utf-8') as f:
        json.dump(students, f, indent=2)

    # 7. Attendance Records
    attendance = []
    base_date = datetime.date.today() - datetime.timedelta(days=10)
    for i in range(10):
        d = (base_date + datetime.timedelta(days=i)).isoformat()
        attendance.append({'id': str(uuid.uuid4()), 'institution_id': 'inst-001', 'student_id': 'std-001', 'student_name': 'Alexander Wright', 'class_name': 'CS-101', 'section': 'A', 'date': d, 'status': 'PRESENT', 'remarks': 'On time'})
        attendance.append({'id': str(uuid.uuid4()), 'institution_id': 'inst-002', 'student_id': 'std-002', 'student_name': 'Beatrix Potter', 'class_name': 'CS-101', 'section': 'A', 'date': d, 'status': 'PRESENT' if i % 3 != 0 else 'ABSENT', 'remarks': 'Regular' if i % 3 != 0 else 'Sick leave'})
        attendance.append({'id': str(uuid.uuid4()), 'institution_id': 'inst-003', 'student_id': 'std-003', 'student_name': 'Charles Darwin', 'class_name': 'ECE-101', 'section': 'A', 'date': d, 'status': 'PRESENT' if i % 2 == 0 else 'LATE', 'remarks': 'Normal'})
    with open(Config.ATTENDANCE_FILE, 'w', encoding='utf-8') as f:
        json.dump(attendance, f, indent=2)

    # 8. Fees Records
    fees = [
        {'id': 'fee-001', 'fee_code': 'FEE-2026-0001', 'institution_id': 'inst-001', 'student_id': 'std-001', 'student_name': 'Alexander Wright', 'fee_type': 'Tuition Fee', 'total_amount': 2500.0, 'paid_amount': 1500.0, 'pending_amount': 1000.0, 'due_date': '2026-09-30', 'status': 'PARTIAL'},
        {'id': 'fee-002', 'fee_code': 'FEE-2026-0002', 'institution_id': 'inst-002', 'student_id': 'std-002', 'student_name': 'Beatrix Potter', 'fee_type': 'Tuition Fee', 'total_amount': 3800.0, 'paid_amount': 3800.0, 'pending_amount': 0.0, 'due_date': '2026-09-30', 'status': 'PAID'},
        {'id': 'fee-003', 'fee_code': 'FEE-2026-0003', 'institution_id': 'inst-003', 'student_id': 'std-003', 'student_name': 'Charles Darwin', 'fee_type': 'Tuition Fee', 'total_amount': 1420.0, 'paid_amount': 0.0, 'pending_amount': 1420.0, 'due_date': '2026-09-30', 'status': 'PENDING'}
    ]
    with open(Config.FEES_FILE, 'w', encoding='utf-8') as f:
        json.dump(fees, f, indent=2)

    # 9. Audit Logs
    audit = [
        {'id': 'aud-001', 'institution_id': 'inst-001', 'timestamp': '2026-09-01 10:15:00', 'user': 'admin@eduflow.local', 'role': 'SUPER_ADMIN', 'action': 'CREATE_INSTITUTION', 'module': 'Institutions', 'description': 'Registered Greenfield International School', 'status': 'SUCCESS'},
        {'id': 'aud-002', 'institution_id': 'inst-002', 'timestamp': '2026-09-01 09:30:00', 'user': 'schooladmin@eduflow.local', 'role': 'SCHOOL_ADMIN', 'action': 'UPDATE_FEE', 'module': 'Finance', 'description': 'Updated tuition fee ledger for St. Xavier University', 'status': 'SUCCESS'}
    ]
    with open(Config.AUDIT_LOGS_FILE, 'w', encoding='utf-8') as f:
        json.dump(audit, f, indent=2)

    print("EduFlow ERP database seeded successfully with institution-wise data!")

if __name__ == '__main__':
    seed_database()
