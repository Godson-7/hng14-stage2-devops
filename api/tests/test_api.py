from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with patch('redis.Redis') as mock_redis:
    mock_instance = MagicMock()
    mock_instance.ping.return_value = True
    mock_redis.return_value = mock_instance
    import main
    main.r = mock_instance

client = TestClient(main.app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_create_job_returns_job_id():
    main.r.lpush = MagicMock(return_value=1)
    main.r.hset = MagicMock(return_value=1)
    response = client.post("/jobs")
    assert response.status_code == 200
    assert "job_id" in response.json()

def test_get_missing_job_returns_404():
    main.r.hget = MagicMock(return_value=None)
    response = client.get("/jobs/nonexistent-id")
    assert response.status_code == 404

def test_get_existing_job_returns_status():
    main.r.hget = MagicMock(return_value=b"queued")
    response = client.get("/jobs/some-real-id")
    assert response.status_code == 200
    assert response.json()["status"] == "queued"