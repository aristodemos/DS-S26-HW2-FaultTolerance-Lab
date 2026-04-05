import time

from grader.conftest import kill_service, reset_system, submit_job, wait_for_completion, get_job

def test_no_duplicate_completion():
    reset_system()

    job_id = submit_job({"operation": "square", "value": 7})

    job = wait_for_completion(job_id)

    assert job["result"] == 49

    # Wait extra time to detect duplicate writes
    time.sleep(3)

    job_after = get_job(job_id)

    assert job_after["result"] == 49
    assert job_after["status"] == "COMPLETED"