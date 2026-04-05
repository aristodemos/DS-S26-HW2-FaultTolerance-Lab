import time

from grader.conftest import kill_service, reset_system, restart_service, submit_job, wait_for_completion


def test_worker_failure_recovery():
    reset_system()
    job_id = submit_job({"operation": "sleep", "value": 42, "duration": 5})
    time.sleep(2)
    kill_service("worker1")
    time.sleep(2)
    restart_service("worker1")
    job = wait_for_completion(job_id, timeout=30)
    assert job["result"] == 42
