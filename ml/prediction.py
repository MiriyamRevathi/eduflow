import os
import joblib
import numpy as np
from typing import Dict, Any
from ml.dataset_builder import DatasetBuilder
from ml.training import RiskModelTrainer
from ml.recommendations import RecommendationEngine
from config import Config

class StudentRiskPredictor:
    def __init__(self):
        self.model_path = os.path.join(Config.MODEL_DIR, 'student_risk_rf.joblib')
        self.scaler_path = os.path.join(Config.MODEL_DIR, 'scaler.joblib')
        self._ensure_model_trained()

    def _ensure_model_trained(self):
        if not os.path.exists(self.model_path) or not os.path.exists(self.scaler_path):
            trainer = RiskModelTrainer()
            trainer.train_and_save()

    def predict_student_risk(self, student_id: str) -> Dict[str, Any]:
        builder = DatasetBuilder()
        feats = builder.extract_student_features(student_id)

        try:
            clf = joblib.load(self.model_path)
            scaler = joblib.load(self.scaler_path)

            X_in = np.array([[
                feats['attendance_pct'],
                feats['marks_pct'],
                feats['assignment_pct'],
                feats['leave_count'],
                feats['fee_pending_ratio']
            ]])

            X_scaled = scaler.transform(X_in)
            probs = clf.predict_proba(X_scaled)[0]
            pred_class = clf.predict(X_scaled)[0]

            labels_map = {0: 'LOW RISK', 1: 'MEDIUM RISK', 2: 'HIGH RISK'}
            risk_label = labels_map.get(pred_class, 'LOW RISK')
            risk_score = round(float(np.max(probs)) * 100.0, 1)

        except Exception as e:
            print(f"Prediction fallback: {e}")
            # Fallback heuristic rule
            att = feats['attendance_pct']
            marks = feats['marks_pct']
            if att < 60 or marks < 40:
                risk_label = 'HIGH RISK'
                risk_score = 85.0
            elif att < 75 or marks < 60:
                risk_label = 'MEDIUM RISK'
                risk_score = 65.0
            else:
                risk_label = 'LOW RISK'
                risk_score = 15.0

        recommendations = RecommendationEngine.generate_recommendations(feats, risk_label)

        return {
            'student_id': student_id,
            'features': feats,
            'risk_category': risk_label,
            'risk_score': risk_score,
            'recommendations': recommendations
        }
