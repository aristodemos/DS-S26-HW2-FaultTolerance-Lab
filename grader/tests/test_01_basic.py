from grader.conftest import reset_system, submit_job, wait_for_completion


def test_single_job():
    reset_system()
    job_id = submit_job({"operation": "square", "value": 5})
    job = wait_for_completion(job_id)
    assert job["result"] == 25
