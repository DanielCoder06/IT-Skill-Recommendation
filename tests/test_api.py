from fastapi.testclient import TestClient

from src.api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data == {
        "message": "IT Skill Recommendation API is running."
    }


def test_get_recommendations():
    response = client.get(
        "/recommendations/1?top_n=3"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["cv_id"] == 1
    assert data["count"] == 3
    assert len(data["recommendations"]) == 3

    recommendation = data["recommendations"][0]

    assert "job_id" in recommendation
    assert "job_title" in recommendation
    assert "match_rate" in recommendation
    assert "matched_skills" in recommendation
    assert "missing_skills" in recommendation
    assert "extra_skills" in recommendation
    assert "skill_recommendations" in recommendation
    assert "learning_roadmap" in recommendation
    assert "evaluation" in recommendation


def test_get_recommendations_respects_top_n():
    response = client.get(
        "/recommendations/1?top_n=2"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["count"] == 2
    assert len(data["recommendations"]) == 2


def test_get_recommendations_invalid_top_n():
    response = client.get(
        "/recommendations/1?top_n=0"
    )

    assert response.status_code == 422


def test_get_recommendations_invalid_cv():
    response = client.get(
        "/recommendations/999999"
    )

    assert response.status_code == 404

    data = response.json()

    assert "detail" in data