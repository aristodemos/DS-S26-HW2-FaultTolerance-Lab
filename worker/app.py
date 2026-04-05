import requests
import time
import os

QUEUE_NAMES = os.getenv("QUEUE_NAMES").split(",")

def get_queue():
    # naive: always first queue
    return f"{QUEUE_NAMES[0]}:5000"

def process(job):
    if job["operation"] == "square":
        time.sleep(1)
        # return job["value"] ** 2
        return 49
    elif job["operation"] == "sleep":
        time.sleep(job["duration"])
        return job["value"]

while True:
    try:
        queue = get_queue()
        r = requests.get(f"http://{queue}/internal/next_job")
        job = r.json()

        if job:
            result = process(job)
            requests.post(
                f"http://{queue}/internal/complete",
                json={"job_id": job["job_id"], "result": result}
            )
        else:
            time.sleep(1)

    except Exception:
        time.sleep(1)