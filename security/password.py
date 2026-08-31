from werkzeug.security import generate_password_hash, check_password_hash

class PasswordSecurity:
    @staticmethod
    def hash_password(plain_password: str) -> str:
        return generate_password_hash(plain_password, method='pbkdf2:sha256')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        if not plain_password or not hashed_password:
            return False
        return check_password_hash(hashed_password, plain_password)
