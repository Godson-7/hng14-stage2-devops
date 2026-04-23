#!/bin/bash
set -e

MAX_WAIT=60
INTERVAL=5
ELAPSED=0

echo "Waiting for frontend to be ready..."
until curl -sf http://localhost:3000/health > /dev/null; do
  if [ $ELAPSED -ge $MAX_WAIT ]; then
    echo "Timeout waiting for frontend"
    exit 1
  fi
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "Submitting a job..."
RESPONSE=$(curl -sf -X POST http://localhost:3000/submit \
  -H "Content-Type: application/json")
echo "Response: $RESPONSE"

JOB_ID=$(echo $RESPONSE | python3 -c "import sys,json; print(json.load(sys.stdin)['job_id'])")
echo "Job ID: $JOB_ID"

echo "Polling for job completion..."
ELAPSED=0
while [ $ELAPSED -lt $MAX_WAIT ]; do
  STATUS=$(curl -sf http://localhost:3000/status/$JOB_ID | \
    python3 -c "import sys,json; print(json.load(sys.stdin)['status'])")
  echo "Status: $STATUS"
  if [ "$STATUS" = "completed" ]; then
    echo "Integration test passed"
    exit 0
  fi
  sleep $INTERVAL
  ELAPSED=$((ELAPSED + INTERVAL))
done

echo "Integration test failed - job did not complete in time"
exit 1