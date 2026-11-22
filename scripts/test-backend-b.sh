#!/bin/bash
set -euo pipefail

curl -i --fail http://127.0.0.1:3002/
curl -I --fail http://127.0.0.1:3002/api/status