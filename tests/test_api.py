import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database.repository import Repository
from src.database.schema import SchemaManager
from unittest.mock import patch

# Create a test client
client = TestClient(app)


@pytest.fixture(scope="module", autouse=True)
def setup_test_db():
    repo = Repository()
    schema = SchemaManager()
    schema.create_tables()
    yield repo
    repo.db.execute("DROP TABLE IF EXISTS executive_briefs")
    repo.db.execute("DROP TABLE IF EXISTS companies")
    repo.db.execute("DROP TABLE IF EXISTS recommendations")
    repo.db.execute("DROP TABLE IF EXISTS events")
    repo.close()


def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "database" in data["data"]
    assert data["data"]["pipeline"] == "ready"


def test_executive_brief_empty():
    from unittest.mock import patch

    with patch("src.api.deps.Repository.get_latest_executive_brief", return_value=None):
        response = client.get("/api/v1/executive-brief")
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        # If DB is empty, should return a default fallback
        assert data["data"]["id"] == "empty"


def test_companies_endpoint():
    response = client.get("/api/v1/companies?limit=10")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)
    assert data["meta"]["limit"] == 10


def test_timeline_endpoint():
    response = client.get("/api/v1/timeline?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_recommendations_endpoint():
    response = client.get("/api/v1/recommendations")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert isinstance(data["data"], list)


def test_search_endpoint():
    response = client.get("/api/v1/search?q=test")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "companies" in data["data"]
    assert "events" in data["data"]


@patch("src.api.pipeline.BackgroundTasks.add_task")
def test_pipeline_run_endpoint(mock_add_task):
    response = client.post("/api/v1/pipeline/run")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["meta"]["status"] == "running"
    mock_add_task.assert_called_once()
