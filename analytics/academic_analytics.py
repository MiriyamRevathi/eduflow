"""
EduFlow ERP Academic Performance Analytics
Computes course GPAs, subject pass rates, and grade distributions.
"""
from typing import Dict, Any, List
from repositories.marks_repository import MarksRepository
from repositories.course_repository import CourseRepository
from repositories.subject_repository import SubjectRepository

class AcademicAnalytics:
    def __init__(self):
        self.marks_repo = MarksRepository()
        self.course_repo = CourseRepository()
        self.subject_repo = SubjectRepository()

    def get_course_performance_breakdown(self, course_id: str) -> Dict[str, Any]:
        subjects = self.subject_repo.find_by_course(course_id)
        subject_stats = []
        for s in subjects:
            marks = self.marks_repo.find_by_field('subject_id', s['id'])
            if marks:
                avg_obtained = sum(m.get('marks_obtained', 0) for m in marks) / len(marks)
                pass_cnt = sum(1 for m in marks if m.get('status') == 'PASSED')
                pass_rate = round((pass_cnt / len(marks) * 100.0), 1)
            else:
                avg_obtained = 0.0
                pass_rate = 100.0

            subject_stats.append({
                'subject_id': s['id'],
                'subject_name': s['name'],
                'avg_marks': round(avg_obtained, 2),
                'pass_rate_pct': pass_rate
            })

        return {
            'course_id': course_id,
            'subject_stats': subject_stats
        }
