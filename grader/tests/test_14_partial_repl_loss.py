import time

from grader.conftest import kill_service, reset_system, submit_job, wait_for_completion, reset_system, restart_service


def test_replication_survives_leader_death():
    reset_system()


    job_id = submit_job({"operation": "square", "value": 8})

    time.sleep(1)  # ensure accepted

    kill_service("queue1")

    job = wait_for_completion(job_id, timeout=45)

    assert job["result"] == 64

    restart_service("queue1")