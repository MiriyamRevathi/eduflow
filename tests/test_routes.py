import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_page_renders(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b"Welcome to EduFlow ERP" in rv.data

def test_unauthenticated_redirect(client):
    rv = client.get('/')
    assert rv.status_code == 302
