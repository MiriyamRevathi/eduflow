"""
EduFlow ERP Service — LibraryService
Book catalog, issue/return transactions, and overdue fine calculation.
"""
from typing import Optional, Dict, Any, List, Tuple
from repositories.library_repository import LibraryRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
import datetime

class LibraryService:
    def __init__(self):
        self.library_repo = LibraryRepository()
        self.repo = self.library_repo
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_catalog(self, search_query: str = None, category: str = None) -> List[Dict[str, Any]]:
        return self.library_repo.find_books(search_query, category)

    def add_book(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()
        isbn = data.get('isbn', '').strip()
        if not title or not author:
            return False, "Title and Author are required.", None

        count = self.library_repo.count_books() + 1
        book_data = {
            'id': f"bk-{count:04d}",
            'title': title,
            'author': author,
            'isbn': isbn or f"978-0-{count:05d}-0",
            'category': data.get('category', 'Computer Science'),
            'total_copies': int(data.get('copies', 5)),
            'available_copies': int(data.get('copies', 5)),
            'location_rack': data.get('location_rack', 'A-1')
        }
        created = self.library_repo.add_book(book_data)
        self.audit_repo.log_action(actor_email, actor_role, 'ADD_BOOK', 'LIBRARY', f"Added book {title}")
        return True, "Book added to catalog successfully.", created

    def issue_book(self, book_id: str, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        if not book_id or not student_id:
            return False, "Book and Student are required."
        success, msg = self.library_repo.issue_book(book_id, student_id)
        if success:
            self.audit_repo.log_action(actor_email, actor_role, 'ISSUE_BOOK', 'LIBRARY', f"Issued book {book_id} to student {student_id}")
        return success, msg

    def return_book(self, txn_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        if not txn_id:
            return False, "Transaction ID required."
        success, msg = self.library_repo.return_book(txn_id)
        if success:
            self.audit_repo.log_action(actor_email, actor_role, 'RETURN_BOOK', 'LIBRARY', f"Returned book transaction {txn_id}")
        return success, msg
