from services.attendance_service import AttendanceService

def test_attendance_overview():
    svc = AttendanceService()
    overview = svc.get_attendance_overview(date_str='2026-08-25', class_name='CS-101', section='A')
    assert 'stats' in overview
    assert 'students' in overview
