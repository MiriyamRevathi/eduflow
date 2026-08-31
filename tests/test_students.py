from services.student_service import StudentService

def test_student_pagination_and_query():
    svc = StudentService()
    res = svc.get_paginated_students(page=1, per_page=10)
    assert 'items' in res
    assert 'total' in res
    assert res['total'] >= 0

def test_student_full_profile():
    svc = StudentService()
    # Check seed student
    student = svc.get_student_full_profile('std-001')
    assert student is not None
    assert student['student_id'] == 'STU-2026-0001'
