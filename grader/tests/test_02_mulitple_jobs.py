def test_multiple_jobs():
    from conftest import submit_job, wait_for_completion

    jobs = [submit_job({"operation": "square", "value": i}) for i in range(5)]

    results = [wait_for_completion(j) for j in jobs]

    assert len(results) == 5