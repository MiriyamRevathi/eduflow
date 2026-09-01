"""
EduFlow ERP Repository — InstitutionRepository
JSON persistence repository for Institutions.
"""
from typing import Dict, Any, List, Optional
from storage.json_storage import JSONStorage
import os

class InstitutionRepository:
    def __init__(self, storage_path: Optional[str] = None):
        if not storage_path:
            storage_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', 'institutions.json')
        self.storage = JSONStorage(storage_path)
        self._ensure_seeded()

    def _ensure_seeded(self):
        data = self.storage.read_all()
        if not data:
            sample_institutions = [
                {
                    'id': 'inst-001',
                    'code': 'GIS-101',
                    'name': 'Greenfield International School',
                    'type': 'School',
                    'email': 'info@greenfield.edu',
                    'phone': '+1 (555) 234-5678',
                    'address': '100 Education Way',
                    'city': 'Boston',
                    'state': 'MA',
                    'country': 'USA',
                    'established_year': 2008,
                    'students_count': 1450,
                    'faculty_count': 92,
                    'attendance_rate': 96.4,
                    'fee_collection': 485000.00,
                    'pending_fees': 24500.00,
                    'status': 'ACTIVE',
                    'admin_name': 'Dr. Arthur Pendelton',
                    'admin_email': 'admin@greenfield.edu',
                    'created_at': '2026-01-15 09:00:00'
                },
                {
                    'id': 'inst-002',
                    'code': 'SXU-202',
                    'name': 'St. Xavier University',
                    'type': 'University',
                    'email': 'contact@stxavier.edu',
                    'phone': '+1 (555) 876-5432',
                    'address': '500 University Ave',
                    'city': 'Chicago',
                    'state': 'IL',
                    'country': 'USA',
                    'established_year': 1995,
                    'students_count': 8420,
                    'faculty_count': 410,
                    'attendance_rate': 93.8,
                    'fee_collection': 3850000.00,
                    'pending_fees': 210000.00,
                    'status': 'ACTIVE',
                    'admin_name': 'Prof. Sarah Jenkins',
                    'admin_email': 's.jenkins@stxavier.edu',
                    'created_at': '2026-01-16 10:30:00'
                },
                {
                    'id': 'inst-003',
                    'code': 'AIT-303',
                    'name': 'Apex Institute of Technology',
                    'type': 'College',
                    'email': 'admissions@apextech.edu',
                    'phone': '+1 (555) 345-6789',
                    'address': '75 Innovation Blvd',
                    'city': 'Austin',
                    'state': 'TX',
                    'country': 'USA',
                    'established_year': 2012,
                    'students_count': 3250,
                    'faculty_count': 185,
                    'attendance_rate': 91.5,
                    'fee_collection': 1420000.00,
                    'pending_fees': 98000.00,
                    'status': 'ACTIVE',
                    'admin_name': 'Dr. Marcus Vance',
                    'admin_email': 'm.vance@apextech.edu',
                    'created_at': '2026-01-20 14:15:00'
                },
                {
                    'id': 'inst-004',
                    'code': 'MSA-404',
                    'name': 'Metro Science Academy',
                    'type': 'School',
                    'email': 'office@metroscience.edu',
                    'phone': '+1 (555) 456-7890',
                    'address': '220 Science Park Rd',
                    'city': 'Seattle',
                    'state': 'WA',
                    'country': 'USA',
                    'established_year': 2018,
                    'students_count': 890,
                    'faculty_count': 58,
                    'attendance_rate': 88.4,
                    'fee_collection': 290000.00,
                    'pending_fees': 45000.00,
                    'status': 'PENDING',
                    'admin_name': 'Elena Rostova',
                    'admin_email': 'e.rostova@metroscience.edu',
                    'created_at': '2026-02-01 11:20:00'
                },
                {
                    'id': 'inst-005',
                    'code': 'HCA-505',
                    'name': 'Horizon College of Arts',
                    'type': 'College',
                    'email': 'admin@horizonarts.edu',
                    'phone': '+1 (555) 567-8901',
                    'address': '410 Creative Lane',
                    'city': 'Denver',
                    'state': 'CO',
                    'country': 'USA',
                    'established_year': 2010,
                    'students_count': 2100,
                    'faculty_count': 115,
                    'attendance_rate': 84.1,
                    'fee_collection': 680000.00,
                    'pending_fees': 142000.00,
                    'status': 'SUSPENDED',
                    'admin_name': 'Julian Thorne',
                    'admin_email': 'j.thorne@horizonarts.edu',
                    'created_at': '2026-02-05 16:45:00'
                },
                {
                    'id': 'inst-006',
                    'code': 'PIM-606',
                    'name': 'Pacific Institute of Management',
                    'type': 'Institute',
                    'email': 'contact@pacificmgmt.edu',
                    'phone': '+1 (555) 678-9012',
                    'address': '800 Bay Street',
                    'city': 'San Francisco',
                    'state': 'CA',
                    'country': 'USA',
                    'established_year': 2005,
                    'students_count': 1850,
                    'faculty_count': 98,
                    'attendance_rate': 94.7,
                    'fee_collection': 920000.00,
                    'pending_fees': 38000.00,
                    'status': 'ACTIVE',
                    'admin_name': 'Dr. Robert Sterling',
                    'admin_email': 'r.sterling@pacificmgmt.edu',
                    'created_at': '2026-02-10 08:30:00'
                },
                {
                    'id': 'inst-007',
                    'code': 'RAH-707',
                    'name': 'Royal Academy High',
                    'type': 'School',
                    'email': 'admissions@royalacademy.edu',
                    'phone': '+1 (555) 789-0123',
                    'address': '330 Crestview Dr',
                    'city': 'Atlanta',
                    'state': 'GA',
                    'country': 'USA',
                    'established_year': 2015,
                    'students_count': 1120,
                    'faculty_count': 74,
                    'attendance_rate': 95.2,
                    'fee_collection': 410000.00,
                    'pending_fees': 18500.00,
                    'status': 'ACTIVE',
                    'admin_name': 'Victoria Sterling',
                    'admin_email': 'v.sterling@royalacademy.edu',
                    'created_at': '2026-02-14 13:10:00'
                },
                {
                    'id': 'inst-008',
                    'code': 'TGU-808',
                    'name': 'Trinity Global University',
                    'type': 'University',
                    'email': 'info@trinityglobal.edu',
                    'phone': '+1 (555) 890-1234',
                    'address': '1000 Metropolitan Plaza',
                    'city': 'New York',
                    'state': 'NY',
                    'country': 'USA',
                    'established_year': 1988,
                    'students_count': 12400,
                    'faculty_count': 650,
                    'attendance_rate': 92.9,
                    'fee_collection': 5200000.00,
                    'pending_fees': 310000.00,
                    'status': 'ACTIVE',
                    'admin_name': 'Prof. David Kingsley',
                    'admin_email': 'd.kingsley@trinityglobal.edu',
                    'created_at': '2026-02-18 15:00:00'
                }
            ]
            self.storage.write_all(sample_institutions)

    def find_all(self) -> List[Dict[str, Any]]:
        return self.storage.read_all()

    def find_by_id(self, item_id: str) -> Optional[Dict[str, Any]]:
        for inst in self.storage.read_all():
            if inst.get('id') == item_id:
                return inst
        return None

    def find_by_status(self, status: str) -> List[Dict[str, Any]]:
        return [inst for inst in self.storage.read_all() if inst.get('status') == status]

    def count(self) -> int:
        return len(self.storage.read_all())

    def create(self, data: Dict[str, Any]) -> Dict[str, Any]:
        records = self.storage.read_all()
        records.append(data)
        self.storage.write_all(records)
        return data

    def update(self, item_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        records = self.storage.read_all()
        for idx, inst in enumerate(records):
            if inst.get('id') == item_id:
                records[idx].update(updates)
                self.storage.write_all(records)
                return records[idx]
        return None

    def delete(self, item_id: str) -> bool:
        records = self.storage.read_all()
        filtered = [inst for inst in records if inst.get('id') != item_id]
        if len(filtered) < len(records):
            self.storage.write_all(filtered)
            return True
        return False
