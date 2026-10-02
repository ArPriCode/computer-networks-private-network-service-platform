# Computer Networks Project 1

**Course:** Computer Networks

**Infrastructure:** Type 2, two physical Macs with combined roles

This is the Phase 1 lab design: Mac 1 runs DNS and Backend A; Mac 2 runs Nginx HTTPS and Backend B.

> **Status:** This README documents the requested two-Mac target. The current backend and Nginx files still use the previous `team1.test` configuration, port `443`, and different LAN addresses. DNS configuration and the scripts referenced in the proposed layout are not implemented in this checkout. Commands below are setup and verification instructions for the target design, not a claim that the target deployment has already been verified.

## Team

| Name | Roll number |
| --- | --- |
| Arun Kumar Giri | `2401010099` |
| Gaurav Meena | `2401010169` |
| Ritik Ranjan | Not provided |

## Architecture

### Machines

| Machine | Current LAN IP | Services |
| --- | --- | --- |
| Mac 1 | `10.7.15.60` | dnsmasq DNS `:53`; Backend A `:3001` |
| Mac 2 | `10.7.21.116` | Nginx HTTPS `:8443`; Backend B `:3002` |

These are current DHCP leases and may change. Run `ifconfig en0` on each Mac before testing, then update the DNS and Nginx configuration if needed.

### Request flow

```text
Client (Mac 2 or another LAN machine)
	| DNS query, UDP :53
	v
Mac 1: dnsmasq
	| app.teamX.test, api.teamX.test -> 10.7.21.116
	v
Mac 2: Nginx HTTPS :8443 (TLS terminates here)
	| default round-robin upstream
	+--------------------> Mac 1: Backend A :3001
	+--------------------> Mac 2: Backend B :3002

Response: JSON, X-Backend: A or B, Cache-Control: max-age=60
```

DNS points to the Nginx proxy, not directly to either backend.

| Hostname | Resolves to | Target |
| --- | --- | --- |
| `app.teamX.test` | `10.7.21.116` | Mac 2 Nginx |
| `api.teamX.test` | `10.7.21.116` | Mac 2 Nginx |

## Backend API

Both backends should expose the same endpoints, with the backend identity changed as appropriate.

| Method | Path | Response |
| --- | --- | --- |
| `GET` | `/` | `{"backend":"A","message":"Hello from Backend A"}` or Backend B equivalent |
| `GET` | `/api/status` | `{"backend":"A","status":"ok","server":"Backend A"}` or Backend B equivalent |
| `HEAD` | `/` or `/api/status` | Same status and headers as GET, without a body |

Successful responses should include `X-Backend: A` or `B`, `Cache-Control: max-age=60`, and `Content-Type: application/json`.

## TLS

Nginx on Mac 2 terminates HTTPS on port `8443`.

| Item | Target configuration |
| --- | --- |
| Local CA | TeamX local root CA |
| Server certificate | `app.crt`, signed by the local CA |
| Subject Alternative Names | `DNS:app.teamX.test`, `DNS:api.teamX.test` |
| Client trust | Import the root CA into macOS Keychain; trusted clients should not need `curl -k` |

The existing `ssl/cert.pem` is for `app.team1.test` and does not cover these TeamX names. A matching certificate is required before hostname-verified HTTPS testing. Keep all private keys local and never commit them.

## Project report

[View or download the Computer Networks project documentation](https://raw.githubusercontent.com/ArPriCode/computer-networks-private-network-service-platform/main/CN_Documentation.pdf).

## Setup

Both Macs must be on the same Wi-Fi LAN. Install Python 3 on both, dnsmasq on Mac 1, and Nginx on Mac 2:

```sh
brew install python
brew install dnsmasq # Mac 1
brew install nginx   # Mac 2
```

### Mac 1: DNS and Backend A

Find the dnsmasq configuration path with `brew info dnsmasq`. Configure the current Mac 1 address and DNS records (replace addresses if DHCP leases changed):

```conf
listen-address=127.0.0.1,10.7.15.60
address=/app.teamX.test/10.7.21.116
address=/api.teamX.test/10.7.21.116
```

Start dnsmasq and Backend A:

```sh
sudo brew services start dnsmasq
cd backend-a && python3 server.py
```

### Mac 2: Nginx HTTPS and Backend B

Set Mac 1 as the Wi-Fi DNS server, flush the resolver cache, and confirm the setting:

```sh
networksetup -setdnsservers "Wi-Fi" 10.7.15.60
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
networksetup -getdnsservers "Wi-Fi"
```

Configure Nginx to listen on `8443`, load the TeamX certificate and key, and proxy to `10.7.15.60:3001` and `10.7.21.116:3002`. Then validate and start Nginx and Backend B:

```sh
nginx -t
brew services start nginx
cd backend-b && python3 server.py
```

## Verification commands

Run these after configuring the target services. Update IPs if DHCP leases changed.

### DNS

```sh
dig @10.7.15.60 app.teamX.test
dig @10.7.15.60 api.teamX.test
dig app.teamX.test
```

Both names should resolve to Mac 2's current address. A direct query should identify Mac 1 as the DNS server.

### Mac A and Mac B screenshots

**Mac A — Backend A running**

![Mac A running Backend A](Screenshot%202026-10-02%20at%2019.10.59.png)

**Mac B — HTTPS requests reaching both backends**

![Mac B showing HTTPS responses from both backends](Screenshot%202026-10-02%20at%2019.10.59-1.png)

### Direct backend requests

```sh
curl http://10.7.15.60:3001/
curl http://10.7.21.116:3002/
curl -I http://10.7.15.60:3001/api/status
curl -I http://10.7.21.116:3002/api/status
```

### HTTPS through Nginx

After the client trusts the TeamX CA:

```sh
curl https://app.teamX.test:8443/api/status
curl -I https://app.teamX.test:8443/api/status
```

Expect HTTP `200`, `Content-Type: application/json`, `Cache-Control: max-age=60`, and `X-Backend: A` or `B`.

### Load balancing

```sh
for i in {1..10}; do
		printf 'Request %s: ' "$i"
		curl -s -D - https://app.teamX.test:8443/api/status -o /dev/null | grep -i '^X-Backend:'
done
```

With both backends healthy and no other upstream directives, requests use Nginx's default round-robin policy. Concurrent traffic means strict A/B alternation is not guaranteed.

## Security

- Never commit private keys (`*.key`, `*.pem`) or certificate signing requests (`*.csr`).
- Keep the TeamX CA private key on its managing machine.
- Import the local root CA only on lab clients that need to trust this test certificate.

## Repository layout

```text
.
├── .gitignore
├── backend-a/       Backend A source and README
├── backend-b/       Backend B source and README
├── docs/            Topology, request flow, and address guides
├── evidence/        Evidence grouped by networking topic
├── nginx/           Nginx configuration
├── scripts/         Helper script files
└── ssl/             Local certificate material; private keys stay untracked
```
