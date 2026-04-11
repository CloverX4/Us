# 🏗️ System Design — Learning Plan (Evergreen)

> **Start Date**: March 21, 2026
> **Pace**: 1-2 sessions/week alongside DSA
> **Philosophy**: Not interview prep. Genuine understanding. Build the instinct to design systems that work in the real world.
> **Goal**: Be the person in the room who UNDERSTANDS why things are built the way they are — not just someone who memorized "use Redis for caching."

---

## 🧬 How This Plan Works

Unlike DSA (which has a clear 2-month end date), this plan is **evergreen**. System design knowledge compounds forever. The plan has phases, but you'll keep adding case studies and teardowns indefinitely.

**Each session is one of:**
- 🧱 **Foundation** — learn a building block (database, cache, queue, etc.)
- 🔭 **Scale Journey** — take a system from 100 → 100M users
- 📐 **Case Study** — design a real system from scratch
- 🔬 **Teardown** — reverse-engineer how a real company built something
- 🔧 **Apply** — use what you learned in your own projects (Floww)

---

## 📈 Phase Overview

| Phase | Focus | Duration | Goal |
|-------|-------|----------|------|
| **Phase 1: Building Blocks** | Foundations — the components every system uses | 3-4 weeks | Understand each piece independently |
| **Phase 2: Scale Thinking** | The 100 → 100M user journey | 2-3 weeks | Learn WHEN and WHY to add complexity |
| **Phase 3: Case Studies** | Design real systems from scratch | Ongoing | Apply building blocks to real problems |
| **Phase 4: Deep Dives** | HLD + LLD on complex systems | Ongoing | Go deep on the hard parts |
| **Phase 5: Teardowns** | Reverse-engineer real architectures | Ongoing | Learn from the best (and their mistakes) |

---

## 🔥 Phase 1: Building Blocks (Weeks 1-4)

> The alphabet before the words. You can't design systems if you don't know the pieces.

### Week 1: How the Internet Actually Works
| Session | Topic | Key Questions |
|---------|-------|--------------|
| 1 | **Client → Server: The Full Journey** | What happens when you type a URL? DNS, TCP, HTTP, TLS — the full stack |
| 2 | **APIs & Protocols** | REST vs GraphQL vs gRPC. When to use which? What even IS an API at the network level? |

### Week 2: Databases — The Heart of Every System
| Session | Topic | Key Questions |
|---------|-------|--------------|
| 3 | **SQL vs NoSQL — The Real Tradeoffs** | It's not "SQL is old, NoSQL is new." When does each shine? What's ACID? What's BASE? |
| 4 | **Indexing, Sharding, Replication** | How does a database handle 1M reads/sec? How do you split data across machines? What breaks? |

### Week 3: The Speed Layer
| Session | Topic | Key Questions |
|---------|-------|--------------|
| 5 | **Caching — The Art of Remembering** | Cache invalidation is one of the hardest problems in CS. Why? What's an LRU cache? Where do you put caches? |
| 6 | **CDNs & Edge Computing** | How does Netflix stream HD video to 200 countries with low latency? What's "the edge"? |

### Week 4: The Glue
| Session | Topic | Key Questions |
|---------|-------|--------------|
| 7 | **Load Balancers & Reverse Proxies** | How do you distribute 100K requests/sec across 50 servers? What's consistent hashing? |
| 8 | **Message Queues & Event-Driven Architecture** | Kafka, RabbitMQ, SQS — why do we need queues? What's pub/sub? When does synchronous break? |

---

## 🔭 Phase 2: The Scale Journey (Weeks 5-7)

> This is the core insight: **systems evolve, they aren't designed once.**

| Session | Scale | What We Design | What Breaks | What We Add |
|---------|-------|----------------|-------------|------------|
| 9 | **100 users** | Single server, single DB, monolith | Nothing yet — don't over-engineer! | Just deploy and ship |
| 10 | **10K users** | First growing pains | DB reads slow, single server maxed | Read replicas, basic caching, horizontal scaling |
| 11 | **1M users** | Real scale problems | Write bottlenecks, global latency, data consistency | Sharding, CDN, message queues, microservices (maybe) |
| 12 | **100M users** | Planet-scale challenges | Network partitions, data center failures, regulatory (GDPR) | Multi-region, eventual consistency, chaos engineering |

---

## 📐 Phase 3: Case Studies (Week 8+, Ongoing)

> Design systems from scratch. Each one teaches different patterns.

### Starter Case Studies (ordered by complexity of new concepts introduced)
| # | System | Key Patterns Learned |
|---|--------|---------------------|
| 1 | **URL Shortener** | Hashing, base conversion, read-heavy optimization, caching |
| 2 | **Paste Bin / Notes App** | Object storage, metadata vs content separation, TTL |
| 3 | **Rate Limiter** | Sliding window (hey, DSA crossover!), token bucket, distributed counting |
| 4 | **Chat System (WhatsApp)** | WebSockets, presence, message ordering, fanout |
| 5 | **News Feed (Instagram/Twitter)** | Fan-out on write vs read, ranking, caching timelines |
| 6 | **Notification System** | Priority queues, delivery guarantees, multi-channel (push, email, SMS) |
| 7 | **Search Autocomplete** | Tries (DSA crossover!), prefix matching at scale, caching popular queries |
| 8 | **Video Streaming (YouTube/Netflix)** | Chunked upload, transcoding, adaptive bitrate, CDN |
| 9 | **Ride Sharing (Uber)** | Geospatial indexing, real-time matching, ETA estimation, surge pricing |
| 10 | **Distributed File System (Google Drive)** | Chunking, deduplication, conflict resolution, sync |

### Advanced Case Studies (added as we go)
- Payment System (Stripe)
- E-commerce (Amazon — order management, inventory)
- Recommendation Engine (Spotify/Netflix)
- Distributed Task Scheduler
- Real-time Collaboration (Google Docs)
- Ad Serving System
- Monitoring & Alerting System

---

## 🛠️ Bonus: Practical Skills Sessions (Interspersed)

> Not strictly SD, but deeply connected. Hands-on networking/security skills that make you dangerous.

| # | Topic | Key Skills |
|---|-------|-----------|
| 1 | **Nmap & Network Reconnaissance** | Port scanning, OS fingerprinting, service detection, NSE scripts, practical security auditing |
| 2 | **Wireshark & Packet Analysis** | See TCP/TLS/HTTP at packet level, debug real traffic, understand what's on the wire |

*Schedule these when they connect naturally to what we're learning.*

---

## 🔬 Phase 4: Deep Dives (Interspersed)

### HLD Topics
- Microservices vs Monolith — the real decision framework
- API Gateway patterns
- Service mesh and service discovery
- Circuit breakers and resilience patterns
- Data pipelines (ETL, streaming)
- Event sourcing and CQRS

### LLD Topics
- API contract design (OpenAPI, versioning)
- Data modeling (schema design for different use cases)
- Class design for real systems (rate limiter, LRU cache, connection pool)
- Concurrency patterns (thread pools, async, actors)

---

## 🔍 Phase 5: Real-World Teardowns (Ongoing)

> Learn from the masters. Read their engineering blogs. Understand their decisions.

### Teardown Queue (added over time)
| Company | System | Source |
|---------|--------|--------|
| Netflix | Chaos Engineering & Resilience | Netflix Tech Blog |
| Uber | Real-time Marketplace Architecture | Uber Engineering |
| Slack | Message Storage Redesign | Slack Engineering |
| Discord | How they store billions of messages | Discord Blog |
| Instagram | Scaling to 1B+ users | IG Engineering |
| Stripe | Distributed Payment Processing | Stripe Blog |
| GitHub | The 24-hour incident (2018) | GitHub Post-mortem |

---

## 🎯 How Sessions Integrate with DSA

| Day | Activity |
|-----|----------|
| Mon-Fri (4-5 days) | DSA (Algoww) |
| Sat or Sun (1-2 sessions) | System Design (Desinoww) |
| Overlap moments | When DSA topic connects to SD (tries → autocomplete, heaps → scheduling), discuss it |

This isn't rigid — some weeks you'll feel like more SD, some weeks more DSA. The split can flex as long as DSA stays primary during the 2-month plan.

---

## 📊 Confidence Tracker

| Topic | Confidence | Last Reviewed |
|-------|-----------|---------------|
| Networking & HTTP | — | — |
| Databases (SQL) | — | — |
| Databases (NoSQL) | — | — |
| Caching | — | — |
| Load Balancing | — | — |
| Message Queues | — | — |
| CDNs | — | — |
| Storage Systems | — | — |
| Microservices | — | — |
| API Design | — | — |
| Scaling Patterns | — | — |
| Failure & Resilience | — | — |
| Data Modeling | — | — |
| Monitoring | — | — |

---

## 💡 "Aha!" Moments Journal

> The moments that changed how you think about systems

*(populated as we learn)*

---

*Created: March 21, 2026 — v1 (Evergreen, will keep growing)*
