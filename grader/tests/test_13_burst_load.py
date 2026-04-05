from grader.conftest import submit_job, wait_for_completion, reset_system

def test_burst_load():
    
    reset_system()
    jobs = [submit_job({"operation": "square", "value": i}) for i in range(20)]

    results = [wait_for_completion(j, timeout=30) for j in jobs]

    assert len(results) == 20