from src.app import activities


def test_get_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert data["Chess Club"]["description"] == "Learn strategies and compete in chess tournaments"


def test_signup_for_activity(client):
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"

    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email in activities[activity_name]["participants"]


def test_duplicate_signup_returns_400(client):
    activity_name = "Chess Club"
    email = "duplicate@mergington.edu"

    first_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert first_response.status_code == 200

    second_response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student is already signed up for this activity"


def test_remove_participant(client):
    activity_name = "Chess Club"
    email = "michael@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    activity_name = "Chess Club"
    email = "missing@mergington.edu"

    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
