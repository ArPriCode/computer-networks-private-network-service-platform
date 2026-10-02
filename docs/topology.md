# Network Topology

Phase 1 has one Nginx reverse proxy and two independent Python HTTP backends:

```text
Client
	|
	| HTTPS :443 (app.team1.test)
	v
Nginx reverse proxy
	|                         |
	| HTTP :3001              | HTTP :3002
	v                         v
Backend A                 Backend B
```

The Nginx `backend_pool` upstream contains both backend addresses. Nginx terminates TLS at the client-facing virtual host and proxies requests to the backends over HTTP. Both backend processes must be running and reachable from the Nginx host.

The IP addresses in the source and Nginx configuration are fixed values for the current lab setup. Update them if the hosts or network change; see [IP addresses and ports](ip-addresses.md).
