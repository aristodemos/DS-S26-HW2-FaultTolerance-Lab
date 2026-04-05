import time
from grader.conftest import reset_system, submit_job, wait_for_completion


def test_sleep_respects_requested_duration():
    reset_system()

    durations = [5, 6, 7]  # different values to verify behavior
    tolerance = 0.2  # small buffer for timing jitter

    job_ids = [
        submit_job({"operation": "sleep", "duration": d, "value": i})
        for i, d in enumerate(durations)
    ]

    results = []
    for job_id, expected_duration in zip(job_ids, durations):
        start = time.time()

        result = wait_for_completion(job_id)

        elapsed = time.time() - start

        # ✅ Verify minimum duration is respected
        assert elapsed >= expected_duration, (
            f"Task finished too early: expected ≥ {expected_duration}s, got {elapsed:.2f}s"
        )

        # ✅ Optional: guard against extreme overshoot (sanity check)
        assert elapsed < expected_duration + 2, (
            f"Task took too long: expected ~{expected_duration}s, got {elapsed:.2f}s"
        )

        # ✅ Verify correctness of returned value
        results.append(result)

    for i, r in enumerate(results):
        assert r["result"] == i