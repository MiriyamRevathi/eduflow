from flask import session
from typing import Optional, Dict, Any

class SessionManager:
    SESSION_USER_KEY = 'user_id'
    SESSION_ROLE_KEY = 'user_role'
    SESSION_NAME_KEY = 'user_name'
    SESSION_EMAIL_KEY = 'user_email'

    @staticmethod
    def login_user(user: Dict[str, Any]):
        session.clear()
        session[SessionManager.SESSION_USER_KEY] = str(user.get('id'))
        session[SessionManager.SESSION_ROLE_KEY] = user.get('role')
        session[SessionManager.SESSION_NAME_KEY] = user.get('full_name')
        session[SessionManager.SESSION_EMAIL_KEY] = user.get('email')
        session.permanent = True

    @staticmethod
    def logout_user():
        session.clear()

    @staticmethod
    def get_current_user_id() -> Optional[str]:
        return session.get(SessionManager.SESSION_USER_KEY)

    @staticmethod
    def get_current_role() -> Optional[str]:
        return session.get(SessionManager.SESSION_ROLE_KEY)

    @staticmethod
    def get_current_user_email() -> Optional[str]:
        return session.get(SessionManager.SESSION_EMAIL_KEY)

    @staticmethod
    def is_authenticated() -> bool:
        return SessionManager.SESSION_USER_KEY in session
