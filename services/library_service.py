from typing import Optional, Dict, Any, List, Tuple
from repositories.book_repository import BookRepository
from repositories.library_repository import LibraryRepository
from repositories.student_repository import StudentRepository
from repositories.audit_repository import AuditRepository
from utils.datetime_utils import DateTimeUtils
import uuid
import datetime

class LibraryService:
    def __init__(self):
        self.book_repo = BookRepository()
        self.library_repo = LibraryRepository()
        self.student_repo = StudentRepository()
        self.audit_repo = AuditRepository()

    def get_catalog(self, search_query: str = None, category: str = None) -> List[Dict[str, Any]]:
        if search_query:
            return self.book_repo.search(search_query, ['title', 'author', 'isbn', 'category'])
        if category:
            return self.book_repo.find_by_field('category', category)
        return self.book_repo.find_all()

    def add_book(self, data: Dict[str, Any], actor_email: str, actor_role: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        title = data.get('title', '').strip()
        author = data.get('author', '').strip()

        if not title or not author:
            return False, "Book Title and Author are required.", None

        book_count = self.book_repo.count() + 1
        book_data = {
            'id': f"bk-{book_count:04d}",
            'isbn': data.get('isbn', f"978-013{book_count:06d}"),
            'title': title,
            'author': author,
            'category': data.get('category', 'General'),
            'total_copies': int(data.get('total_copies', 5)),
            'available_copies': int(data.get('total_copies', 5)),
            'rack_number': data.get('rack_number', 'CS-01')
        }

        created = self.book_repo.create(book_data)
        self.audit_repo.log_action(actor_email, actor_role, 'ADD_BOOK', 'LIBRARY', f"Added book {title} to library catalog")
        return True, f"Book {title} added to catalog.", created

    def issue_book(self, book_id: str, student_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        book = self.book_repo.find_by_id(book_id)
        if not book:
            return False, "Book not found."

        avail = int(book.get('available_copies', 0))
        if avail <= 0:
            return False, "No copies available for issue."

        student = self.student_repo.find_by_id(student_id)
        if not student:
            return False, "Student record not found."

        today = datetime.date.today()
        due_date = today + datetime.timedelta(days=14)

        txn = {
            'id': str(uuid.uuid4()),
            'book_id': book_id,
            'book_title': book.get('title'),
            'student_id': student_id,
            'issue_date': today.isoformat(),
            'due_date': due_date.isoformat(),
            'return_date': None,
            'status': 'ISSUED',
            'fine_amount': 0.0
        }

        self.library_repo.create(txn)
        self.book_repo.update(book_id, {'available_copies': avail - 1})
        self.audit_repo.log_action(actor_email, actor_role, 'ISSUE_BOOK', 'LIBRARY', f"Issued '{book['title']}' to student {student['full_name']}")
        return True, f"Book '{book['title']}' issued to {student['full_name']} (Due: {due_date.isoformat()})."

    def return_book(self, txn_id: str, actor_email: str, actor_role: str) -> Tuple[bool, str]:
        txn = self.library_repo.find_by_id(txn_id)
        if not txn:
            return False, "Transaction record not found."

        if txn.get('status') == 'RETURNED':
            return False, "Book has already been returned."

        today = datetime.date.today()
        today_str = today.isoformat()
        due_str = txn.get('due_date')

        fine = 0.0
        if due_str:
            due_dt = datetime.datetime.strptime(due_str, '%Y-%m-%d').date()
            if today > due_dt:
                overdue_days = (today - due_dt).days
                fine = float(overdue_days * 2.0)  # $2 per overdue day

        self.library_repo.update(txn_id, {
            'return_date': today_str,
            'status': 'RETURNED',
            'fine_amount': fine
        })

        # Replenish copy
        book = self.book_repo.find_by_id(txn.get('book_id'))
        if book:
            curr_avail = int(book.get('available_copies', 0))
            self.book_repo.update(book['id'], {'available_copies': curr_avail + 1})

        self.audit_repo.log_action(actor_email, actor_role, 'RETURN_BOOK', 'LIBRARY', f"Returned book '{txn.get('book_title')}' with fine ${fine:.2f}")
        return True, f"Book returned successfully. Overdue fine assessed: ${fine:.2f}."
