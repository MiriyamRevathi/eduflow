from typing import List, Dict, Any
from repositories.institution_repository import InstitutionRepository
from repositories.student_repository import StudentRepository
from repositories.teacher_repository import TeacherRepository
from repositories.user_repository import UserRepository
from repositories.course_repository import CourseRepository
from repositories.book_repository import BookRepository

class SearchService:
    def __init__(self):
        self.inst_repo = InstitutionRepository()
        self.student_repo = StudentRepository()
        self.teacher_repo = TeacherRepository()
        self.user_repo = UserRepository()
        self.course_repo = CourseRepository()
        self.book_repo = BookRepository()

    def global_search(self, query: str) -> List[Dict[str, Any]]:
        if not query or len(query.strip()) < 2:
            return []

        q = query.strip().lower()
        results = []

        # 1. Search Institutions (Top priority for Super Admin)
        institutions = self.inst_repo.find_all()
        matching_insts = [i for i in institutions if q in i.get('name', '').lower() or q in i.get('code', '').lower() or q in i.get('city', '').lower()]
        for inst in matching_insts[:5]:
            results.append({
                'category': 'Institutions',
                'title': f"🏛️ {inst['name']} ({inst['code']})",
                'subtitle': f"Type: {inst['type']} | City: {inst['city']}, {inst['state']} | Status: {inst['status']}",
                'url': f"/institutions/{inst['id']}"
            })

        # 2. Search Students
        students = self.student_repo.search(q, ['full_name', 'student_id', 'email', 'class_name'])
        for s in students[:5]:
            results.append({
                'category': 'Students',
                'title': f"👨‍🎓 {s['full_name']} ({s['student_id']})",
                'subtitle': f"Class {s['class_name']}-{s['section']} | {s['email']}",
                'url': f"/students/{s['id']}"
            })

        # 3. Search Faculty
        teachers = self.teacher_repo.search(q, ['full_name', 'faculty_id', 'email', 'department'])
        for t in teachers[:5]:
            results.append({
                'category': 'Faculty',
                'title': f"👩‍🏫 {t['full_name']} ({t['faculty_id']})",
                'subtitle': f"{t['designation']} - {t['department']}",
                'url': f"/faculty/{t['id']}"
            })

        # 4. Search System Users
        users = self.user_repo.find_all()
        matching_users = [u for u in users if q in u.get('full_name', '').lower() or q in u.get('email', '').lower() or q in u.get('role', '').lower()]
        for u in matching_users[:5]:
            results.append({
                'category': 'Users & Roles',
                'title': f"👤 {u['full_name']} ({u['role']})",
                'subtitle': f"Email: {u['email']} | Status: {u.get('status', 'ACTIVE')}",
                'url': "/users"
            })

        # 5. Search Courses
        courses = self.course_repo.search(q, ['name', 'code', 'department'])
        for c in courses[:5]:
            results.append({
                'category': 'Courses',
                'title': f"📚 {c['name']} ({c['code']})",
                'subtitle': f"Department: {c['department']}",
                'url': "/academics"
            })

        # 6. Reports & Analytics matches
        if 'report' in q or 'student' in q or 'fee' in q or 'attendance' in q:
            results.append({
                'category': 'Reports',
                'title': "📊 Executive Reports & Data Center",
                'subtitle': "Nationwide attendance, tuition fee, and student roster exports",
                'url': "/reports"
            })

        return results
