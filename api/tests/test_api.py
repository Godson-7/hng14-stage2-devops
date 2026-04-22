from fastapi.testclient import TestClient
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_health_endpoint():
    with patch('redis.Redis') as mock_redis:
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock_redis.return_value = mock_instance
        import main
        main.r = mock_instance
        client = TestClient(main.app)
        response = client.get("/health")
        assert response.status_code == 200

def test_create_job():
    with patch('redis.Redis') as mock_redis:
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock_redis.return_value = mock_instance
        import main
        main.r = mock_instance
        client = TestClient(main.app)
        response = client.post("/jobs")
        assert response.status_code == 200
        assert "job_id" in response.json()

def test_get_missing_job_returns_404():
    with patch('redis.Redis') as mock_redis:
        mock_instance = MagicMock()
        mock_instance.ping.return_value = True
        mock_instance.hget.return_value = None
        mock_redis.return_value = mock_instance
        import main
        main.r = mock_instance
        client = TestClient(main.app)
        response = client.get("/jobs/nonexistent-id")
        assert response.status_code == 404