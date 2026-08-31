from typing import Optional, Dict, Any, List, Tuple
import datetime
from repositories.attendance_repository import AttendanceRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils
import uuid

class AttendanceService:
    def __init__(self):
        self.attendance_repo = AttendanceRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_attendance_overview(self, date_str: str = None, class_name: str = 'CS-101', section: str = 'A') -> Dict[str, Any]:
        if not date_str:
            date_str = DateTimeUtils.current_date_str()

        students = self.student_repo.find_by_class_and_section(class_name, section)
        attendance_records = self.attendance_repo.find_by_date(date_str)
        
        att_map = {r['student_id']: r for r in attendance_records}

        student_list = []
        present_cnt = 0
        absent_cnt = 0
        late_cnt = 0
        excused_cnt = 0

        for std in students:
            att = att_map.get(std['id'])
            status = att.get('status') if att else 'PRESENT'
            remarks = att.get('remarks') if att else ''

            if status == 'PRESENT':
                present_cnt += 1
            elif status == 'ABSENT':
                absent_cnt += 1
            elif status == 'LATE':
                late_cnt += 1
            elif status == 'EXCUSED':
                excused_cnt += 1

            student_list.append({
                'student_id': std['id'],
                'student_code': std['student_id'],
                'full_name': std['full_name'],
                'status': status,
                'remarks': remarks,
                'overall_pct': self.attendance_repo.get_attendance_percentage(std['id'])
            })

        total = len(students)
        pct = round((present_cnt + late_cnt + excused_cnt) / total * 100.0, 1) if total > 0 else 100.0

        return {
            'date': date_str,
            'class_name': class_name,
            'section': section,
            'students': student_list,
            'stats': {
                'total': total,
                'present': present_cnt,
                'absent': absent_cnt,
                'late': late_cnt,
                'excused': excused_cnt,
                'attendance_pct': pct
            }
        }

    def save_bulk_attendance(self, date_str: str, class_name: str, section: str, attendance_data: List[Dict[str, Any]], actor_email: str, actor_role: str) -> Tuple[bool, str]:
        if not date_str:
            date_str = DateTimeUtils.current_date_str()

        for item in attendance_data:
            student_id = item.get('student_id')
            status = item.get('status', 'PRESENT')
            remarks = item.get('remarks', '')

            existing = self.attendance_repo.find_by_student_and_date(student_id, date_str)
            if existing:
                self.attendance_repo.update(existing['id'], {'status': status, 'remarks': remarks})
            else:
                new_record = {
                    'id': str(uuid.uuid4()),
                    'student_id': student_id,
                    'class_name': class_name,
                    'section': section,
                    'date': date_str,
                    'status': status,
                    'remarks': remarks
                }
                self.attendance_repo.create(new_record)

        self.audit_repo.log_action(actor_email, actor_role, 'MARK_ATTENDANCE', 'ATTENDANCE', f"Marked bulk attendance for {class_name}-{section} on {date_str}")
        return True, f"Attendance for {class_name}-{section} on {date_str} saved successfully."
