from flask import Flask, request, jsonify
import uuid

app = Flask(__name__)

jobs = {}

@app.route("/internal/jobs", methods=["POST"])
def create_job():
    job_id = str(uuid.uuid4())
    job = {
        "job_id": job_id,
        "operation": request.json["operation"],
        "value": request.json.get("value"),
        "duration": request.json.get("duration", 0),
        "status": "PENDING",
        "result": None
    }
    jobs[job_id] = job
    return {"job_id": job_id}


@app.route("/internal/jobs/<job_id>")
def get_job(job_id):
    return jsonify(jobs.get(job_id, {}))


@app.route("/internal/next_job")
def next_job():
    for job in jobs.values():
        if job["status"] == "PENDING":
            job["status"] = "RUNNING"
            return jsonify(job)
    return jsonify({})


@app.route("/internal/complete", methods=["POST"])
def complete():
    job_id = request.json["job_id"]
    jobs[job_id]["status"] = "COMPLETED"
    jobs[job_id]["result"] = request.json["result"]
    return {"status": "ok"}


@app.route("/internal/reset", methods=["POST"])
def reset():
    global jobs
    jobs = {}
    return {"status": "reset"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)