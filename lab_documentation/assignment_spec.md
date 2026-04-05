# 📄 1. Assignment Specification (Student Handout)

## 🧪 Assignment: Break & Fix — Fault-Tolerant Distributed Task Queue

### 🎯 Objective

In this assignment, you will build a **distributed task queue** and evolve it from a **fragile single-node system** into a **fault-tolerant distributed service**.

Your system must:

* accept jobs via an HTTP API
* process them asynchronously using worker nodes
* survive failures (worker crash, leader crash)
* ensure that **acknowledged jobs are not lost**

---

## 🏗️ System Overview

Your system will consist of the following components:

* **gateway** (HTTP entry point — used by the grader)
* **queue nodes** (`queue1`, `queue2`)
* **worker node(s)** (`worker1`, optional `worker2`)

The instructor provides:

* Docker Compose boilerplate
* Worker boilerplate
* Reset endpoint boilerplate
* Grader (pytest-based)

You implement:

* queue logic
* replication / coordination
* fault tolerance

---

## 🌐 API Contract (MANDATORY)

All systems must expose an HTTP API at:

```
http://localhost:${GATEWAY_PORT}
```

### 1. Submit Job

```
POST /jobs
```

**Request:**

```json
{
  "operation": "square",
  "value": 7
}
```

**Response:**

```json
{
  "job_id": "uuid"
}
```

---

### 2. Get Job Status

```
GET /jobs/<job_id>
```

**Response:**

```json
{
  "job_id": "uuid",
  "status": "PENDING | RUNNING | COMPLETED | FAILED",
  "result": 49
}
```

---

### 3. Health Check

```
GET /health
```

**Response:**

```json
{
  "status": "ok"
}
```

---

### 4. Cluster Info

```
GET /cluster
```

**Response:**

```json
{
  "leader": "queue1",
  "nodes": ["queue1", "queue2"],
  "workers": ["worker1"]
}
```

---

### 5. Reset (Provided)

```
POST /admin/reset
```

Resets system state between tests.

---

## ⚙️ Environment Configuration (.env)

You must use a `.env` file.

Example:

```env
GATEWAY_PORT=8080
QUEUE_NODES=queue1,queue2
WORKER_NODES=worker1
```

---

## 🧩 Functional Requirements

### Basic Functionality

* Jobs can be submitted via the gateway
* Workers process jobs asynchronously
* Job status transitions correctly:

  * PENDING → RUNNING → COMPLETED

---

### Fault Tolerance

Your system must handle:

#### 1. Worker Failure

* If a worker crashes during execution:

  * the job must eventually complete
  * it must not be lost

---

#### 2. Queue Node Failure (Leader Failure)

* If the leader node crashes:

  * another node must take over
  * previously accepted jobs must still exist
  * system must continue processing

---

### Replication Requirement

* Jobs must be replicated to at least one other node before being acknowledged

---

### Job Semantics

* A job that is acknowledged must:

  * **eventually reach a terminal state**
  * **not disappear**
* Final state must contain **at most one successful completion per job**

---

## 🐳 Docker Requirements

You must support:

```bash
docker compose up --build -d
```

And your system must be reachable within **30 seconds**.

---

## 🧪 Grading

You will be graded using an **automated pytest-based grader**.

To test locally:

```bash
pytest grader/tests -v
```

---

## 📦 Deliverables

Your repository must include:

* `docker-compose.yml`
* `.env`
* source code
* compatibility with provided grader

---

<!-- ## 📊 Grading Breakdown

| Category             | Points |
| -------------------- | ------ |
| Packaging & Docker   | 20     |
| API Compliance       | 15     |
| Basic Functionality  | 20     |
| Fault Tolerance      | 25     |
| Grader Compatibility | 10     |
| Code Quality & Docs  | 10     |

--- -->

## 🚫 Constraints

* Python only
* HTTP API mandatory
* Fixed service names required:

  * `gateway`
  * `queue1`, `queue2`
  * `worker1`
* Do NOT modify grader tests

---

---

# 📘 2. Reference API Contract (Instructor Spec)

This is your internal “source of truth” for grading.

## Job Model

```json
job = {
        "job_id": string,
        "operation": "square" or "sleep",
        "value": payload.get("value"),
        "duration": if operation is sleep -> float(payload.get("duration", 0)),
        "status": "PENDING | RUNNING | COMPLETED | FAILED",
        "result": result of operation or value,
        "owner": None -> worker_id who executes the job,
        "started_at": timestamp -> time.time(),
        "created_at": created at -> time.time(),
        "updated_at": created at -> time.time(),
        "completed_at": time.time(),
        "attempts": 0,
}
```
Not all fields are mandatory; Implement what is required by the given tests.

---

## Supported Operations (MANDATORY)

Keep this fixed:

### square

```
input: integer
output: integer^2
```

### sleep

```
input: { "duration": seconds, "value": X }
output: X after delay
```

👉 `sleep` is critical for failure testing.

---

## Status Rules

| State     | Meaning                  |
| --------- | ------------------------ |
| PENDING   | Accepted but not started |
| RUNNING   | Assigned to worker       |
| COMPLETED | Successfully finished    |
| FAILED    | Terminal failure         |

---

## Timing Constraints

* Job must complete within:

  * normal job: 5 seconds
  * sleep job: duration + 5 seconds buffer

---

## Failure Semantics

### Required guarantees:

* no acknowledged job is lost
* eventual completion
* system recovers after:

  * 1 queue node failure
  * 1 worker failure

---

## Leader Behavior (loosely defined)

* exactly one leader at a time (best effort)
* leader handles:

  * job acceptance
  * scheduling
* follower(s):

  * replicate state
  * can take over

Implementation is up to you. 
Go for the simplest model that passes the tests. 
E.g keep the first queue as leader until it fails.
You are not expected to implement a leader election mechanism.

---

---

# 🧪 3. Pytest Grader Skeleton

## 📁 Structure

```text
grader/
├── requirements.txt
├── pytest.ini
├── conftest.py
└── tests/
    ├── test_00_boot.py
    ├── test_01_basic.py
    ├── test_02_multiple_jobs.py
    ├── test_03_worker_failure.py
    ├── test_04_leader_failure.py
```

---

## requirements.txt for tests

```txt
pytest
requests
tenacity
```



# Lab Reference Implementation

## Run

```bash
docker compose up --build -d
```

## Smoke test

```bash
curl -s http://localhost:8080/health
curl -s -X POST http://localhost:8080/jobs \
  -H 'Content-Type: application/json' \
  -d '{"operation":"square","value":7}'
```
or in one line:
```
curl -s -X POST http://localhost:8080/jobs -H 'Content-Type: application/json' -d '{"operation":"square","value":7}'
```
This returns a job_id
```json
{"job_id":"d344f36d-f3bf-446f-8f2a-276ef5abffdc"}
```

Get Results of submitted job:
```bash
curl -s http://localhost:8080/jobs/<job_id>
```

Expected result, somthing similar to:
```json
{
  "duration":0,
  "job_id":"f4b53bbc-9de7-41cb-9e5a-43f35d75f01a",
  "operation":"square",
  "result":49,
  "status":"COMPLETED",
  "value":7
}
```

## Reset
This gateway endpoint calls the */internal/reset* endpoint of the queue service
to clean the *jobs* dictionary.
```bash
curl -s -X POST http://localhost:8080/admin/reset
```

## Grader

From project root:
```bash
python -m venv .venv # Create a python virtual environment.
source .venv/bin/activate # Acitvate it.
pip install -r grader/requirements.txt # Install requirements.
pytest grader/tests -v # Use this for tests. You don't have to repeat the venv commands.
```

You can run just a single test with the -k flag:
```bash
pytest grader/tests -v -k test_02
```
[See this brief guide on pytest](using_pytest.md)