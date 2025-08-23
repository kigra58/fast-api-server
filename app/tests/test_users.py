import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.session import Base, get_db
from app.main import app
from app.services import user as user_service


# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Setup test database
@pytest.fixture(scope="function")
def db():
    # Create the database and tables
    Base.metadata.create_all(bind=engine)
    
    # Create a connection and session
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    # Begin a nested transaction
    nested = connection.begin_nested()
    
    # Override the get_db dependency
    def override_get_db():
        try:
            yield session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    yield session
    
    # Rollback the transaction
    session.close()
    transaction.rollback()
    connection.close()


# Test client
@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c


# Create a test superuser
@pytest.fixture(scope="function")
def superuser(db):
    user_in = {
        "email": "admin@example.com",
        "username": "admin",
        "password": "admin123",
        "is_superuser": True,
    }
    user = user_service.create(db, obj_in=user_in)
    return user


# Create a test normal user
@pytest.fixture(scope="function")
def normal_user(db):
    user_in = {
        "email": "user@example.com",
        "username": "normaluser",
        "password": "user123",
        "is_superuser": False,
    }
    user = user_service.create(db, obj_in=user_in)
    return user


# Test authentication
def test_login(client, normal_user):
    response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "normaluser", "password": "user123"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


# Test user creation
def test_create_user(client, superuser, db):
    # Login as superuser
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "admin", "password": "admin123"},
    )
    token = login_response.json()["access_token"]
    
    # Create a new user
    new_user = {
        "email": "newuser@example.com",
        "username": "newuser",
        "password": "newpass123",
        "first_name": "New",
        "last_name": "User",
    }
    
    response = client.post(
        f"{settings.API_V1_STR}/users/",
        json=new_user,
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == new_user["email"]
    assert data["username"] == new_user["username"]
    assert "password" not in data
    assert data["first_name"] == new_user["first_name"]
    assert data["last_name"] == new_user["last_name"]


# Test get current user
def test_get_current_user(client, normal_user):
    # Login
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "normaluser", "password": "user123"},
    )
    token = login_response.json()["access_token"]
    
    # Get current user
    response = client.get(
        f"{settings.API_V1_STR}/users/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == normal_user.email
    assert data["username"] == normal_user.username


# Test update user
def test_update_user(client, normal_user):
    # Login
    login_response = client.post(
        f"{settings.API_V1_STR}/auth/login",
        data={"username": "normaluser", "password": "user123"},
    )
    token = login_response.json()["access_token"]
    
    # Update user
    update_data = {
        "first_name": "Updated",
        "last_name": "User",
    }
    
    response = client.put(
        f"{settings.API_V1_STR}/users/me",
        json=update_data,
        headers={"Authorization": f"Bearer {token}"},
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
