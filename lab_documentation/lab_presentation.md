# 🧪 Fault-Tolerant Distributed Systems — From Failure to Design


# 🧭 Part 1 — Why Distributed Systems Are Hard (10 min)

## 💥 The Illusion of “It Works”

In a single-node system:

* Memory is reliable
* Execution is predictable
* State is local

In a distributed system:

* Nodes crash
* Messages are lost
* State is fragmented

👉 **Key idea: Failure is not an exception — it is the default**

---

## ⚠️ Fundamental Problem

> A distributed system must behave correctly **even when parts of it fail**

---

## 🔥 Demo Thought Experiment

Imagine:

* A job is submitted
* Worker starts processing
* Worker crashes mid-task

Questions:

* Is the job lost?
* Should it retry?
* Could it run twice?

👉 These are not bugs — these are **design decisions**

---

# 🧠 Part 2 — Core Concepts (Theory Meets Practice) (15 min)

---

## 1. Replication

### Idea:

Store the same data on multiple nodes

### Why:

* Survive node failures
* Improve availability

### Tradeoff:

* Consistency vs availability

---

## 2. Leader-Based Systems

### Idea:

One node is responsible for:

* accepting writes
* coordinating state

### Why:

* simplifies consistency

### Risk:

* leader failure

---

## 3. Failure Detection

### Problem:

How do we know a node is dead?

### Reality:

We don’t — we **suspect** based on timeouts

👉 This is called **partial failure**

---

## 4. Consistency Models

### Strong Consistency:

All nodes see same state immediately

### Eventual Consistency:

State converges over time

👉 In this lab:
We aim for:

* **no data loss**
* **eventual correctness**

---

## 5. Idempotency

### Idea:

Running the same operation multiple times produces the same result

### Why:

Failures cause retries

---

## 6. At-least-once vs Exactly-once

| Model         | Meaning                |
| ------------- | ---------------------- |
| At-least-once | May run multiple times |
| Exactly-once  | Runs once (hard!)      |

👉 In practice:
We aim for:

* at-least-once + idempotency

---

# 🔗 Part 3 — Link to Theory (10 min)

---

## 📚 FLP Impossibility Result

> You cannot guarantee consensus in an asynchronous system with failures

👉 Translation:

* You cannot have perfect agreement + perfect availability

---

## ⚖️ CAP Theorem

You can only choose **two of three**:

* Consistency
* Availability
* Partition tolerance

👉 In real systems:
Partition tolerance is mandatory

So you choose between:

* Consistency
* Availability

---

## 🧠 What this means for your lab

You are building a system that:

* tolerates failures
* sacrifices strict consistency if needed
* guarantees eventual correctness

---

# ⚠️ Part 4 — Common Pitfalls (10 min)

---

## ❌ Pitfall 1: Single Point of Failure

* only one queue node
* system dies when it dies

---

## ❌ Pitfall 2: No Retry Logic

* worker crashes → job stuck forever

---

## ❌ Pitfall 3: No Replication

* leader dies → all jobs lost

---

## ❌ Pitfall 4: Stuck RUNNING Jobs

* job marked RUNNING
* worker dies
* job never retried

---

## ❌ Pitfall 5: Duplicate Execution Bugs

* job runs twice
* result overwritten incorrectly

---

## ❌ Pitfall 6: Hardcoded Dependencies

* gateway only talks to queue1

---

## ✅ Good Practices

* retry with fallback
* timeout-based recovery
* idempotent operations
* replication before acknowledgment
* clear state transitions

---

# 🧪 Part 5 — Understanding the Lab (5 min)

---

## 🎯 Your Task

You are given a **broken distributed system**

It:

* works in normal conditions
* fails under stress

Your job is to:
👉 **Make it survive failure**

---

## 💡 What You Must Achieve

* jobs are not lost
* system recovers from:

  * worker crash
  * leader crash
* jobs eventually complete

---

## 🧠 Important Insight

You are not writing “correct code”

👉 You are designing **correct behavior under failure**

---

# 🛠️ Part 6 — Implementation Strategy (10 min)

---

## Step 1 — Understand the Baseline

Run the system:

```bash
docker compose up --build -d
```

Test it:

```bash
pytest grader/tests -v
```

---

## Step 2 — Break It Yourself

```bash
docker compose kill queue1
docker compose kill worker1
```

Observe:

* what failed?
* why?

---

## Step 3 — Fix Worker Failures

Problem:

* RUNNING jobs get stuck

Solution:

* add timeout
* reset job to PENDING

---

## Step 4 — Add Gateway Failover

Problem:

* gateway depends on one node

Solution:

* try multiple queues

---

## Step 5 — Add Replication

Problem:

* data lost on crash

Solution:

* replicate jobs to second node

---

## Step 6 — Add Basic Leader Logic

* one node accepts writes
* fallback if leader fails

---

## Step 7 — Make Completion Safe

Problem:

* duplicate execution

Solution:

* ignore duplicate completion

---

## Step 8 — Pass the Grader

Run:

```bash
pytest grader/tests -v
```

Fix until all pass.

---

# 🧠 Final Takeaways (5 min)

---

## 🧩 Key Lessons

* Distributed systems fail by default
* Fault tolerance must be designed
* Replication is essential
* Retries require idempotency
* There is no perfect solution (CAP, FLP)

---

## 💬 Final Thought

> “A distributed system is one where the failure of a computer you didn’t even know existed can make your program fail.”

---

## 🚀 What You Should Focus On

If you’re stuck, ask:

* What happens if this node dies?
* What happens if this message is lost?
* What happens if this runs twice?

👉 That’s how distributed systems are built.

---

# ✅ End of Session
