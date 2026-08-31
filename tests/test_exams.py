from services.exam_service import ExamService

def test_grade_calculation():
    grade, gpa, status = ExamService.calculate_grade_and_gpa(95, 100)
    assert grade == 'A+'
    assert gpa == 4.0
    assert status == 'PASSED'

    g_fail, gpa_fail, status_fail = ExamService.calculate_grade_and_gpa(20, 100)
    assert g_fail == 'F'
    assert status_fail == 'FAILED'
