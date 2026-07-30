# rAthena Admin Studio M1 Mockup

Dependency-free static prototype of the proposed admin-only rAthena control plane.

## Run locally

```bash
python -m http.server 4173 --directory apps/admin-studio/mockup
```

Open `http://localhost:4173`.

## Included views

- Command Center
- Player Operations
- Economy Studio
- Anti-abuse review
- Audit Ledger
- Typed dry-run command preview

## Safety boundary

All data is synthetic. The mockup contains no API client, WebSocket client, SQL connector, shell command, or raw AtCommand integration. Mutating interactions append only to an in-memory simulated audit ledger.