#!/bin/bash
set -euo pipefail

PID="$(lsof -ti tcp:3002 2>/dev/null || true)"
if [[ -n "$PID" ]]; then
    kill "$PID"
    echo "Stopped Backend B process $PID"
else
    echo "Backend B is not running"
fi