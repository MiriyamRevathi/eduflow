from services.fee_service import FeeService

def test_fee_service_payment():
    svc = FeeService()
    fees = svc.get_all_fees()
    assert len(fees) > 0
