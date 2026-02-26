import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)

def test_signup_and_delete():
    activity = "Chess Club"
    email = "testuser@mergington.edu"

    # Ensure test email is not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # Signup
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert email in activities[activity]["participants"]
    assert resp.json()["message"].startswith("Signed up")

    # Duplicate signup should fail
    resp_dup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp_dup.status_code == 400
    assert "already signed up" in resp_dup.json()["detail"]

    # Delete
    resp_del = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp_del.status_code == 200
    assert email not in activities[activity]["participants"]
    assert resp_del.json()["message"].startswith("Unregistered")

    # Deleting again should fail
    resp_del2 = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp_del2.status_code == 404
    assert "not signed up" in resp_del2.json()["detail"]
