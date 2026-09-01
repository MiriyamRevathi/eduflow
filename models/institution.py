"""
EduFlow ERP Domain Model — InstitutionModel
"""
from typing import Dict, Any, Optional

class InstitutionModel:
    def __init__(
        self,
        id: str,
        code: str,
        name: str,
        type: str,
        email: str,
        phone: str,
        address: str = "",
        city: str = "",
        state: str = "",
        country: str = "USA",
        established_year: int = 2005,
        students_count: int = 0,
        faculty_count: int = 0,
        attendance_rate: float = 95.0,
        fee_collection: float = 0.0,
        pending_fees: float = 0.0,
        status: str = "ACTIVE",
        admin_name: str = "Dr. Admin",
        admin_email: str = "admin@institution.edu",
        created_at: str = ""
    ):
        self.id = id
        self.code = code
        self.name = name
        self.type = type
        self.email = email
        self.phone = phone
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.established_year = established_year
        self.students_count = students_count
        self.faculty_count = faculty_count
        self.attendance_rate = attendance_rate
        self.fee_collection = fee_collection
        self.pending_fees = pending_fees
        self.status = status
        self.admin_name = admin_name
        self.admin_email = admin_email
        self.created_at = created_at

    def to_dict(self) -> Dict[str, Any]:
        return self.__dict__
