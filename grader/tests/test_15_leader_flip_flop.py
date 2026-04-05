from grader.conftest import submit_job, wait_for_completion, kill_service, restart_service, reset_system, submit_job_with_retries
import time

def test_leader_instability():
    pass
    # reset_system()
    # job_id = submit_job_with_retries({"operation": "square", "value": 6}, 5)
    
    # print(f"job --> {job_id}")

    # kill_service("queue1")
    # time.sleep(2)
    # restart_service("queue1")

    # kill_service("queue2")
    # time.sleep(2)
    # restart_service("queue2")

    # job = wait_for_completion(job_id, timeout=60)

    # assert job["result"] == 36