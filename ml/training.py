import os
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from ml.dataset_builder import DatasetBuilder
from config import Config

class RiskModelTrainer:
    def __init__(self):
        self.model_path = os.path.join(Config.MODEL_DIR, 'student_risk_rf.joblib')
        self.scaler_path = os.path.join(Config.MODEL_DIR, 'scaler.joblib')

    def train_and_save(self) -> bool:
        try:
            builder = DatasetBuilder()
            X, y = builder.build_synthetic_dataset()

            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)

            clf = RandomForestClassifier(n_estimators=50, random_state=42, max_depth=6)
            clf.fit(X_scaled, y)

            joblib.dump(clf, self.model_path)
            joblib.dump(scaler, self.scaler_path)

            print("Scikit-learn student risk model trained and saved successfully.")
            return True
        except Exception as e:
            print(f"Error training ML model: {e}")
            return False
