# HTTP Request Flow

1. The client resolves `app.teamX.test` to the Nginx host and opens an HTTPS connection on port `8443`.
2. Nginx presents the configured certificate and key, then proxies the request to the `backend_pool` over HTTP.
3. The pool contains Backend A (`:3001`) and Backend B (`:3002`). With no balancing directive configured, Nginx uses its default round-robin upstream selection; this setup does not configure active health checks.
4. The selected backend returns JSON. `/` and `/api/status` return `200`; an unknown path returns `404`.
5. Nginx returns the backend response to the client over the HTTPS connection.

The backends identify their response with `X-Backend: A` or `X-Backend: B`. They also send `Cache-Control: max-age=60` and an `ETag`. The current handlers provide the ETag header but do not implement conditional `If-None-Match` handling.

To verify direct backend responses, run:

```sh
curl -i http://127.0.0.1:3001/api/status
curl -i http://127.0.0.1:3002/api/status
```

After configuring DNS and importing the TeamX local CA, test the proxy with `curl -i https://app.teamX.test:8443/api/status`. Do not use `-k` in the final demonstration.
