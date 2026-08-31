from typing import Optional, Dict, Any, Tuple
from repositories.user_repository import UserRepository
from security.password import PasswordSecurity
from security.session import SessionManager
from repositories.audit_repository import AuditRepository

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()
        self.audit_repo = AuditRepository()

    def authenticate(self, email: str, plain_password: str) -> Tuple[bool, str, Optional[Dict[str, Any]]]:
        if not email or not plain_password:
            return False, "Email and password are required.", None

        user = self.user_repo.find_by_email(email)
        if not user:
            return False, "Invalid email or password.", None

        if user.get('status') != 'ACTIVE':
            return False, "Your account has been deactivated. Please contact administration.", None

        if not PasswordSecurity.verify_password(plain_password, user.get('password')):
            return False, "Invalid email or password.", None

        SessionManager.login_user(user)
        self.audit_repo.log_action(user['email'], user['role'], 'USER_LOGIN', 'AUTH', 'User logged in successfully.')
        return True, "Login successful.", user

    def logout(self):
        email = SessionManager.get_current_user_email()
        role = SessionManager.get_current_role()
        if email:
            self.audit_repo.log_action(email, role or 'UNKNOWN', 'USER_LOGOUT', 'AUTH', 'User logged out.')
        SessionManager.logout_user()

    def change_password(self, user_id: str, old_password: str, new_password: str) -> Tuple[bool, str]:
        user = self.user_repo.find_by_id(user_id)
        if not user:
            return False, "User not found."

        if not PasswordSecurity.verify_password(old_password, user.get('password')):
            return False, "Incorrect current password."

        if len(new_password) < 6:
            return False, "New password must be at least 6 characters long."

        hashed_pwd = PasswordSecurity.hash_password(new_password)
        self.user_repo.update(user_id, {'password': hashed_pwd})
        self.audit_repo.log_action(user['email'], user['role'], 'PASSWORD_CHANGE', 'USER', 'Password updated successfully.')
        return True, "Password changed successfully."
