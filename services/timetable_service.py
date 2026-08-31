"""
EduFlow ERP Service — TimetableService
Weekly class schedule, slot booking, and real-time teacher/room conflict detection algorithm.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.timetable_repository import TimetableRepository
from repositories.teacher_repository import TeacherRepository
from repositories.subject_repository import SubjectRepository
from repositories.audit_repository import AuditRepository

class TimetableService:
    def __init__(self):
        self.timetable_repo = TimetableRepository()
        self.repo = self.timetable_repo
        self.teacher_repo = TeacherRepository()
        self.subject_repo = SubjectRepository()
        self.audit_repo = AuditRepository()

    def get_timetable_grid(self, class_name: str = 'CS-101', section: str = 'A') -> Dict[str, Any]:
        return self.timetable_repo.get_grid_by_class(class_name, section)

    def add_period(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]], List[str]]:
        class_name = data.get('class_name', 'CS-101')
        section = data.get('section', 'A')
        day = data.get('day_of_week', 'Monday')
        start_time = data.get('start_time', '09:00 AM')
        end_time = data.get('end_time', '10:00 AM')
        subject_id = data.get('subject_id', '')
        teacher_id = data.get('teacher_id', '')
        room = data.get('room_no', '101')

        has_conflict, conflicts = self.timetable_repo.check_conflicts(day, start_time, end_time, teacher_id, room, class_name, section)
        if has_conflict:
            return False, f"Schedule Conflict Detected: {'; '.join(conflicts)}", None, conflicts

        count = self.timetable_repo.count() + 1
        period_data = {
            'id': f"slot-{count:04d}",
            'class_name': class_name,
            'section': section,
            'day_of_week': day,
            'start_time': start_time,
            'end_time': end_time,
            'subject_id': subject_id,
            'teacher_id': teacher_id,
            'room_no': room
        }
        created = self.timetable_repo.create(period_data)
        self.audit_repo.log_action(actor_email, actor_role, 'ADD_TIMETABLE_PERIOD', 'TIMETABLE', f"Scheduled period {day} {start_time} for class {class_name}")
        return True, "Timetable period scheduled successfully.", created, []

    def delete_period(self, period_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        period = self.timetable_repo.find_by_id(period_id)
        if not period:
            return False, "Timetable period not found."

        self.timetable_repo.delete(period_id)
        self.audit_repo.log_action(actor_email, actor_role, 'DELETE_TIMETABLE_PERIOD', 'TIMETABLE', f"Deleted period {period_id}")
        return True, "Timetable period deleted successfully."
