# hng14-stage2-devops

A containerized job processing system with a frontend, API, worker, and Redis queue.

## Services

- **Frontend** (Node.js/Express) — accepts job submissions on port 3000
- **API** (FastAPI/Python) — creates jobs and stores them in Redis on port 8000
- **Worker** (Python) — picks jobs from Redis queue and processes them
- **Redis** — message queue between API and worker

## How to Run

1. Clone the repo
2. Copy the example env file:
```bash
cp .env.example .env
```
3. Start the stack:
```bash
docker compose up --build
```
4. Open browser at http://localhost:3000

## How to Test

Submit a job:
```bash
curl -X POST http://localhost:3000/submit
```

Check job status:
```bash
curl http://localhost:3000/status/<job_id>
```

## Bugs Fixed

See [FIXES.md](FIXES.md) for all bugs found and fixed.