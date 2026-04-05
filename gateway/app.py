from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

QUEUE_HOST = os.getenv("QUEUE_HOST", "queue1")
QUEUE_PORT = os.getenv("QUEUE_PORT", "5000")

def queue_url(path):
    return f"http://{QUEUE_HOST}:{QUEUE_PORT}{path}"

@app.route("/health")
def health():
    return {"status": "ok"}

@app.route("/jobs", methods=["POST"])
def submit_job():
    r = requests.post(queue_url("/internal/jobs"), json=request.json)
    return jsonify(r.json())

@app.route("/jobs/<job_id>")
def get_job(job_id):
    r = requests.get(queue_url(f"/internal/jobs/{job_id}"))
    return jsonify(r.json())

@app.route("/admin/reset", methods=["POST"])
def reset():
    requests.post(queue_url("/internal/reset"))
    return {"status": "reset"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)