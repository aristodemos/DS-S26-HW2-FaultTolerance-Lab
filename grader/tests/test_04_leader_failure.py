def test_leader_failover():
    from conftest import submit_job, wait_for_completion, kill_service

    job_id = submit_job({"operation": "square", "value": 9})

    time.sleep(1)
    kill_service("queue1")

    job = wait_for_completion(job_id, timeout=30)

    assert job["result"] == 81