#!/bin/bash
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "========== MAC 1: PHASE 1 + PHASE 2 =========="

CONF="$PROJECT/config/dnsmasq/dnsmasq.conf"
grep -q '^local-ttl=30$' "$CONF" || echo 'local-ttl=30' >> "$CONF"

echo "===== PRIMARY DNS ====="
dig @10.7.15.60 app.teamX.test

echo "===== BACKUP DNS ====="
dig @10.7.21.116 app.teamX.test

echo "===== HTTPS ====="
curl -i --connect-timeout 5 https://app.teamX.test:8443/ || true

echo "===== LOAD BALANCING ====="
for i in {1..10}; do
  curl -sSI --connect-timeout 5 https://app.teamX.test:8443/api/status |
    grep -i '^X-Backend:' || true
done

echo "===== CACHE 200 ====="
curl -i https://app.teamX.test:8443/api/status || true

echo "===== CACHE 304 ====="
ETAG="$(curl -sSI https://app.teamX.test:8443/api/status |
  awk 'tolower($1)=="etag:" {gsub("\r","",$2); print $2}')"
if [[ -n "$ETAG" ]]; then
  curl -i -H "If-None-Match: $ETAG" https://app.teamX.test:8443/api/status || true
fi

echo "===== BACKEND A ====="
curl -sS http://127.0.0.1:3001/api/status || true

echo "===== MAC 1 COMPLETE ====="
