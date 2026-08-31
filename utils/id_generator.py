import uuid
import datetime

class IDGenerator:
    @staticmethod
    def generate_uuid() -> str:
        return str(uuid.uuid4())

    @staticmethod
    def generate_custom_id(prefix: str, number: int, width: int = 4) -> str:
        year = datetime.datetime.now().year
        return f"{prefix}-{year}-{str(number).zfill(width)}"

    @staticmethod
    def generate_student_id(number: int) -> str:
        return IDGenerator.generate_custom_id("STU", number, 4)

    @staticmethod
    def generate_faculty_id(number: int) -> str:
        return IDGenerator.generate_custom_id("FAC", number, 4)

    @staticmethod
    def generate_fee_id(number: int) -> str:
        return IDGenerator.generate_custom_id("FEE", number, 4)

    @staticmethod
    def generate_payment_id(number: int) -> str:
        return IDGenerator.generate_custom_id("PAY", number, 5)

    @staticmethod
    def generate_admission_id(number: int) -> str:
        return IDGenerator.generate_custom_id("ADM", number, 4)

    @staticmethod
    def generate_exam_id(number: int) -> str:
        return IDGenerator.generate_custom_id("EXM", number, 4)
