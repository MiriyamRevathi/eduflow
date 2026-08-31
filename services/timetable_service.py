from typing import Optional, Dict, Any, List, Tuple
from repositories.timetable_repository import TimetableRepository
from repositories.teacher_repository import TeacherRepository
from repositories.subject_repository import SubjectRepository
from repositories.audit_repository import AuditRepository
import uuid

class TimetableService:
    def __init__(self):
        self.timetable_repo = TimetableRepository()
        self.teacher_repo = TeacherRepository()
        self.subject_repo = SubjectRepository()
        self.audit_repo = AuditRepository()

    def get_timetable_grid(self, class_name: str = 'CS-101', section: str = 'A') -> Dict[str, Any]:
        entries = self.timetable_repo.find_by_class_and_section(class_name, section)
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
        grid = {day: [] for day in days}
        for item in entries:
            d = item.get('day')
            if d in grid:
                grid[d].append(item)

        for d in days:
            grid[d] = sorted(grid[d], key=lambda x: x.get('start_time', ''))

        return {
            'class_name': class_name,
            'section': section,
            'grid': grid
        }

    def add_period(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]], List[str]]:
        day = data.get('day')
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        teacher_id = data.get('teacher_id')
        room = data.get('room')
        subject_id = data.get('subject_id')

        conflicts = self.timetable_repo.check_conflict(day, start_time, end_time, teacher_id=teacher_id, room=room)
        if conflicts:
            return False, "Timetable scheduling conflict detected!", None, conflicts

        teacher = self.teacher_repo.find_by_id(teacher_id)
        subject = self.subject_repo.find_by_id(subject_id)

        period_data = {
            'id': f"tt-{uuid.uuid4().hex[:6]}",
            'class_name': data.get('class_name', 'CS-101'),
            'section': data.get('section', 'A'),
            'day': day,
            'start_time': start_time,
            'end_time': end_time,
            'subject_id': subject_id,
            'subject_name': subject.get('name') if subject else 'N/A',
            'teacher_id': teacher_id,
            'teacher_name': teacher.get('full_name') if teacher else 'N/A',
            'room': room
        }

        created = self.timetable_repo.create(period_data)
        self.audit_repo.log_action(actor_email, actor_role, 'ADD_TIMETABLE_PERIOD', 'TIMETABLE', f"Scheduled period for {period_data['class_name']}-{period_data['section']} on {day} ({start_time}-{end_time})")
        return True, "Period scheduled successfully without conflicts.", created, []

    def delete_period(self, period_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        success = self.timetable_repo.delete(period_id)
        if success:
            self.audit_repo.log_action(actor_email, actor_role, 'DELETE_TIMETABLE_PERIOD', 'TIMETABLE', f"Deleted timetable period {period_id}")
            return True, "Period deleted successfully."
        return False, "Period not found."
