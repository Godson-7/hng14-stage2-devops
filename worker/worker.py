import redis
import time
import os
import signal
import sys

REDIS_HOST = os.getenv("REDIS_HOST", "redis")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

def connect_redis():
    while True:
        try:
            client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)
            client.ping()
            print("Connected to Redis")
            return client
        except redis.ConnectionError:
            print("Redis not ready, retrying in 2s...")
            time.sleep(2)

r = connect_redis()

def handle_shutdown(signum, frame):
    print("Shutting down worker gracefully...")
    sys.exit(0)

signal.signal(signal.SIGTERM, handle_shutdown)
signal.signal(signal.SIGINT, handle_shutdown)

def process_job(job_id):
    print(f"Processing job {job_id}")
    time.sleep(2)
    r.hset(f"job:{job_id}", "status", "completed")
    print(f"Done: {job_id}")

print("Worker started, waiting for jobs...")
while True:
    try:
        job = r.brpop("jobs", timeout=5)
        if job:
            _, job_id = job
            process_job(job_id.decode())
    except redis.ConnectionError:
        print("Lost Redis connection, reconnecting...")
        r = connect_redis()
