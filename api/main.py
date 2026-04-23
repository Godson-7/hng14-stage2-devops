from fastapi import FastAPI
from fastapi.responses import JSONResponse
import redis
import uuid
import os

app = FastAPI()

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)


@app.get("/health")
def health():
    try:
        r.ping()
        return {"status": "ok"}
    except redis.ConnectionError:
        return JSONResponse(status_code=503, content={"status": "redis unavailable"})


@app.post("/jobs")
def create_job():
    job_id = str(uuid.uuid4())
    r.lpush("jobs", job_id)
    r.hset(f"job:{job_id}", "status", "queued")
    return {"job_id": job_id}


@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    status = r.hget(f"job:{job_id}", "status")
    if not status:
        return JSONResponse(status_code=404, content={"error": "not found"})
    return {"job_id": job_id, "status": status.decode()}
