# Backend A

Backend A is a small Python HTTP server used as one target in the Phase 1 Nginx upstream pool.

## Details

- Listen address: `0.0.0.0:3001`
- Root endpoint: `GET /`
- Status endpoint: `GET /api/status`
- Successful responses identify the server with `"backend": "A"` and `X-Backend: A`.
- Unknown paths return HTTP `404`.

## Run and test

From the project root:

```sh
python3 backend-a/server.py
curl http://127.0.0.1:3001/
curl http://127.0.0.1:3001/api/status
```

The server also handles `HEAD` requests. JSON responses include an `ETag` and `Cache-Control: max-age=60` header.