from grader.conftest import reset_system, submit_job, wait_for_completion


def test_multiple_jobs():
    reset_system()
    job_ids = [submit_job({"operation": "square", "value": i}) for i in range(5)]
    results = [wait_for_completion(job_id) for job_id in job_ids]
    assert [r["result"] for r in results] == [i * i for i in range(5)]
