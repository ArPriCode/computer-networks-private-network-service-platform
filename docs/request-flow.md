# HTTP Request Flow

1. The client resolves `app.team1.test` to the Nginx host and opens an HTTPS connection on port `443`.
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

After configuring DNS or a hosts-file entry and starting Nginx, test the proxy with `curl -k -i https://app.team1.test/api/status`. The `-k` option is only appropriate for a local/self-signed lab certificate.
