from fastapi.testclient import TestClient

from main import app
from dependencies.current_user import get_current_user


def fake_current_user():
    return {
        "id": 999,
        "user_name": "test_user",
        "role": "User",
        "status": "Active"
    }


app.dependency_overrides[get_current_user] = fake_current_user

client = TestClient(app)


def test_profile():

    response = client.get("/profile/current_user")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == 999
    assert data["user_name"] == "test_user"
    assert data["role"] == "User"

    app.dependency_overrides={}