---
tags: [architecture, patterns, multi-region, global]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Architecture Pattern: Multi-Region Deployment

A Multi-Region architecture involves deploying identical or complementary application stacks in more than one Azure Region (e.g., East US and West Europe).

## Why Multi-Region?
1. **High Availability / Disaster Recovery:** If an entire Azure region goes offline due to a natural disaster or massive outage, the application continues to run from the secondary region.
2. **Latency / User Experience:** Serving a user in London from a datacenter in London is much faster than serving them from a datacenter in New York.
3. **Data Sovereignty:** Legal requirements might dictate that European customer data stays in Europe, while US customer data stays in the US.

## Implementation Strategies

### Active-Active vs Active-Passive Decision Matrix

| Characteristic | Active-Active | Active-Passive (Warm Standby) | Pilot Light (Cold) |
|----------------|---------------|-------------------------------|--------------------|
| **Description** | Traffic split across both regions simultaneously. | Primary region handles 100% traffic. Secondary takes over on failure. | Secondary has data but minimal/no compute running until failure. |
| **RTO/RPO** | Near Zero / Near Zero | Minutes / Minutes | Hours / Hours |
| **Cost** | Highest (2x full capacity) | High (Compute runs at lower scale) | Lowest (Only paying for storage) |
| **Complexity**| Highest (Data collision management) | Medium (Failover orchestration) | Low |
| **Use Case** | Global financial platforms, e-commerce | Standard enterprise apps | Back-office tools, batch processing |

## Global Traffic Routing

To route traffic to the correct region, you need a service that lives *outside* of a specific Azure region.

- **Azure Front Door (Layer 7):** Best for HTTP/HTTPS web applications. It uses Microsoft's global edge network (Anycast) to route users to the lowest-latency backend. It also includes CDN caching and Web Application Firewall (WAF) capabilities.
- **Azure Traffic Manager (DNS-based):** Best for non-HTTP traffic (e.g., UDP/TCP gaming servers) or hybrid scenarios. It returns the IP address of the target region based on DNS queries (Priority, Weighted, Performance routing methods).

## Data Replication and Consistency

Keeping data in sync across regions is the hardest part of multi-region design. You must choose between eventual and strong consistency.

### 1. Azure Cosmos DB (NoSQL)
The gold standard for multi-region apps.
- Supports **Multi-Master (Active-Active)** writes, meaning instances in both US and Europe can write data simultaneously.
- You can tune consistency levels (Strong, Bounded Staleness, Session, Consistent Prefix, Eventual) to trade off latency vs. absolute data correctness.

### 2. Azure SQL Database (Relational)
- Uses **Active Geo-Replication**. The primary region handles all writes. The secondary region is a readable replica.
- **Failover:** In a disaster, you initiate a failover. The secondary database becomes the primary writable database. 
- **Auto-failover groups:** Provide a single endpoint string for the application. If a failover occurs, the endpoint automatically points to the new primary, requiring no code changes.

### 3. Azure Storage
- Use **GRS (Geo-Redundant Storage)** or **GZRS (Geo-Zone-Redundant Storage)**.
- Data is written synchronously in the primary region (LRS/ZRS), and then asynchronously copied to the paired region.
- Note: The secondary region is read-only (if RA-GRS is enabled) until a formal storage account failover is initiated by the administrator.

## Global Networking (vWAN)
When scaling multi-region hub-and-spoke networks, managing global VNet peering becomes complex.
- **Azure Virtual WAN (vWAN)** provides a managed global transit architecture.
- You deploy a Virtual Hub in Region A and another Virtual Hub in Region B.
- Because they are in the same vWAN, Azure automatically establishes a high-speed, any-to-any global mesh across the Microsoft backbone, allowing Spokes in Region A to talk to Spokes in Region B effortlessly.
