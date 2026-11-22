# IP Addresses and Ports

| Component | Address | Port |
|---|---|---:|
| Mac 1 / DNS / Backend A | `10.7.15.60` | `53`, `3001` |
| Mac 2 / Nginx / Backend B | `10.7.21.116` | `8443`, `3002` |
| Private application names | `app.teamX.test`, `api.teamX.test` | resolves to Mac 2 |

These DHCP addresses are examples for the current LAN. Recheck `ifconfig en0` and update `config/dnsmasq/dnsmasq.conf`, `nginx/nginx.conf`, and this table after an address change.
