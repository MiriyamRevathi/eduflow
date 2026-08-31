"""
EduFlow ERP Repository — AssignmentRepository
Data access layer for Assignment handling JSON storage persistence, indexing, and queries.
"""
from typing import Optional, Dict, Any, List, Tuple
import os
from config import Config
from repositories.base_repository import BaseRepository

class AssignmentRepository(BaseRepository):
    def __init__(self):
        file_key = "ASSIGNMENTS_FILE" if "assignment" not in ["teacher", "audit", "hostel", "transport", "timetable", "leave", "event", "admission"] else ("TEACHERS_FILE" if "assignment" == "teacher" else ("AUDIT_LOGS_FILE" if "assignment" == "audit" else "ASSIGNMENT_FILE" if "assignment" in ["timetable", "leave"] else "ASSIGNMENTS_FILE"))
        path = getattr(Config, file_key, os.path.join(Config.DATA_DIR, f"assignments.json"))
        super().__init__(path, id_field='id')

    def find_by_code(self, code: str) -> Optional[Dict[str, Any]]:
        """Find record by unique code identifier."""
        if not code:
            return None
        return self.find_one_by_field('code', code.strip())

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        """Filter records by status value."""
        return self.find_by_field('status', status)

    def find_active(self) -> List[Dict[str, Any]]:
        """Retrieve all active records."""
        return self.find_by_field('status', 'ACTIVE')

    def search_by_keyword(self, keyword: str, fields: List[str] = None) -> List[Dict[str, Any]]:
        """Perform text search across multiple schema fields."""
        if not fields:
            fields = ['name', 'code', 'title', 'email', 'description', 'id', 'student_id', 'faculty_id', 'fee_code', 'isbn']
        return self.search(keyword, fields)

    def bulk_create(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Batch insert records atomically."""
        created_items = []
        for item in items:
            created_items.append(self.create(item))
        return created_items

    def bulk_update_status(self, ids: List[str], new_status: str) -> int:
        """Batch update status for multiple record IDs."""
        count = 0
        for item_id in ids:
            if self.update(item_id, {'status': new_status}):
                count += 1
        return count

    def get_summary_stats(self) -> Dict[str, Any]:
        """Compute collection summary stats."""
        all_records = self.find_all()
        total_count = len(all_records)
        active_count = sum(1 for r in all_records if r.get('status') == 'ACTIVE')
        inactive_count = sum(1 for r in all_records if r.get('status') in ['INACTIVE', 'ARCHIVED'])
        return {
            'total': total_count,
            'active': active_count,
            'inactive': inactive_count,
            'active_ratio_pct': round((active_count / total_count * 100.0), 1) if total_count > 0 else 0.0
        }

    def get_paginated_filtered(
        self,
        page: int = 1,
        per_page: int = 10,
        status: Optional[str] = None,
        query: Optional[str] = None,
        sort_by: str = 'id',
        order: str = 'asc'
    ) -> Dict[str, Any]:
        """Paginate records with filters and sorting."""
        criteria = {}
        if status:
            criteria['status'] = status
        search_fields = ['name', 'code', 'title', 'email', 'id', 'student_id', 'faculty_id', 'fee_code', 'isbn']
        return self.paginate(
            page=page,
            per_page=per_page,
            criteria=criteria,
            search_query=query,
            search_fields=search_fields,
            sort_by=sort_by,
            order=order
        )

    # Key entity repository methods
    def find_by_student_id(self, student_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('student_id', student_id)

    def find_by_user_id(self, user_id: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('user_id', user_id)

    def find_by_course(self, course_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('course_id', course_id)

    def find_by_class_and_section(self, class_name: str, section: str) -> List[Dict[str, Any]]:
        return self.find_where({'class_name': class_name, 'section': section})

    def find_by_email(self, email: str) -> Optional[Dict[str, Any]]:
        if not email:
            return None
        return self.find_one_by_field('email', email.strip().lower())

    def find_by_role(self, role: str) -> List[Dict[str, Any]]:
        return self.find_by_field('role', role)

    def find_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)

    def find_by_date(self, date_str: str) -> List[Dict[str, Any]]:
        return self.find_by_field('date', date_str)

    def find_by_student_and_date(self, student_id: str, date_str: str) -> Optional[Dict[str, Any]]:
        records = self.find_where({'student_id': student_id, 'date': date_str})
        return records[0] if records else None

    def get_attendance_percentage(self, student_id: str) -> float:
        records = self.find_by_student(student_id)
        if not records:
            return 100.0
        present_count = sum(1 for r in records if r.get('status') in ['PRESENT', 'LATE', 'EXCUSED'])
        return round((present_count / len(records)) * 100.0, 2)

    def find_by_exam(self, exam_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('exam_id', exam_id)

    def find_by_student_and_exam(self, student_id: str, exam_id: str) -> Optional[Dict[str, Any]]:
        records = self.find_where({'student_id': student_id, 'exam_id': exam_id})
        return records[0] if records else None

    def find_by_fee_id(self, fee_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('fee_id', fee_id)

    def find_by_isbn(self, isbn: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('isbn', isbn)

    def find_issued_to_student(self, student_id: str) -> List[Dict[str, Any]]:
        records = self.find_by_field('student_id', student_id)
        return [r for r in records if r.get('status') == 'ISSUED']

    def find_all_by_student(self, student_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('student_id', student_id)

    def find_by_vehicle_number(self, vehicle_number: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('vehicle_number', vehicle_number)

    def find_by_applicant(self, applicant_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('applicant_id', applicant_id)

    def find_upcoming(self) -> List[Dict[str, Any]]:
        records = self.find_all()
        return sorted(records, key=lambda x: x.get('event_date', ''), reverse=False)

    def find_by_application_number(self, application_no: str) -> Optional[Dict[str, Any]]:
        return self.find_one_by_field('application_no', application_no)

    def find_by_teacher(self, teacher_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('teacher_id', teacher_id)

    def check_conflict(self, day: str, start_time: str, end_time: str, teacher_id: str = None, room: str = None, exclude_id: str = None) -> List[str]:
        conflicts = []
        all_entries = self.find_all()
        for item in all_entries:
            if exclude_id and str(item.get('id')) == str(exclude_id):
                continue
            if item.get('day') == day:
                e_start = item.get('start_time')
                e_end = item.get('end_time')
                if not (end_time <= e_start or start_time >= e_end):
                    if teacher_id and item.get('teacher_id') == teacher_id:
                        conflicts.append(f"Teacher Conflict: {item.get('teacher_name')} is already teaching {item.get('subject_name')} in {item.get('class_name')}-{item.get('section')} at {e_start}-{e_end}")
                    if room and item.get('room') == room:
                        conflicts.append(f"Room Conflict: Room {room} is already occupied by {item.get('class_name')}-{item.get('section')} at {e_start}-{e_end}")
        return conflicts

    def log_action(self, user_email: str, user_role: str, action: str, entity: str, details: str = ''):
        import uuid
        import datetime
        log_entry = {
            'id': str(uuid.uuid4()),
            'user': user_email,
            'role': user_role,
            'action': action,
            'entity': entity,
            'details': details,
            'timestamp': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.create(log_entry)

    def get_recent(self, limit: int = 20) -> List[Dict[str, Any]]:
        logs = self.find_all()
        return sorted(logs, key=lambda x: x.get('timestamp', ''), reverse=True)[:limit]
