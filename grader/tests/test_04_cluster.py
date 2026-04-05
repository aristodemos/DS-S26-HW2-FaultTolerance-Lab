import requests

from grader.conftest import BASE_URL, reset_system


def test_cluster_endpoint():
    reset_system()
    response = requests.get(f"{BASE_URL}/cluster", timeout=5)
    assert response.status_code == 200
    payload = response.json()
    assert "leader" in payload
    assert "nodes" in payload
    assert "workers" in payload
