from ml.prediction import StudentRiskPredictor

def test_ml_risk_prediction():
    predictor = StudentRiskPredictor()
    res = predictor.predict_student_risk('std-001')
    assert 'risk_category' in res
    assert 'risk_score' in res
    assert 'recommendations' in res
    assert res['risk_category'] in ['LOW RISK', 'MEDIUM RISK', 'HIGH RISK']
