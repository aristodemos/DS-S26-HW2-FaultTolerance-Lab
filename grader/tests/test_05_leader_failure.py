import time

from grader.conftest import kill_service, reset_system, submit_job, wait_for_completion, restart_service


def test_leader_failover():
    reset_system()
    job_id = submit_job({"operation": "square", "value": 9})
    time.sleep(5)
    kill_service("queue1")
    job = wait_for_completion(job_id, timeout=60)
    assert job["result"] == 81
    restart_service("queue1")