# IP Addresses and Ports

These are the addresses currently hard-coded in the project. They describe the lab's present configuration and may need to be replaced on another network.

| Component | Address | Port | Configured in |
| --- | --- | ---: | --- |
| Backend A | `10.7.6.85` | `3001` | `backend-a/server.py`, `nginx/nginx.conf` |
| Backend B | `10.7.0.248` | `3002` | `backend-b/server.py`, `nginx/nginx.conf` |
| Nginx HTTPS virtual host | `app.team1.test` | `443` | `nginx/nginx.conf` |

Both backend servers bind to `0.0.0.0`, so they accept connections on their host interfaces. Nginx must be able to reach each backend address and port. The client must resolve `app.team1.test` to the Nginx host.

The startup messages in each backend print the current LAN URL. Recheck those values when the host network changes, and update the Nginx upstream addresses to match.
