# Request Flow

```text
Client
  -> UDP/TCP port 53: dnsmasq resolves app.teamX.test
  -> TCP port 8443: TLS terminates at Nginx
  -> HTTP port 3001 or 3002: Nginx load balances to a backend
  -> HTTPS response: JSON plus X-Backend and cache headers
```

DNS resolves hostnames to the Nginx address. TLS protects the client-to-edge connection. HTTP between Nginx and the backends stays on the private LAN.
