import pytest
from app import create_app
from security.password import PasswordSecurity
from services.auth_service import AuthService

def test_password_hashing():
    plain = "secret123"
    hashed = PasswordSecurity.hash_password(plain)
    assert hashed != plain
    assert PasswordSecurity.verify_password(plain, hashed) is True
    assert PasswordSecurity.verify_password("wrong", hashed) is False

def test_auth_service_login():
    app = create_app()
    with app.test_request_context():
        auth_service = AuthService()
        success, msg, user = auth_service.authenticate("admin@eduflow.local", "admin123")
        assert success is True
        assert user['email'] == "admin@eduflow.local"

        success_bad, msg_bad, _ = auth_service.authenticate("admin@eduflow.local", "wrongpassword")
        assert success_bad is False
