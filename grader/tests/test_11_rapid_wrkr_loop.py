import time

from grader.conftest import submit_job, wait_for_completion, kill_service, restart_service, reset_system

def test_worker_crash_loop():
    
    reset_system()

    job_id = submit_job({
        "operation": "sleep",
        "value": 99,
        "duration": 6
    })

    for _ in range(3):
        time.sleep(1)
        kill_service("worker1")
        time.sleep(1)
        restart_service("worker1")

    job = wait_for_completion(job_id, timeout=40)

    assert job["result"] == 99