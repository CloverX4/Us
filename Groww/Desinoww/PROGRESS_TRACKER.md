# 📊 System Design — Progress Tracker

> **Started**: March 21, 2026

---

## 🔥 Stats

| Metric | Value |
|--------|-------|
| **Foundation Topics Covered** | 2 / 8 (APIs & Protocols — in progress) |
| **Scale Journey Stages** | 0 / 4 |
| **Case Studies Completed** | 0 |
| **Teardowns Done** | 0 |
| **"Aha!" Moments** | 36 |

---

## 📝 Session Log

### Phase 1: Building Blocks

#### Session 1 — March 25-26, 2026 | Networking: What Happens When You Type a URL?
- **Topics Covered**: Full request lifecycle (DNS → TCP → TLS → HTTP → Server → Response → Render), DNS caching hierarchy (5 levels), DNS vs CDN, root servers & internet governance, TCP 3-way handshake, TLS handshake & symmetric vs asymmetric crypto, mobile networks, what makes a browser, how to make things faster
- **Starting Knowledge**: Knew DNS and TCP existed, vague on details. Thought DNS was a single server.
- **Aha! Moments**: DNS caching at 5+ levels; only 13 root server addresses power the internet; internet is mostly cables not air; GeoDNS + CDN = location-aware routing; TLS 1.3 saves billions of ms/day at Google scale; 2002 root DNS DDoS — internet survived because of caching
- **Questions Asked**: Excellent curiosity — asked about mobile networks, what makes a browser, CDN vs DNS, root server governance, data through air. Self-aware about knowledge gaps.
- **Confidence After**: 5/10 (first exposure, lots to absorb)
- **Next**: Deeper dive into APIs & Protocols (REST vs GraphQL vs gRPC)

#### Session 2 — March 26, 2026 | Networking Follow-ups: DNS Deep Dive, CDN, Edge Computing, Mobile Networks
- **Topics Covered**: TTL configuration and tradeoffs, DNS prefetching, Akamai, CDN deep dive + GeoDNS, CDN vs P2P, root server 512-byte constraint, TLD management, backwards compatibility, 5G vs WiFi, edge computing, all 13 root server operators (A–M), direct root server querying from terminal, $185K TLD application, .amazon vs South America drama, glue records, full 3-hop DNS chain, **practical networking toolkit** (nslookup types, tracert, ping, ipconfig), DNS record types (A/MX/TXT/NS), DNS resolver comparison (ISP vs Google vs Cloudflare — tested live), ICMP protocol, tracert internals (TTL increment hack), IP TTL vs DNS TTL, OS fingerprinting from TTL, Nmap overview, hiding from tracert (NAT/firewall/VPN), VPN slowness causes, Electron apps
- **Starting Knowledge**: Had questions from Session 1 about CDN, root servers, mobile networks, edge computing
- **Aha! Moments**: 512-byte UDP limit shaped 13 root servers; root servers store ~1500 TLD entries; .io makes millions; TTL is configurable; 5G uses beamforming; edge computing = code at CDN nodes; backwards compatibility = 1980s in 2026; direct root server queries; TLD list is public; $185K TLD fee; 13 roots are replicas; glue records; .amazon 7-year drama; ARPANET origins; tracert = genius TTL increment hack; ICMP is the internet's nervous system; Cloudflare 4x faster than ISP DNS; OS fingerprinting from TTL; VPN + Electron = slowness explained
- **Questions Asked**: Exceptional curiosity — TTL, CDN, root servers, 5G, TLD ownership, root server operators, glue records, .amazon, DNS record types, tracert internals, ICMP, OS fingerprinting, hiding from tracert, VPN slowness, Electron apps, Nmap, DNS resolver speed, DNS over HTTPS
- **Confidence After**: 7/10 (strong DNS understanding, can use networking tools practically, understands packet-level diagnostics)
- **Next**: APIs & Protocols (REST vs GraphQL vs gRPC)

#### Session 3 — April 2, 2026 | APIs & Protocols: What's Under the Hood
- **Topics Covered**: What an API actually is at the network level (HTTP message inside TCP), web servers (Kestrel/.NET — parses HTTP, routes to controllers), web servers across stacks (Go net/http, Node libuv, Python Gunicorn, Java Tomcat), why Kestrel is fast (IO completion ports, Span<T>, pipelines), TechEmpower benchmarks top 10 (Rust dominance), forward proxy vs reverse proxy, Nginx (Engine-X, C10K problem, event-driven), how Nginx serves static files (URL pattern matching), event-driven architecture (single thread not parallel — never idle), load balancing layers (global → cluster → service → app), IIS + Kubernetes ingress in her .NET work setup
- **Starting Knowledge**: Knew APIs as endpoints with docs, used REST at work, didn't know what sat between the internet and her controllers
- **Aha! Moments**: Web server = invisible layer between raw bytes and controllers; Kestrel influenced C# language design (Span<T>); forward proxy protects client, reverse proxy protects server; event-driven ≠ parallel — one thread never idle; load balancing is nested not redundant (4 layers); Nginx error page = proxy alive but app behind it dead; DNS TTL and proxy cache TTL = same concept different layers
- **Questions Asked**: Outstanding Explorer mode — web server internals, how other stacks handle it, what a reverse proxy does, how Nginx serves static files, how single-threaded event loop works, why load balancing seems redundant across layers. Connected IIS + ingress routes from her own work.
- **Confidence After**: 6/10 (strong grasp of layers under APIs, proxy/reverse proxy clicked, event-driven understood. REST/GraphQL/gRPC comparison still pending)
- **Next**: Continue APIs & Protocols — REST (what makes it RESTful), GraphQL, gRPC, when to use which

---

## 🏆 Milestones

- [ ] 🧱 **Foundation Complete** — All 8 building blocks understood
- [ ] 🔭 **Scale Thinker** — Completed the 100 → 100M journey
- [ ] 📐 **First Case Study** — Designed a full system from scratch
- [ ] 🔬 **First Teardown** — Reverse-engineered a real company's architecture
- [ ] 🔧 **Applied to Floww** — Used SD concepts in your own project
- [ ] 🎯 **Interview Ready** — Can lead a 45-min SD discussion confidently

---

*Updated after every session by your mentor (Copilot)*
