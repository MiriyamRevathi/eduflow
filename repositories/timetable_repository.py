from typing import Optional, Dict, Any, List
from config import Config
from repositories.base_repository import BaseRepository

class TimetableRepository(BaseRepository):
    def __init__(self):
        super().__init__(Config.TIMETABLE_FILE, id_field='id')

    def find_by_class_and_section(self, class_name: str, section: str) -> List[Dict[str, Any]]:
        return self.find_where({'class_name': class_name, 'section': section})

    def find_by_teacher(self, teacher_id: str) -> List[Dict[str, Any]]:
        return self.find_by_field('teacher_id', teacher_id)

    def check_conflict(self, day: str, start_time: str, end_time: str, teacher_id: str = None, room: str = None, exclude_id: str = None) -> List[str]:
        conflicts = []
        all_entries = self.find_all()
        for item in all_entries:
            if exclude_id and str(item.get('id')) == str(exclude_id):
                continue
            if item.get('day') == day:
                # check time overlap
                e_start = item.get('start_time')
                e_end = item.get('end_time')
                if not (end_time <= e_start or start_time >= e_end):
                    if teacher_id and item.get('teacher_id') == teacher_id:
                        conflicts.append(f"Teacher Conflict: {item.get('teacher_name')} is already teaching {item.get('subject_name')} in {item.get('class_name')}-{item.get('section')} at {e_start}-{e_end}")
                    if room and item.get('room') == room:
                        conflicts.append(f"Room Conflict: Room {room} is already occupied by {item.get('class_name')}-{item.get('section')} at {e_start}-{e_end}")
        return conflicts
