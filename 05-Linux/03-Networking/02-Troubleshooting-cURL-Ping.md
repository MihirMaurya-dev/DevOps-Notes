---
tags: [linux, networking, troubleshooting, curl, ping, netstat, ss]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Linux Network Troubleshooting

When an application "can't connect to the database" or "the website is down," you must isolate the failure. Is it DNS? Is it a blocked port? Is the service actually listening?

## 1. `ping` (ICMP Testing)
Tests basic Layer 3 (Network Layer) connectivity.
- **Limitation:** Many modern firewalls and Azure NSGs block ICMP by default. A failed ping does NOT mean the server is down.
```bash
ping google.com
ping -c 4 192.168.1.10 # Send exactly 4 packets and stop
```

## 2. `curl` (Layer 7 HTTP Testing)
`curl` is the ultimate tool for testing APIs, web servers, and HTTP connectivity.
- `-I`: Fetch headers only (checks if the server responds without downloading the payload).
- `-v`: Verbose mode. Shows the entire TLS handshake, DNS resolution, and request/response headers. Incredible for debugging SSL certificate issues.
- `-L`: Follow redirects.
- `-k`: Insecure (ignore invalid/self-signed SSL certificates).

**Real-World DevOps Use Cases:**
```bash
# Check if a web server is up and returning HTTP 200 OK
curl -I https://api.contoso.com/healthz

# Debug a TLS/SSL handshake failure
curl -v https://api.contoso.com

# Send a test JSON payload to an API
curl -X POST https://api.contoso.com/users \
     -H "Content-Type: application/json" \
     -d '{"name": "test_user"}'
```

## 3. `telnet` and `nc` (Netcat) - Layer 4 Port Testing
Since `ping` uses ICMP, how do you test if a specific TCP port (like 5432 for PostgreSQL) is open through the firewall?

```bash
# Using telnet
telnet 192.168.1.50 5432
# If it connects, the port is open. If it times out, a firewall is dropping it. If connection refused, nothing is listening.

# Using Netcat (nc) - often preferred over telnet in modern systems
nc -zv 192.168.1.50 5432
# -z = zero I/O mode (just scan, don't send data)
# -v = verbose
```


## 4. `ss` (Socket Statistics)
`ss` is the modern replacement for `netstat`. It shows what ports your server is actually listening on.

```bash
# Show all listening TCP and UDP ports with the process name
sudo ss -tulnp

# Output explanation:
# t = TCP, u = UDP, l = listening, n = numeric (don't resolve IPs to hostnames), p = show process name

# Find out exactly what process is bound to port 8080
sudo ss -tulnp | grep :8080
```

## 5. `dig` and `nslookup` (DNS Testing)
DNS is responsible for 90% of networking issues. "It's always DNS."

```bash
# Query the default DNS server for a domain's A record
dig google.com

# Query a SPECIFIC DNS server (e.g., Google's 8.8.8.8) to bypass local caching
dig google.com @8.8.8.8

# Check the MX (Mail) records
dig mx google.com +short
```

## 6. `traceroute` / `mtr`
Maps the path packets take across the internet to reach a destination.
- `mtr` (My Traceroute) combines `ping` and `traceroute` into a real-time updating interface. Great for identifying exactly which router is dropping packets.
