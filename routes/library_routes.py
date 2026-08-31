from flask import Blueprint, render_template, request, redirect, url_for, flash
from services.library_service import LibraryService
from repositories.student_repository import StudentRepository
from security.rbac import login_required, admin_required
from security.session import SessionManager

library_bp = Blueprint('library', __name__, url_prefix='/library')
library_service = LibraryService()
student_repo = StudentRepository()

@library_bp.route('/')
@login_required
def index():
    search_q = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    books = library_service.get_catalog(search_q, category)
    students = student_repo.find_all()
    return render_template('library/index.html', books=books, students=students, search_q=search_q, category=category)

@library_bp.route('/books/new', methods=['GET', 'POST'])
@login_required
@admin_required
def new_book():
    if request.method == 'POST':
        actor_email = SessionManager.get_current_user_email()
        actor_role = SessionManager.get_current_role()

        data = {
            'title': request.form.get('title'),
            'author': request.form.get('author'),
            'isbn': request.form.get('isbn'),
            'category': request.form.get('category'),
            'total_copies': request.form.get('total_copies'),
            'rack_number': request.form.get('rack_number')
        }

        success, msg, created = library_service.add_book(data, actor_email, actor_role)
        if success:
            flash(msg, 'success')
            return redirect(url_for('library.index'))
        else:
            flash(msg, 'danger')

    return render_template('library/book_form.html')

@library_bp.route('/issue', methods=['POST'])
@login_required
def issue_book():
    book_id = request.form.get('book_id')
    student_id = request.form.get('student_id')
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = library_service.issue_book(book_id, student_id, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('library.transactions'))

@library_bp.route('/transactions')
@login_required
def transactions():
    all_txns = library_service.library_repo.find_all()
    for t in all_txns:
        std = student_repo.find_by_id(t.get('student_id'))
        t['student_name'] = std.get('full_name') if std else 'N/A'
    return render_template('library/transactions.html', transactions=all_txns)

@library_bp.route('/<txn_id>/return', methods=['POST'])
@login_required
def return_book(txn_id):
    actor_email = SessionManager.get_current_user_email()
    actor_role = SessionManager.get_current_role()

    success, msg = library_service.return_book(txn_id, actor_email, actor_role)
    if success:
        flash(msg, 'success')
    else:
        flash(msg, 'danger')

    return redirect(url_for('library.transactions'))
