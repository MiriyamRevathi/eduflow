from flask import Blueprint, render_template, request, jsonify
from ml.prediction import StudentRiskPredictor
from repositories.student_repository import StudentRepository
from security.rbac import login_required

ml_bp = Blueprint('ml', __name__, url_prefix='/ml')
predictor = StudentRiskPredictor()
student_repo = StudentRepository()

@ml_bp.route('/')
@login_required
def index():
    students = student_repo.find_all()
    risk_predictions = []

    for std in students:
        res = predictor.predict_student_risk(std['id'])
        risk_predictions.append({
            'student': std,
            'risk_category': res['risk_category'],
            'risk_score': res['risk_score'],
            'recommendations': res['recommendations'],
            'features': res['features']
        })

    return render_template('ml/index.html', predictions=risk_predictions)

@ml_bp.route('/predict/<student_id>')
@login_required
def predict(student_id):
    res = predictor.predict_student_risk(student_id)
    return jsonify(res)
