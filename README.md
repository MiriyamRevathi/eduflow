# EduFlow ERP — School & College Management System

EduFlow ERP is a full-stack, enterprise-grade School & College Management System built with Python, Flask, Jinja2, Vanilla JavaScript, CSS3, local file-based JSON persistence, and local `scikit-learn` machine learning risk analytics.

---

## 🌟 Key Features

- **Full Functionality & Zero Dead Buttons**: Every action link, modal, search input, status filter, export button, and tab switch is connected to real backend routes and JSON storage.
- **12 User Roles & RBAC**: Support for Super Admin, School Admin, College Admin, Principal, Teacher, Faculty, Student, Parent, Accountant, Librarian, Transport Manager, and Hostel Warden.
- **Student & Faculty Portals**: Comprehensive student directory with multi-tab academic profiles, faculty workloads, and department tracking.
- **Admissions Workflow**: Full application lifecycle (`APPLIED` → `UNDER_REVIEW` → `APPROVED` → `REJECTED` → `WAITLISTED` → `ENROLLED`) with automated student provisioning.
- **Attendance Engine**: Daily and bulk classroom attendance marking with automated attendance percentage calculation.
- **Academics & Timetable**: Course catalog, subject credits, and interactive weekly timetable grid with real-time teacher/room conflict detection.
- **Examinations & GPA Engine**: Exam scheduling, marks entry, and GPA/grade calculation (A+, A, B, C, D, F, 0–4.0 scale).
- **Fees & Payment Simulation**: Fee structure creation, invoice generation, partial payment tracking, and Cash/Card/UPI payment simulation with printable PDF receipts.
- **Library Circulation**: Catalog management, book issue/return tracking, and automated overdue fine calculation ($2/day).
- **Hostel & Transport**: Hostel building/room/bed allocation and transport route assignment with vehicle capacity check.
- **Leave & Events**: Multi-role leave application & approval pipeline, interactive events calendar, and targeted announcements.
- **Local Machine Learning**: Scikit-Learn Random Forest student academic-risk prediction classifier (`LOW RISK`, `MEDIUM RISK`, `HIGH RISK`) with actionable AI recommendations.
- **Reports & Global Search**: CSV export for all datasets, global keyboard-shortcut search (`Ctrl+K`), system audit trail logs, and notification center.
- **Modern UI/UX**: Dark/Light theme toggle (persisted locally), responsive sidebar, toast alerts, data tables, and custom Canvas charts.

---

## 🔑 Demo Accounts

All accounts use their respective role email and default passwords:

| Role | Email | Default Password |
| :--- | :--- | :--- |
| **Super Admin** | `admin@eduflow.local` | `admin123` |
| **School Admin** | `schooladmin@eduflow.local` | `admin123` |
| **College Admin** | `collegeadmin@eduflow.local` | `admin123` |
| **Principal** | `principal@eduflow.local` | `principal123` |
| **Teacher / Faculty**| `teacher@eduflow.local` | `teacher123` |
| **Student** | `student@eduflow.local` | `student123` |
| **Parent** | `parent@eduflow.local` | `parent123` |
| **Accountant** | `accountant@eduflow.local` | `accountant123` |
| **Librarian** | `librarian@eduflow.local` | `librarian123` |
| **Transport Manager**| `transport@eduflow.local` | `transport123` |
| **Hostel Warden** | `warden@eduflow.local` | `warden123` |

---

## 🚀 Quick Start Guide

### 1. Installation
```bash
# Clone or navigate to the eduflow directory
cd eduflow

# Install locked dependencies
pip install -r requirements.lock
```

### 2. Run the Application
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## 🧪 Testing

Run the full `pytest` test suite:
```bash
pytest -v
```

---

## 🐳 Docker Deployment

Build and run using Docker:
```bash
docker build -t eduflow-erp .
docker run -p 5000:5000 eduflow-erp
```
