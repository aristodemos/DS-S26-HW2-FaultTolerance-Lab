import os
import subprocess
import time

import requests
from tenacity import retry, stop_after_attempt, wait_fixed

BASE_URL = f"http://localhost:{os.getenv('GATEWAY_PORT', '8080')}"


@retry(stop=stop_after_attempt(30), wait=wait_fixed(1))
def wait_for_system():
    response = requests.get(f"{BASE_URL}/health", timeout=2)
    assert response.status_code == 200

def submit_job_with_retries(payload, num_retires=3, timeout=15):
    for i in range(num_retires):
        try:
            response = requests.post(f"{BASE_URL}/jobs", json=payload, timeout=timeout)
            break
        except requests.Timeout:
            time.sleep(1)
    assert response.status_code == 200, response.text
    assert "job_id" in response.json()
    return response.json()["job_id"]

def submit_job(payload):
    response = requests.post(f"{BASE_URL}/jobs", json=payload, timeout=3)
    assert response.status_code == 200, response.text
    return response.json()["job_id"]


def get_job(job_id):
    response = requests.get(f"{BASE_URL}/jobs/{job_id}", timeout=5)
    assert response.status_code == 200, response.text
    return response.json()


def wait_for_completion(job_id, timeout=25):
    deadline = time.time() + timeout
    while time.time() < deadline:
        job = get_job(job_id)
        if "status" in job and job["status"] == "COMPLETED":
            return job
        time.sleep(1)
    raise TimeoutError(f"Job {job_id} did not complete in time")


def kill_service(name):
    subprocess.run(["docker", "compose", "kill", name], check=True)


def restart_service(name):
    subprocess.run(["docker", "compose", "up", "-d", name], check=True)


def reset_system():
    response = requests.post(f"{BASE_URL}/admin/reset", timeout=3)
    assert response.status_code == 200
    time.sleep(1)
