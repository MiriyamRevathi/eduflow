import numpy as np
from typing import List, Dict, Any, Tuple
from repositories.student_repository import StudentRepository
from repositories.attendance_repository import AttendanceRepository
from repositories.marks_repository import MarksRepository
from repositories.assignment_repository import AssignmentRepository
from repositories.leave_repository import LeaveRepository
from repositories.fee_repository import FeeRepository

class DatasetBuilder:
    def __init__(self):
        self.student_repo = StudentRepository()
        self.attendance_repo = AttendanceRepository()
        self.marks_repo = MarksRepository()
        self.assignment_repo = AssignmentRepository()
        self.leave_repo = LeaveRepository()
        self.fee_repo = FeeRepository()

    def extract_student_features(self, student_id: str) -> Dict[str, float]:
        # Feature 1: Attendance Percentage
        att_pct = self.attendance_repo.get_attendance_percentage(student_id)

        # Feature 2: Marks Average %
        marks = self.marks_repo.find_by_student(student_id)
        if marks:
            total_obtained = sum(m.get('marks_obtained', 0) for m in marks)
            total_max = sum(m.get('max_marks', 100) for m in marks)
            marks_pct = (total_obtained / total_max * 100.0) if total_max > 0 else 50.0
        else:
            marks_pct = 70.0

        # Feature 3: Assignment Submission Rate
        all_assignments = self.assignment_repo.find_all()
        submitted_cnt = 0
        for asg in all_assignments:
            subs = asg.get('submissions', [])
            for s in subs:
                if s.get('student_id') == student_id:
                    submitted_cnt += 1
                    break
        asg_pct = (submitted_cnt / len(all_assignments) * 100.0) if all_assignments else 100.0

        # Feature 4: Leave Application Frequency
        leaves = self.leave_repo.find_by_applicant(student_id)
        leave_cnt = float(len(leaves))

        # Feature 5: Pending Fee Ratio
        fees = self.fee_repo.find_by_student(student_id)
        if fees:
            total_net = sum(f.get('net_amount', 0) for f in fees)
            total_pending = sum(f.get('pending_amount', 0) for f in fees)
            fee_ratio = (total_pending / total_net) if total_net > 0 else 0.0
        else:
            fee_ratio = 0.0

        return {
            'attendance_pct': att_pct,
            'marks_pct': marks_pct,
            'assignment_pct': asg_pct,
            'leave_count': leave_cnt,
            'fee_pending_ratio': fee_ratio
        }

    def build_synthetic_dataset(self) -> Tuple[np.ndarray, np.ndarray]:
        # Generate 150 student feature vectors representing diverse performance profiles
        X = []
        y = []
        np.random.seed(42)

        for _ in range(150):
            # Synthetic features: [att_pct, marks_pct, asg_pct, leave_cnt, fee_pending_ratio]
            att = np.random.uniform(40.0, 100.0)
            marks = np.random.uniform(30.0, 98.0)
            asg = np.random.uniform(20.0, 100.0)
            leaves = np.random.poisson(1.5)
            fee_ratio = np.random.uniform(0.0, 1.0)

            # Define ground truth rule-based risk classification label
            risk_score = (100 - att) * 0.35 + (100 - marks) * 0.35 + (100 - asg) * 0.20 + (leaves * 5.0) + (fee_ratio * 15.0)

            if risk_score > 45.0:
                label = 2  # HIGH RISK
            elif risk_score > 25.0:
                label = 1  # MEDIUM RISK
            else:
                label = 0  # LOW RISK

            X.append([att, marks, asg, leaves, fee_ratio])
            y.append(label)

        return np.array(X), np.array(y)
