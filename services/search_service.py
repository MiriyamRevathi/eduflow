from typing import List, Dict, Any
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.course_repository import CourseRepository
from repositories.book_repository import BookRepository
from repositories.exam_repository import ExamRepository
from repositories.event_repository import EventRepository

class SearchService:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.teacher_repo = TeacherRepository()
        self.course_repo = CourseRepository()
        self.book_repo = BookRepository()
        self.exam_repo = ExamRepository()
        self.event_repo = EventRepository()

    def global_search(self, query: str) -> List[Dict[str, Any]]:
        if not query or len(query.strip()) < 2:
            return []

        q = query.strip().lower()
        results = []

        # 1. Search Students
        students = self.student_repo.search(q, ['full_name', 'student_id', 'email', 'class_name'])
        for s in students[:5]:
            results.append({
                'category': 'Students',
                'title': f"{s['full_name']} ({s['student_id']})",
                'subtitle': f"Class {s['class_name']}-{s['section']} | {s['email']}",
                'url': f"/students/{s['id']}"
            })

        # 2. Search Faculty
        teachers = self.teacher_repo.search(q, ['full_name', 'faculty_id', 'email', 'department'])
        for t in teachers[:5]:
            results.append({
                'category': 'Faculty',
                'title': f"{t['full_name']} ({t['faculty_id']})",
                'subtitle': f"{t['designation']} - {t['department']}",
                'url': f"/faculty/{t['id']}"
            })

        # 3. Search Courses
        courses = self.course_repo.search(q, ['name', 'code', 'department'])
        for c in courses[:5]:
            results.append({
                'category': 'Courses',
                'title': f"{c['name']} ({c['code']})",
                'subtitle': f"Department: {c['department']}",
                'url': "/academics"
            })

        # 4. Search Library Books
        books = self.book_repo.search(q, ['title', 'author', 'isbn', 'category'])
        for b in books[:5]:
            results.append({
                'category': 'Library',
                'title': f"{b['title']}",
                'subtitle': f"by {b['author']} | ISBN: {b['isbn']}",
                'url': "/library"
            })

        # 5. Search Exams
        exams = self.exam_repo.search(q, ['title', 'exam_id', 'room'])
        for e in exams[:5]:
            results.append({
                'category': 'Examinations',
                'title': f"{e['title']} ({e['exam_id']})",
                'subtitle': f"Date: {e['exam_date']} | Room: {e['room']}",
                'url': "/exams"
            })

        return results
