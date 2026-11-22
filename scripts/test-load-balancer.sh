#!/bin/bash
set -euo pipefail

URL="${1:-https://app.teamX.test:8443/api/status}"

for i in {1..10}; do
    printf 'Request %s: ' "$i"
    curl -sS -D - -o /dev/null "$URL" | grep -i '^X-Backend:' || true
done