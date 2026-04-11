# Session 1: What Happens When You Type a URL — Notes

## The Full Journey
```
Browser → DNS lookup → TCP handshake → TLS handshake → HTTP request → Server → Response → Render
```

## DNS (Domain Name System)
- Translates domain names → IP addresses (phone book of the internet)
- NOT a single server — it's a hierarchical system with caching at every level:
  - Browser cache → OS cache → Router cache → ISP resolver → Root/TLD/Auth servers
- Each cache entry has a **TTL** (Time To Live) — configurable by the domain owner
- **GeoDNS**: DNS can return different IPs based on user location → routes to nearest server/CDN
- Low TTL = fast propagation of changes, more lookups. High TTL = fewer lookups, slow to update.

### DNS Hierarchy
```
Root servers (13 addresses, 1700+ physical servers worldwide)
    ↓ "for .com, ask Verisign"
TLD servers (.com, .in, .gov)
    ↓ "for google.com, ask Google's nameserver"
Authoritative servers
    → "google.com = 142.250.193.206"
```
- Root servers managed by ICANN, Verisign, NASA, etc.
- Use **anycast** — same IP, multiple physical locations, traffic routed to nearest

### CDN vs DNS
| | DNS | CDN |
|---|---|---|
| Purpose | Name → IP translation | Content delivery (copies near users) |
| Analogy | Phone book | Library branches |
| Example | Cloudflare DNS, 8.8.8.8 | CloudFront, Akamai |
They work together: GeoDNS routes users to nearest CDN node

## TCP (Transmission Control Protocol) — 3-Way Handshake
```
Client → SYN → Server
Client ← SYN-ACK ← Server
Client → ACK → Server
```
Guarantees reliable, ordered delivery. Both sides confirm they're alive.

## TLS (Transport Layer Security) — Encryption Handshake
```
Client → ClientHello (supported methods, random) → Server
Client ← ServerHello (certificate, chosen method) ← Server
Client → Key Exchange (encrypted pre-master secret) → Server
Both sides now share a symmetric key
```
- Uses asymmetric crypto (slow) ONCE to establish a symmetric key (fast)
- Asymmetric is ~1000x slower than symmetric — so we minimize its use
- TLS 1.3 reduced to 1 round trip (from 2 in TLS 1.2) — Google pushed for this

## HTTP Request/Response
- Browser sends: GET /path, headers (Host, User-Agent, Cookie)
- Server processes: Load balancer → Web server → Cache/DB → Response
- Browser receives: HTML, then fires MORE requests for CSS/JS/images

## Mobile Networks
```
Phone → (radio, 4G/5G) → Cell tower → (fiber) → Carrier network → Internet
```
- Only phone→tower is wireless. After that, it's all cables.
- SIM = authentication with carrier (replaces WiFi password)
- Slower than WiFi: more hops, shared towers, radio interference

## What Makes Something a Browser?
1. Makes HTTP requests (any program can do this — curl, Python requests)
2. Parses HTML/CSS/JS ← THIS is what makes it a browser
3. Renders visually
4. Manages cookies/sessions/cache
At its core, networking = sockets. A browser is a fancy socket client.

## How to Make Things Faster (ranked by impact)
1. CDN — serve static content near users
2. DNS prefetching — resolve before user clicks
3. Connection reuse (HTTP/2 keep-alive) — skip handshakes
4. Server-side caching (Redis) — avoid hitting DB
5. Compression (gzip/brotli) — smaller responses
6. Edge computing — run logic at CDN nodes

## Aha! Moments
- DNS caching exists at 5+ levels — browser, OS, router, ISP, DNS servers
- Only 13 root server addresses power ALL DNS resolution worldwide
- "The internet" is mostly physical cables, not air
- GeoDNS + CDN = different users get different servers based on location
- TLS 1.3 saves 1 round trip — at Google's scale, that's billions of ms/day
- 2002 DDoS hit 9 of 13 root DNS servers — internet survived because of caching

## Questions to Revisit
- How does anycast routing work? → ANSWERED: Same IP, multiple physical servers. BGP routes to nearest. Root DNS uses this — 13 addresses, 1700+ servers.
- What exactly is in an SSL certificate? → Deferred to dedicated TLS/crypto session
- How does HTTP/2 differ from HTTP/1.1? → Future session
- What is edge computing in practice? → ANSWERED: Running code at CDN nodes, not just caching. Cloudflare Workers, Lambda@Edge. <1ms responses possible.
- **TXT records deep dive** → Revisit during TLS/crypto session (SPF, DKIM, domain verification flow)
- **Asymmetric vs symmetric encryption deep dive** → Deferred to dedicated TLS/crypto session (how keys work, RSA, Diffie-Hellman)

## Session 2 Follow-ups (March 26)

### TTL is Configurable
- Set in DNS provider (Cloudflare, Route53, GoDaddy)
- Low TTL (60s) = fast propagation, more lookups. High TTL (86400s) = fewer lookups, slow propagation.
- **Pro move**: Lower TTL before server migration, raise it after.
- Check any site's TTL: `nslookup -type=A google.com`

### DNS Prefetching
- Browser resolves DNS for links on a page BEFORE you click them
- `<link rel="dns-prefetch" href="https://example.com">`
- Saves 20-50ms per click. Google Search does this aggressively.

### Akamai
- One of the oldest/largest CDN companies (1998, MIT origin)
- 365,000+ servers in 135 countries
- Also does DDoS protection, WAF, edge computing

### CDN Deep Dive
- Copies of static content (images, CSS, JS) stored at edge servers worldwide
- GeoDNS routes users to the nearest edge server — same domain, different IPs based on location
- Like mirrors/torrents but managed, automated, and invisible to users
- CDN ≠ peer-to-peer (Apple Find My uses BLE crowd-sourcing — completely different)

### Root Servers — The 13 Myth
- All 13 contain the SAME data (replicas, not categories)
- 13 is a packet size limitation — DNS responses had to fit in 512-byte UDP packets
  - Each root server entry ≈ 32 bytes. 13 × 32 + headers = 512 bytes exactly. 14th wouldn't fit.
  - Not that all 13 respond — the LIST of all 13 had to fit in one response packet
  - Modern EDNS removed the limit, but 13 roots are too deeply baked to change
  - Backwards compatibility shapes everything — can't shut down the internet for an upgrade
- Anycast: 1 IP = hundreds of physical servers, BGP routes to nearest
- Handle ~100 billion queries/day across 1,700+ physical servers
- Root servers store very little — just a lookup table of ~1,500 TLDs:
  ```
  .com → "Ask Verisign at 192.5.6.30"
  .in  → "Ask NIXI at 37.209.192.10"
  .gov → "Ask CISA at 69.36.157.30"
  ```
- TLDs managed by different orgs: .com=Verisign, .in=NIXI (India), .gov=CISA, .io=NIC.io
- Fun fact: .io = British Indian Ocean Territory (pop ~3000) — makes millions from tech startup domain sales
- Full TLD list is public: https://data.iana.org/TLD/tlds-alpha-by-domain.txt (~1,500 TLDs)
- Includes wild ones: .pizza, .ninja, .wtf, .horse + company TLDs: .google, .apple, .amazon
- You can query root servers directly! `nslookup -type=NS com. a.root-servers.net` → returns 13 .com nameservers
- .in handled by trs-dns servers (TRS = The Registry Services, operated by NIXI)

### The 13 Root Server Operators (A–M)
| Server | Operator | Note |
|--------|----------|------|
| A | Verisign | Also runs .com and .net |
| B | USC-ISI (Univ. of Southern California) | Original from 1980s |
| C | Cogent Communications | |
| D | University of Maryland | A university runs critical internet infra |
| E | NASA Ames Research Center | NASA runs a root server |
| F | ISC (Internet Systems Consortium) | Also makes BIND (most popular DNS software) |
| G | US DoD (DISA) | Military |
| H | US Army Research Lab | Two military ones |
| I | Netnod (Sweden) | First non-US operator |
| J | Verisign | They got two |
| K | RIPE NCC (Netherlands) | Europe's internet registry |
| L | ICANN | The governing body itself |
| M | WIDE Project (Japan) | Japanese research org |
- Mostly US military/academic — internet was invented as ARPANET (US military/academic project)
- All 13 hold the SAME ~1,500 TLD→nameserver mappings. Pure replicas, not shards.
- ISP resolver doesn't "choose" — anycast/BGP routing automatically sends to nearest

### Glue Records — Avoiding the Chicken-and-Egg Problem
- Root servers store **nameserver names**, not IPs: `.com → ask a.gtld-servers.net`
- But to reach `a.gtld-servers.net` you'd need DNS... which is what you're trying to do
- Solution: "glue records" — the IP is attached as bonus info in the response
- Full chain for `google.com` (3 hops, cached after first time):
  1. ISP → root: "Who handles .com?" → "a.gtld-servers.net (here's its IP as glue)"
  2. ISP → TLD: "Who handles google.com?" → "ns1.google.com"
  3. ISP → Google's NS: "IP of google.com?" → "142.250.x.x"

### The .amazon Drama
- 2012: Amazon (company) applies for `.amazon` TLD
- Brazil, Peru, South American countries object — "Amazon is our rainforest, our heritage"
- ICANN's GAC initially sided with the countries
- 7 years of dispute processes
- 2019: ICANN approved `.amazon` for the company with conditions
- South American countries called it digital colonialism
- Plot twist: Amazon barely uses `.amazon` — `amazon.com` is too established to change

### Becoming a TLD Manager
- **ccTLDs** (.in, .uk): Country's government decides, IANA/ICANN delegates. Usually national telecom authority.
- **gTLDs** (.pizza, .ninja): ICANN opens application rounds
  - Application fee: $185,000 + annual fees ~$25,000+
  - Need: 24/7 nameserver infrastructure, financial stability, abuse prevention
  - 2012 round: ~1,930 applications → ~1,200 new TLDs
  - Google applied for 101, Amazon for 76
  - .amazon contested by Amazon vs South American countries (took years)
- **Business model**: Charge registrars wholesale per domain
  - Verisign charges ~$8.97/domain/year for .com → makes ~$1.3B/year
  - Registrars (GoDaddy) sell at $10-15 markup

### Mobile vs WiFi Latency
- Both have ~2 hops before internet. Mobile slower because:
  - Radio less reliable than WiFi
  - Tower shared by thousands (router shared by ~10)
  - Carrier has complex routing (auth, billing)
- 5G closing the gap — and sometimes FASTER than WiFi because:
  - Wider frequency bands (400MHz vs WiFi's 20-160MHz)
  - Lower radio latency (~1ms vs WiFi's ~5-10ms)
  - Dedicated licensed spectrum (vs WiFi's shared unlicensed — neighbor's router, microwave interference)
  - Beamforming (signal focused at your phone) + massive MIMO (multiple antennas)
- 5G mmWave: fastest but short range (~500m), can't penetrate walls. Sub-6GHz: farther but slower.
- Find your nearest tower: OpenSignal app, CellMapper, TRAI Tarang Sanchar (India)

### Edge Computing
- Traditional: code runs at origin server (far away)
- Edge: code runs at CDN nodes near the user
- Tools: Cloudflare Workers, Lambda@Edge, Vercel Edge Functions
- Use case: currency conversion, personalization, A/B testing
- Tradeoff: fast but limited resources, data consistency harder, debugging is complex
- Cloudflare Workers: <1ms response possible
- Application to Floww: serve job listings from edge, only hit main server for submissions

### Networking Toolkit — Practical Commands

| Command | What It Does | When to Use |
|---------|-------------|-------------|
| `nslookup domain` | DNS lookup (IP) | "What IP is this domain?" |
| `nslookup -type=MX domain` | Mail server lookup | "Where does email go?" |
| `nslookup -type=TXT domain` | Text records | "What services verified this domain?" |
| `nslookup -type=NS domain` | Nameservers | "Who's the authority for this domain?" |
| `nslookup domain 8.8.8.8` | Query specific DNS | "What does Google DNS say?" |
| `tracert -d domain` | Trace packet path | "What routers do my packets cross?" |
| `ping -n 4 domain` | Latency + alive check | "How fast/alive is this server?" |
| `ipconfig` | Your network config | "What's my IP/gateway/DNS?" |

### DNS Record Types
- **A record**: domain → IPv4 address
- **AAAA record**: domain → IPv6 address
- **MX record**: domain → mail server (how email routing works)
- **TXT record**: arbitrary text — used for domain ownership verification, SPF (email anti-spoofing)
  - SPF (`v=spf1...`): "Only these IPs can send email as @domain" — anti-phishing
  - Verification flow: Service gives random string → you add as TXT record → service queries DNS → verified
  - Deferred: full TXT/SPF/DKIM deep dive in TLS/crypto session
- **NS record**: domain → authoritative nameservers

### DNS Resolver Comparison (tested live)
- ISP resolver: ~321ms 🐌
- Google DNS (8.8.8.8): ~90ms
- Cloudflare DNS (1.1.1.1): ~75ms 🚀
- Free speed boost: change DNS in Windows Settings → Network → DNS → Manual → 1.1.1.1 (preferred), 8.8.8.8 (alternate)
- DNS over HTTPS: encrypts DNS queries so ISP can't see domains you visit (corporate laptops may block this)

### ICMP — The Internet's Nervous System
- Not just tracert — it's the diagnostic protocol:
  - **Ping**: ICMP Echo Request → Echo Reply
  - **Destination Unreachable**: router can't deliver
  - **Time Exceeded**: TTL hit 0 (tracert exploits this!)
  - **Redirect**: "there's a better route"
  - **Path MTU Discovery**: finding max packet size
- Carries error messages and diagnostics, not actual data

### Tracert — How It Actually Works (Genius Hack)
```
Send packet TTL=1 → Router 1 kills it → sends back "I killed it" + its IP
Send packet TTL=2 → Router 1 passes, Router 2 kills → sends back its IP
Send packet TTL=3 → Routers 1,2 pass, Router 3 kills...
...
Send packet TTL=15 → Reaches Google! Normal response.
```
- Deliberately kills packets to map the path — each death reveals a router
- Nobody designed routers for traceroute — it exploited existing TTL death-notification
- `* * *` = routers that don't respond to ICMP (security practice, still forward traffic)
- ISP routers identify tracert by: ICMP protocol type in header + incrementing TTL pattern

### IP TTL — Why Hops Not Seconds?
- DNS TTL = seconds (cache expiry). IP TTL = hop count. Same name, different context.
- Death counter to prevent infinite routing loops:
  - Packet starts TTL=128 → each router decrements by 1 → TTL=0 → packet killed
  - Without TTL, misconfigured loops would flood the network forever
- Originally specified in seconds (1980s), but routers just decrement by 1 — became hop counter in practice
- Default TTL by OS: Windows=128, Linux/Mac=64, some routers=255
  - Different teams, different decades, different choices — no deep technical reason
  - Same physical path regardless — higher TTL just means more hops before death
- **OS fingerprinting**: can guess OS from TTL (near 128=Windows, near 64=Linux/Mac)
  - Nmap uses this + TCP window size, options ordering, fragment handling
  - Nmap appeared in The Matrix Reloaded — Trinity runs real `nmap -v -sS -O` command

### Can You Hide From Tracert?
- **Your router/firewall**: can block ICMP responses (that's what `* * *` routers do)
- **NAT**: home IPs are behind ISP's NAT — outside world sees ISP's IP, not yours
- **VPN**: replaces your IP with VPN server's — tracert shows path from VPN, not you
- You can't hide while SENDING tracert — destination needs your IP to respond

### VPN Slowness — Why Everything Crawls
- **Extra hops**: You → VPN server (maybe another country) → destination → VPN → back
- **Encryption overhead**: every packet encrypted/decrypted — constant CPU work
- **Full tunnel**: most corporate VPNs route ALL traffic through VPN (even Teams, YouTube)
- **Gateway congestion**: thousands of employees funneling through one VPN server
- **Electron apps** (Teams, Postman, VS Code, Discord, Slack): each runs a full Chromium browser instance. 2-4 GB RAM each. They're websites pretending to be desktop apps.
- Network latency adds ~20-50ms/request, but real killer is VPN congestion + Electron bloat

### New Aha! Moments
- TTL is configurable by website owner — real engineering tradeoff
- Akamai has 365K+ servers, born from MIT
- 13 root servers is a 1980s UDP packet size limitation — the LIST of 13 had to fit in one 512-byte response!
- Edge computing = running CODE at CDN nodes, not just caching files
- Cloudflare Workers can respond in <1ms
- 5G can beat WiFi: dedicated spectrum, beamforming, wider bands, ~1ms radio latency
- Backwards compatibility at planetary scale — 1980s constraints still shape 2026 internet
- Root servers store just ~1,500 TLD entries — surprisingly tiny
- .io makes millions for a territory of 3,000 people because Silicon Valley thinks it looks like I/O
- You can directly query root servers from your terminal — that's exactly what ISP resolvers do
- Full TLD list is a plain text file anyone can read (~1,500 entries)
- Becoming a TLD costs $185K application fee — Verisign makes $1.3B/year from .com alone
- All 13 root servers (A–M) are pure replicas — same data, redundancy not sharding
- Glue records solve DNS chicken-and-egg: nameserver IPs attached as bonus info in response
- .amazon TLD took 7 years of legal drama — Amazon barely uses it, amazon.com too established
- Internet governance is mostly US military/academic orgs — ARPANET origins still visible
- Tracert is a genius hack — deliberately kills packets via incrementing TTL to map router path
- ICMP is the internet's nervous system — ping, tracert, errors all use it
- Cloudflare DNS is 4x faster than ISP DNS — free speed boost by changing one setting
- OS fingerprinting from TTL: near 128=Windows, near 64=Linux — Nmap uses this + more
- VPN slowness = extra hops + encryption overhead + gateway congestion + Electron app bloat
- Electron apps (Teams, Postman) = full Chromium instances = websites cosplaying as desktop apps
