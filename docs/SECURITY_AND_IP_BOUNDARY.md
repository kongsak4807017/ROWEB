# Security and IP Boundary

## 1. Asset rule

Technical delivery through a browser is still distribution. Production publication requires a valid right to use and distribute the selected assets.

Never commit licensed asset bytes to this repository.

## 2. Prohibited repository content

- GRF archives
- extracted client data
- RSW/GND/GAT/RSM/RSM2/SPR/ACT/PAL/STR
- textures, sprites, minimaps, audio, fonts, and artwork from the game client
- database dumps containing asset payloads or user secrets
- production credentials, certificates, API keys, or passwords

## 3. Allowed repository content

- source code and build scripts
- manifest schemas
- hashes and file sizes
- provenance and compatibility metadata
- synthetic fixtures
- configuration examples with placeholders
- test reports that do not expose restricted payloads

## 4. Asset-server controls

Production asset serving must:

- serve only manifest-published objects
- normalize paths before lookup
- reject traversal and absolute paths
- disable directory listing
- enforce extension/content-size policy
- set safe content types
- rate-limit abuse
- log denied and missing requests
- use immutable content URLs

Avoid a general endpoint such as `GET /asset?path=<arbitrary>` unless it is strictly allowlisted and normalized.

## 5. Web platform controls

- HTTPS and WSS only in production
- Content Security Policy
- restrictive CORS
- no mixed content
- secure cookies for web-account features
- no credentials in frontend bundles
- environment-based endpoint configuration
- dependency and supply-chain scanning

## 6. wsProxy controls

- authenticated/expected upstream destinations only
- packet and frame-size limits
- per-IP/session connection limits
- idle timeout and ping/pong
- backpressure and bounded queues
- graceful drain
- abuse and anomaly metrics

The gateway must not become an open TCP proxy.

## 7. rAthena and database controls

- bind internal services to private interfaces where possible
- firewall login/char/map/database ports
- expose only WSS ingress to players
- dedicated least-privilege database users
- secrets outside Git
- production debug commands disabled or restricted
- audit GM and economy-sensitive actions
- tested backups and restoration

## 8. Player privacy

Collect only operationally necessary telemetry. Document retention for:

- account and authentication logs
- IP/security logs
- gameplay/economy audit logs
- browser performance telemetry
- crash/error reports

Do not place personal data in public GitHub issues or reports.

## 9. Release gate

A release is blocked when:

- asset distribution rights are unresolved
- Git history contains restricted assets or secrets
- production permits arbitrary asset-path retrieval
- wsProxy is exposed as an unrestricted proxy
- HTTP/mixed-content access remains
- backup and credential procedures are undocumented
