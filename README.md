# Computer Networks Private Network Service Platform

<div align="center">

[![Course](https://img.shields.io/badge/Course-Computer_Networks-blue?style=for-the-badge)](#)
[![Team](https://img.shields.io/badge/Team-StackHackers-0f766e?style=for-the-badge)](#team)
[![Architecture](https://img.shields.io/badge/Architecture-Two_Mac_LAN-orange?style=for-the-badge)](#architecture)
[![Status](https://img.shields.io/badge/Status-Phase_1_%26_2_Complete-success?style=for-the-badge)](#project-status)

</div>

**Private DNS + HTTPS Reverse Proxy + Load Balancing + Service Resilience**

This repository contains StackHackers' implementation of a fully local private networking platform. It demonstrates how a browser request travels through DNS, TCP, TLS, HTTP, Nginx load balancing, and two independent backend services across two macOS machines.

> [!IMPORTANT]
> This project is intentionally local. No cloud server or public hosting is used. The target private domain is `teamX.test`, and all live services are reachable only on the team's private LAN.

---

## Project Status

| Phase | Status | Outcome |
| --- | --- | --- |
| **Phase 1 - Build & Observe** | ✅ Complete | Private DNS, both backends, Nginx HTTPS, load balancing, caching, and protocol evidence |
| **Phase 2 - Harden & Recover** | ✅ Complete | DNS resilience, TTL behavior, service isolation, backend failover, and edge-migration design |

The repository contains configuration, source code, scripts, screenshots, and packet evidence for the complete project.

---

## Team

| Member | Roll number |
| --- | --- |
| Arun Kumar Giri | `2401010099` |
| Gaurav Meena | `2401010169` |
| Ritik Ranjan | `2401010388` |

---

## Architecture

### Two-Mac Deployment

| Machine | Role | LAN address | Services |
| --- | --- | --- | --- |
| **Mac 1** | DNS + Backend A | `10.7.15.60` | dnsmasq `:53`, Backend A `:3001` |
| **Mac 2** | Edge + Backend B | `10.7.21.116` | Nginx `:8443`, Backend B `:3002` |

> DHCP addresses may change. Verify both Macs with `ifconfig en0` and update the DNS and Nginx upstream configuration before deployment.

### Request Journey

```text
Browser / curl
      |
      | 1. DNS query for app.teamX.test
      v
Mac 1 - dnsmasq :53
      |
      | 2. Returns Mac 2 address: 10.7.21.116
      v
Mac 2 - Nginx :8443
      |
      | 3. TLS terminates
      | 4. Round-robin HTTP proxy
      +--------------------> Backend A :3001
      |
      +--------------------> Backend B :3002
      |
      v
JSON response + X-Backend header
```

| Hostname | DNS answer | Service |
| --- | --- | --- |
| `app.teamX.test` | `10.7.21.116` | Mac 2 Nginx |
| `api.teamX.test` | `10.7.21.116` | Mac 2 Nginx |

More detail:

- [Network topology](docs1/topology.md)
- [IP addresses and ports](docs1/ip-addresses.md)
- [Request flow](docs1/request-flow.md)
- [Phase 1 documentation](docs1/README.md)

---

## Protocol Stack Demonstration

| Layer | Technology | What it proves |
| --- | --- | --- |
| DNS | dnsmasq | Resolves private names to the edge server |
| TCP | macOS networking | Opens a reliable connection to service ports |
| TLS | OpenSSL + Nginx | Encrypts traffic and verifies the TeamX certificate |
| HTTP | Python backend servers | Exposes JSON endpoints and response headers |
| Load balancing | Nginx upstream | Distributes requests across both backends |
| Caching | `Cache-Control`, `ETag` | Supports fresh responses and `304 Not Modified` |
| Resilience | Nginx failover | Tries another backend when one upstream fails |

---

## Backend API

Both backends expose the same contract:

| Method | Endpoint | Response |
| --- | --- | --- |
| `GET` | `/` | Identifies the backend and its running message |
| `GET` | `/api/status` | Returns backend status and server identity |
| `HEAD` | `/` or `/api/status` | Returns headers only |

Example:

```json
{
  "backend": "A",
  "status": "ok",
  "server": "Backend A"
}
```

Every successful response includes:

```text
Content-Type: application/json
Cache-Control: max-age=60
X-Backend: A | B
ETag: "<content hash>"
```

Backend documentation:

- [Backend A setup](backend-a/README.md)
- [Backend B setup](backend-b/README.md)

---

## TLS and Certificate Trust

Nginx terminates HTTPS on port `8443`.

| Certificate item | Target |
| --- | --- |
| Local root CA | StackHackers TeamX root CA |
| Server certificate | SAN certificate for both TeamX hostnames |
| SAN entries | `DNS:app.teamX.test`, `DNS:api.teamX.test` |
| Client trust | Import the root CA into the macOS Keychain |

Generate the certificate and private key on the designated machine:

```sh
./scripts/generate-certificate.sh
```

Never commit private keys or certificate signing requests.

---

## Phase 1 Evidence

<table>
  <tr>
    <td width="50%" align="center">
      <strong>Terminal evidence 1</strong><br>
      <img src="docs1/terminal_photo/Screenshot%202026-11-22%20at%2022.02.25.png" alt="Terminal evidence 1">
    </td>
    <td width="50%" align="center">
      <strong>Terminal evidence 2</strong><br>
      <img src="docs1/terminal_photo/Screenshot%202026-11-22%20at%2022.02.31.png" alt="Terminal evidence 2">
    </td>
  </tr>
  <tr>
    <td width="50%" align="center">
      <strong>Terminal evidence 3</strong><br>
      <img src="docs1/terminal_photo/Screenshot%202026-11-22%20at%2022.02.40.png" alt="Terminal evidence 3">
    </td>
    <td width="50%" align="center">
      <strong>Terminal evidence 4</strong><br>
      <img src="docs1/terminal_photo/Screenshot%202026-11-22%20at%2022.02.54.png" alt="Terminal evidence 4">
    </td>
  </tr>
</table>

The remaining screenshots and packet evidence are stored in [docs1/terminal_photo](docs1/terminal_photo). The packet capture is in [captures/phase1-mac1.pcap](captures/phase1-mac1.pcap).

---

## Setup

### 1. Install dependencies

Both Macs:

```sh
brew install python
```

Mac 1:

```sh
brew install dnsmasq
```

Mac 2:

```sh
brew install nginx
```

### 2. Start Backend A

On Mac 1:

```sh
cd backend-a
python3 server.py
```

### 3. Start dnsmasq

On Mac 1:

```conf
listen-address=127.0.0.1,10.7.15.60
address=/app.teamX.test/10.7.21.116
address=/api.teamX.test/10.7.21.116
local-ttl=30
```

```sh
sudo brew services start dnsmasq
dig @10.7.15.60 app.teamX.test
```

### 4. Configure and start Nginx

On Mac 2:

```sh
nginx -t
brew services start nginx
```

Start Backend B:

```sh
cd backend-b
python3 server.py
```

### 5. Configure the client DNS server

On each client Mac:

```sh
sudo networksetup -setdnsservers "Wi-Fi" 10.7.15.60
sudo dscacheutil -flushcache
sudo killall -HUP mDNSResponder
networksetup -getdnsservers "Wi-Fi"
```

---

## Verification

### DNS resolution

```sh
dig @10.7.15.60 app.teamX.test
dig @10.7.15.60 api.teamX.test
dig app.teamX.test
```

### Direct backend checks

```sh
curl -i http://10.7.15.60:3001/
curl -i http://10.7.21.116:3002/
curl -I http://10.7.15.60:3001/api/status
curl -I http://10.7.21.116:3002/api/status
```

### HTTPS and load balancing

```sh
curl -i https://app.teamX.test:8443/api/status
./scripts/test-load-balancer.sh
```

Expected result:

- HTTP `200 OK`
- `X-Backend: A` or `X-Backend: B`
- `Cache-Control: max-age=60`
- `Content-Type: application/json`

### Conditional caching

```sh
curl -I https://app.teamX.test:8443/api/status
curl -i -H 'If-None-Match: "<etag>"' \
  https://app.teamX.test:8443/api/status
```

If the entity has not changed, the backend may return `304 Not Modified`.

### Network helper

```sh
./scripts/network-info.sh
```

---

## Phase 2 Resilience

The target design adds:

- A second DNS resolver
- Primary and backup DNS configuration
- Short DNS TTL values
- Backend firewall isolation
- Nginx upstream health failover
- Controlled DNS-based edge migration
- Faculty-injected troubleshooting

Failure behavior:

| Failure | Expected observation |
| --- | --- |
| Backend A stopped | Nginx continues serving through Backend B |
| Both backends stopped | DNS and TLS still resolve, application returns `502 Bad Gateway` |
| Primary DNS stopped | Clients with the backup resolver still resolve names |
| Wrong DNS server | Name resolution fails despite direct IP connectivity |
| Wrong destination port | Host is reachable but the TCP service port is unavailable |

---

## Repository Layout

```text
.
├── README.md
├── backend-a/               Backend A Python service
├── backend-b/               Backend B Python service
├── backend-phase-1/         Phase 1 source snapshots
├── backend-phase-2/         Phase 2 source snapshots
├── captures/                Packet capture evidence
├── config/
│   ├── dnsmasq/             dnsmasq configuration
│   └── ssl/                 Public CA material
├── docs/                    Architecture documentation
├── docs1/                   Phase 1 evidence and photographs
├── nginx/                   Nginx load-balancer configuration
├── scripts/                 Setup and verification scripts
└── ssl/                     Local certificate material
```

---

## Project Resources

- [Project report / documentation PDF](CN_Documentation.pdf)
- [Raw project documentation PDF](https://raw.githubusercontent.com/ArPriCode/computer-networks-private-network-service-platform/main/CN_Documentation.pdf)
- [Project explanation video](https://www.youtube.com/watch?v=bXZ1VpMZV8c)
- [GitHub repository](https://github.com/ArPriCode/computer-networks-private-network-service-platform)

---

## Security

- Never commit private keys, CSRs, or certificate serial files.
- Keep the TeamX CA private key with the certificate administrator.
- Restrict backend ports to the Nginx host when demonstrating service isolation.
- Restore original firewall rules after every failure demonstration.
