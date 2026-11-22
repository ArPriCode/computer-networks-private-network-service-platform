# TeamX Topology

```text
Mac 1 (10.7.15.60)
├── dnsmasq :53
└── Backend A :3001

Mac 2 (10.7.21.116)
├── Nginx HTTPS :8443
└── Backend B :3002

Client
└── app.teamX.test / api.teamX.test
    └── Mac 2
        ├── Backend A
        └── Backend B
```

The Nginx machine is the only public application entry point. Backend ports are direct service ports, not client-facing URLs.
