# Bug Fixes

## Fix 1
- **File:** api/main.py
- **Line:** 6
- **Problem:** Redis host hardcoded as "localhost" — fails in Docker networking
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 2
- **File:** api/main.py
- **Line:** 6
- **Problem:** Redis port hardcoded as 6379
- **Fix:** Changed to `int(os.getenv("REDIS_PORT", 6379))`

## Fix 3
- **File:** api/main.py
- **Line:** 6
- **Problem:** No error handling on Redis connection at startup
- **Fix:** Wrapped in try/except, raises on failure with clear message

## Fix 4
- **File:** api/main.py
- **Line:** 17
- **Problem:** 404 "not found" returned with HTTP 200 status code
- **Fix:** Changed to JSONResponse with status_code=404

## Fix 5
- **File:** api/main.py
- **Line:** N/A
- **Problem:** No /health endpoint — Docker HEALTHCHECK had nothing to ping
- **Fix:** Added GET /health endpoint that also verifies Redis connectivity

## Fix 6
- **File:** worker/worker.py
- **Line:** 5
- **Problem:** Redis host hardcoded as "localhost"
- **Fix:** Changed to `os.getenv("REDIS_HOST", "redis")`

## Fix 7
- **File:** worker/worker.py
- **Line:** 5
- **Problem:** Redis port hardcoded as 6379
- **Fix:** Changed to `int(os.getenv("REDIS_PORT", 6379))`

## Fix 8
- **File:** worker/worker.py
- **Line:** N/A
- **Problem:** signal imported but SIGTERM never handled — container kills cause abrupt stop
- **Fix:** Added signal.signal handlers for SIGTERM and SIGINT

## Fix 9
- **File:** worker/worker.py
- **Line:** N/A
- **Problem:** No Redis reconnection logic — if Redis restarts, worker dies silently
- **Fix:** Added connect_redis() loop with retry

## Fix 10
- **File:** frontend/app.js
- **Line:** 5
- **Problem:** API URL hardcoded as "http://localhost:8000" — fails in Docker
- **Fix:** Changed to `process.env.API_URL || "http://api:8000"`

## Fix 11
- **File:** frontend/app.js
- **Line:** N/A
- **Problem:** app.listen binds to 127.0.0.1 by default — unreachable from other containers
- **Fix:** Added '0.0.0.0' as bind address

## Fix 12
- **File:** frontend/app.js
- **Line:** N/A
- **Problem:** No /health endpoint
- **Fix:** Added GET /health route

## Fix 13
- **File:** api/requirements.txt
- **Problem:** No pinned versions — builds are not reproducible
- **Fix:** Pinned all packages to specific versions

## Fix 14
- **File:** worker/requirements.txt
- **Problem:** No pinned versions
- **Fix:** Pinned redis to 5.0.1
