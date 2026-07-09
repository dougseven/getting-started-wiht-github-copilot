import pytest
from fastapi import HTTPException

from src.app import (
    activities,
    get_activities,
    root,
    signup_for_activity,
    unregister_from_activity,
)


def test_get_activities_returns_current_map():
    # Arrange

    # Act
    result = get_activities()

    # Assert
    assert result is activities
    assert "Chess Club" in result


def test_root_returns_redirect_response():
    # Arrange

    # Act
    response = root()

    # Assert
    assert response.status_code in (302, 307)
    assert response.headers["location"] == "/static/index.html"


def test_signup_for_activity_success_adds_participant():
    # Arrange
    activity_name = "Programming Class"
    email = "unit.new.student@mergington.edu"
    before_count = len(activities[activity_name]["participants"])

    # Act
    result = signup_for_activity(activity_name, email)

    # Assert
    assert result["message"] == f"Signed up {email} for {activity_name}"
    assert len(activities[activity_name]["participants"]) == before_count + 1
    assert email in activities[activity_name]["participants"]


def test_signup_for_activity_duplicate_raises_http_400():
    # Arrange
    activity_name = "Programming Class"
    email = "emma@mergington.edu"

    # Act
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity(activity_name, email)

    # Assert
    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Student already signed up for this activity"


def test_signup_for_activity_unknown_activity_raises_http_404():
    # Arrange
    activity_name = "Unknown Club"
    email = "unit.student@mergington.edu"

    # Act
    with pytest.raises(HTTPException) as exc_info:
        signup_for_activity(activity_name, email)

    # Assert
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"


def test_unregister_from_activity_success_removes_participant():
    # Arrange
    activity_name = "Drama Club"
    email = "ava@mergington.edu"

    # Act
    result = unregister_from_activity(activity_name, email)

    # Assert
    assert result["message"] == f"Unregistered {email} from {activity_name}"
    assert email not in activities[activity_name]["participants"]


def test_unregister_from_activity_not_signed_up_raises_http_404():
    # Arrange
    activity_name = "Drama Club"
    email = "not.enrolled@mergington.edu"

    # Act
    with pytest.raises(HTTPException) as exc_info:
        unregister_from_activity(activity_name, email)

    # Assert
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Student is not signed up for this activity"


def test_unregister_from_activity_unknown_activity_raises_http_404():
    # Arrange
    activity_name = "Unknown Club"
    email = "unit.student@mergington.edu"

    # Act
    with pytest.raises(HTTPException) as exc_info:
        unregister_from_activity(activity_name, email)

    # Assert
    assert exc_info.value.status_code == 404
    assert exc_info.value.detail == "Activity not found"
