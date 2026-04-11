# Session 3: APIs & Protocols — Notes (April 2, 2026)

> Started as "APIs & Protocols" but went deep on the layers UNDER APIs — web servers, reverse proxies, event-driven architecture. This is how Indira learns best: bottom-up through curiosity.

---

## What IS an API at the Network Level?

- An API isn't magic — it's an agreement: "send me THIS HTTP message, I'll send you back THAT HTTP message"
- API documentation = specifying the format of these HTTP messages

### The layers inside a request:
```
TCP packet (the envelope)
  └── HTTP message (the letter inside)
        ├── Request line:    GET /api/users/123 HTTP/1.1
        ├── Headers:         Authorization: Bearer eyJ...
        │                    Content-Type: application/json
        │                    Host: api.groww.in
        └── Body (payload):  {"name": "Indira"} (if POST/PUT)
```

---

## Web Servers — The Layer Between the Internet and Your Code

**What:** Parses raw HTTP bytes into structured objects your code can use. Listens on a port, routes to your controller, serializes responses back to bytes.

**The flow in .NET:**
```
Raw bytes on port
  → Kestrel parses HTTP
    → Routing: [HttpGet("/users/{id}")] matches
      → YOUR controller runs
        → Return value → Kestrel serializes to JSON → HTTP bytes → TCP → client
```

**Kestrel** = .NET's built-in web server. Ships with the SDK. You never install it — it's just there.

`[HttpGet("/users/{id}")]` = instruction TO Kestrel's router. Not the web server itself — it tells the router "when GET /users/* comes in, call this method."

### Web servers across stacks:
```
.NET (C#)     →  Kestrel (built-in)
Node.js       →  libuv + http module (built-in)
Go            →  net/http (built into standard library — no framework needed!)
Java/Spring   →  Tomcat / Jetty / Netty (separate projects, bundled in)
Python/Flask  →  Werkzeug (dev only!) → production needs Gunicorn/uWSGI
Ruby/Rails    →  Puma (separate gem)
```

**Pattern:** Compiled languages (C#, Go, Java) → production-ready web server built in. Interpreted languages (Python, Ruby) → need separate production server because built-in dev servers are single-threaded toys.

### Why Kestrel is fast:
- IO completion ports (Windows kernel's native async I/O — OS tells Kestrel when data arrives, no polling)
- Span<T> / Memory<T> — zero-allocation memory types (Microsoft literally built language features to make Kestrel faster)
- System.IO.Pipelines — reads bytes without copying between buffers
- Kestrel is open source: `dotnet/aspnetcore` → `src/Servers/Kestrel/`

### TechEmpower Benchmarks — Top 10 Web Frameworks (Round 22, JSON serialization):
| Rank | Framework | Language | ~RPS |
|------|-----------|----------|------|
| 1 | drogon | C++ | ~7M+ |
| 2 | may-minihttp | Rust | ~7M |
| 3 | actix | Rust | ~6.8M |
| 4 | ntex | Rust | ~6.7M |
| 5 | xitca-web | Rust | ~6.5M |
| 6 | fasthttp | Go | ~6M |
| 7 | vertx | Java | ~5.5M |
| 8 | asp.net (Kestrel) | C# | ~5M+ |
| 9 | h2o | C | ~5M |
| 10 | gin | Go | ~4.5M |

**Rust takes 4 of top 5.** Matches C++ speed but compiler prevents memory bugs. Python/Ruby? ~50-100K RPS range — 100x slower.

---

## Proxy vs Reverse Proxy

**Proxy = middleman.**

**Forward proxy** — acts on behalf of the CLIENT:
```
Client → [PROXY] → Server
         ↑ hides/protects the client
```
- Privacy/anonymity (VPN = fancy proxy)
- Corporate filtering ("no YouTube at work")
- Geo-restriction bypass (US Netflix from India)
- Caching (500 office users, cache shared resources)

**Reverse proxy** — acts on behalf of the SERVER:
```
Client → [PROXY] → Server
                    ↑ hides/protects the server
```
- SSL/TLS termination (decrypt HTTPS here, plain HTTP internally)
- Static file serving (CSS/JS/images without touching app server)
- Rate limiting (block abusive IPs before they hit your code)
- Load balancing (distribute across multiple app instances)
- DDoS absorption

**Analogy:** Reverse proxy = receptionist at an office. Routes visitors, hands out brochures directly, turns away troublemakers — engineers never bothered unless needed.

### Nginx
- Name = "Engine-X" said fast
- Created 2004 by Igor Sysoev to solve the C10K problem (10K simultaneous connections)
- Apache spawned a thread per connection and choked. Nginx used event-driven architecture.
- That Nginx error page at work = "I (proxy) am alive, but the app behind me is dead"

### How Nginx serves static files:
```nginx
location /static/ {
    root /var/www/yourapp/wwwroot;   # serve directly from disk
}
location / {
    proxy_pass http://localhost:5000; # forward to Kestrel
}
```
URL pattern matching. Static = I got this. API = pass through.

---

## Event-Driven Architecture — How One Thread Handles Thousands

**NOT parallel. Switching really fast. Never waiting.**

Like cooking: instead of watching rice for 20 min, you put rice on, start chopping, oil in pan, respond to whatever finishes first. One person, never idle.

The thread says: "Sent a DB query. Instead of waiting, I'll handle 500 other requests. When DB responds, that's an EVENT — I'll come back."

Works because web servers spend 99% of time **waiting** (DB, disk, network). Actual CPU work (parse JSON, run logic) is tiny.

**Breaks when:** Heavy CPU work (image processing, video encoding) — thread is stuck, everything freezes. That's why Node.js = great for APIs, terrible for video encoding.

---

## Load Balancing Layers — They're Nested, Not Redundant

```
Internet
  ↓
① Azure Front Door / Cloudflare (GLOBAL — which data center?)
  ↓
② Kubernetes Ingress (CLUSTER — which service?)
  ↓
③ Kubernetes Service (SERVICE — which pod?)
  ↓
④ Kestrel (APP — parse HTTP, run code)
```

Like: Country → City → Street → House number. Each narrows the destination further.

**Indira's work setup:** IIS (reverse proxy on each pod) + Kubernetes ingress (routing) + Kestrel (app). Confirmed by launchSettings.json, appsettings.json, ingress route names in config.

---

## Aha! Moments

1. 🧱 **Web server = code that sits between raw TCP bytes and your controllers** — Kestrel parses HTTP into objects, routes to your [HttpGet] method, and reverses the process for responses. You've used it every day without knowing.
2. 🔄 **Forward proxy protects the client, reverse proxy protects the server** — same middleman concept, different direction. VPN = forward proxy. Nginx = reverse proxy.
3. 🧱 **Event-driven ≠ parallel** — one thread, never idle. Works because web servers spend 99% of time waiting on I/O, not computing. Breaks on CPU-heavy work.
4. 🌉 **DNS TTL and proxy cache TTL are the same concept at different layers** — caching with expiry is everywhere in the stack.
5. 🔄 **Load balancing is nested, not redundant** — global (which DC?) → cluster (which service?) → service (which pod?) → app (handle it). Each layer makes a different decision at a different scale.
6. 🧱 **Event notification is push, not poll** — OS kernel uses hardware interrupts to notify apps when I/O completes. IO completion ports (Windows) / epoll (Linux) are the APIs for this. Same as phone buzzing vs checking every 2 seconds.
7. 🧱 **It's dominoes all the way down** — wire has electricity → NIC detects (physics) → NIC writes to ring buffer via DMA (bypasses CPU) → NIC fires hardware interrupt (electrical signal on motherboard pin) → CPU runs interrupt handler → OS notifies app. No polling at any level.
8. 🔧 **NIC hears everything but filters** — on WiFi, your NIC receives ALL packets in range but filters: BSSID match? → MAC match? → Can decrypt? → Only then process. Three filter layers on the NIC's own processor. CPU never sees dropped packets.
9. 🔧 **Promiscuous mode** — tell your NIC to stop filtering, process ALL packets. That's what Wireshark does. Also how WiFi sniffing works (but encrypted payloads still unreadable with WPA2/3).
10. 🧱 **NAPI — adaptive interrupt handling** — at very high traffic, interrupts themselves become overhead. Linux temporarily switches to polling mode ("stop interrupting me, I'll check the buffer myself"), switches back when traffic calms. Best of both worlds.

---

## Event-Driven Notification — How Does the Thread Know?

The OS handles it. Not polling ("done yet?"), but **push notification from hardware**.

```
Kestrel                          OS Kernel                    Network Card
  │                                │                              │
  ├── "query DB, notify me" ──────→│                              │
  ├── handles other requests       │                              │
  │                                │    ←── bytes arrive ─────────┤
  │                                ├── hardware interrupt         │
  │    ←── "here's your data" ─────┤                              │
  ├── continues request #4827      │                              │
```

1. Network card receives bytes → fires **hardware interrupt** (electrical signal to CPU)
2. OS kernel wakes up, finds which app registered for that connection
3. OS puts data in the app's buffer and triggers the **callback**
4. Event loop picks it up and continues the original request

**IO completion ports** (Windows) / **epoll** (Linux) = the OS-level APIs for "notify me when I/O is ready." Push, not poll. Same as your phone buzzing on a message — you don't check every 2 seconds.

---

## Still to Cover (deferred to future sessions)
- REST — what actually makes something RESTful (started exploring, will continue next session)
- GraphQL vs REST vs gRPC comparison
- Threads deep dive (Week 4: Load Balancers)
- Kubernetes infrastructure deep dive (later)
- **How hardware actually works** — interrupts, ports, chips, how CPU/network card/disk communicate at the hardware level (Indira flagged this as a general gap she's curious about)
- Wireshark hands-on session (from SD plan Practical Skills)
- Nmap hands-on session (from SD plan Practical Skills)

---

---

## Follow-up (April 5): Hardware Interrupts, NIC Filtering, Tool Recap

### How event notification works at the hardware level:
- No polling at ANY level — it's reactive dominoes from physics to app
- NIC uses DMA (Direct Memory Access) to write to RAM without bothering CPU
- Hardware interrupt = electrical signal on a physical motherboard pin
- NAPI: Linux adaptively switches to polling at extreme traffic, back to interrupts when calm

### How NIC knows which packets are "mine" (WiFi):
- WiFi NIC receives ALL signals in range
- Filters on NIC's own processor: BSSID → MAC → decryption
- Promiscuous mode (Wireshark) disables this filtering

### Tool disambiguation (all from Sessions 2-3):
| Tool | One-liner |
|------|-----------|
| nslookup | "What's the IP for this domain?" (DNS lookup) |
| ping | "Is this host alive? How fast?" (latency) |
| tracert | "What's the path from me to there?" (hop-by-hop map) |
| ipconfig | "What's MY network config?" (local info) |
| nmap | "What's running on that host?" (port scan, OS detection — active probe) |
| wireshark | "What's flowing through my NIC right now?" (packet capture — passive observation) |

*Session went deep on layers under APIs rather than API styles — bottom-up exploration through .NET stack curiosity. REST/GraphQL/gRPC comparison continues next session.*
