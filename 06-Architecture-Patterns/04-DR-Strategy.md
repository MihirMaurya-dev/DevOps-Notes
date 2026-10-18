---
tags: [architecture, patterns, dr, disaster-recovery]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# 🆘 Disaster Recovery (DR) Strategy — Complete Guide in Simple Language

---

## 🤔 What is Disaster Recovery?

Imagine you're running a busy online bank. Suddenly, the entire datacenter in East US catches fire. Everything is gone — servers, databases, everything.

**Disaster Recovery (DR)** is the plan you have *before* that disaster happens, so your bank can keep running from a different location (West Europe) with minimal data loss and downtime.

> 🧠 **In simple words:** DR is your emergency backup plan for when an entire Azure Region goes down. It's not about a single VM failing (that's High Availability). It's about an entire city-level event.

**The difference between High Availability and Disaster Recovery:**
| Concept | Protects Against | Example |
|--------------------------|-----------------------------|----------------------------------------------------|
| **High Availability (HA)** | Single component failure | One VM crashes → another VM takes over (same region) |
| **Disaster Recovery (DR)** | Entire region failure | East US datacenter goes offline → West Europe takes over |

---
## 📏 The Two Critical DR Metrics (You MUST Know These)

These two numbers define everything about your DR strategy. **Every business decision, every cost decision, flows from these two numbers.**

### 🔵 RPO — Recovery Point Objective: "How much data can I lose?"

**Analogy:** Think of RPO like how often you save your Word document. If your laptop crashes and your last save was 2 hours ago, you lose 2 hours of work. That's your RPO.

- **RPO = 0:** Every single transaction is replicated in real-time. If a disaster happens at 3:47:23 PM, you resume from 3:47:23 PM. No data lost.
- **RPO = 15 minutes:** Your last backup was 15 minutes ago. You lose at most 15 minutes of data.
- **RPO = 24 hours:** You backup once a day at midnight. If a disaster happens at 11:59 PM, you lose nearly 24 hours of data.

**Who sets RPO?** The **business**, not IT. A bank might say: "We cannot lose any transaction data. RPO = 0." An internal HR system might say: "Losing up to 4 hours of data is acceptable. RPO = 4 hours."

### 🔴 RTO — Recovery Time Objective: "How long can we be down?"

**Analogy:** If your car breaks down, RTO is how long you're willing to wait for a replacement car before you miss your appointment. If you have a critical meeting in 30 minutes, your RTO is 30 minutes.

- **RTO = 0 minutes:** The system switches over instantly. Users experience no downtime.
- **RTO = 1 hour:** The business can tolerate being down for 1 hour while you restore the system.
- **RTO = 8 hours:** Normal business hours. "We'll be back up by morning."

**The rule:** RPO and RTO are **independent** — there's no formula linking them. A system could have RPO=0 (no data loss) but RTO=1 hour (takes time to switch over). Or RPO=4 hours but RTO=5 minutes.

**The other rule:** Lower RPO and RTO = More expensive. A system with RPO=0 and RTO=0 requires massive infrastructure running 24/7 in two regions simultaneously.

---

## 🏗️ The 3 DR Deployment Strategies

### 1. ☀️ Active / Active (Hot Standby) — "Two fully running systems"

**Analogy:** You have two restaurant locations. Both are fully open, serving customers every day. If Location 1 burns down, Location 2 simply handles all the customers. No closure needed.

**How it works in Azure:**
- Your application runs **simultaneously** in TWO Azure regions (e.g., East US + West Europe)
- Azure Front Door (or Traffic Manager) splits traffic between both — e.g., 50%/50%, or routes users to their closest region
- Both databases are writable and actively synced (e.g., Cosmos DB with multi-master)
- If East US fails, Front Door automatically routes 100% to West Europe

```
Normal operation:       
  US Users → East US (50% traffic)    ← Both regions live
  EU Users → West Europe (50% traffic)

During East US failure:
  All Users → West Europe (100%) ← Automatic failover
```

**RTO:** Near-zero (seconds, not minutes — just DNS propagation)  
**RPO:** Near-zero (data is replicated synchronously or near-synchronously)  
**Cost:** $$$$ 
$ — You pay for full infrastructure in TWO regions permanently  
**Complexity:** Highest — database conflict resolution, session management across regions

**Best for:** Banking, payments, trading platforms, healthcare systems where any downtime = direct financial/legal consequences.

---

### 2. 🌤️ Active / Passive (Warm Standby) — "One runs, one idles"

**Analogy:** You have one restaurant that's fully open, and a second restaurant that's partially set up (kitchen ready, some staff on standby) but serving no customers. If Restaurant 1 closes, you open Restaurant 2 in minutes.

**How it works in Azure:**
- **Primary region (Active):** Full production environment running at full scale
- **Secondary region (Passive/Warm):** The same infrastructure exists but running at **reduced scale** (e.g., minimum nodes, smaller VMs)
- The database replicates continuously from primary to secondary (read-only replica)
- If primary fails: scale up secondary, update DNS/Front Door to point there

```
Normal operation:
  Primary (East US):   Full capacity — 10 nodes, large VMs ← All traffic
  Secondary (West EU): Minimal capacity — 2 nodes, small VMs ← No traffic, just waiting

During East US failure:
  Secondary scales up to full capacity (takes ~5-10 minutes)
  DNS/Front Door switches → West EU now handles all traffic
```

**RTO:** Minutes (5-15 minutes — time to scale up + DNS propagation)  
**RPO:** Minutes (how far behind the read replica is from the primary)  
**Cost:** $$$ — You pay for minimal infrastructure in the secondary region  
**Complexity:** Medium — failover orchestration, potential for some data lag

**Best for:** Standard enterprise applications, internal business systems, non-real-time customer-facing apps.

---

### 3. 🌙 Pilot Light / Cold Standby — "Data only, no compute"

**Analogy:** A pilot light is the small, constantly burning flame in your gas stove that can ignite the full burner when needed. You're not burning a full burner 24/7 — just keeping the flame alive.

**How it works in Azure:**
- **Primary region:** Full production environment
- **Secondary region:** **ONLY the data** is maintained (database geo-replication, storage replication). No compute (VMs, AKS) is running.
- If primary fails: Use Terraform/Bicep to spin up all the infrastructure in the secondary region from scratch, then connect it to the replicated data.

```
Normal operation:
  Primary (East US):   Full stack running (VMs, AKS, databases, everything)
  Secondary (West EU): Only databases and storage are being replicated. Nothing else.

During East US failure:
  1. Trigger Terraform to deploy VMs/AKS/App Gateway in West EU (from existing IaC)
  2. Point the new infrastructure to the replicated database
  3. Update DNS to West EU
  4. Total time: 1-4 hours
```

**RTO:** Hours (time to provision infrastructure from scratch + DNS)  
**RPO:** Hours (depends on replication frequency)  
**Cost:** $ — Only paying for data storage/replication. Minimal compute cost.  
**Complexity:** Low — but the RTO is very high

**Best for:** Non-critical internal tools, batch processing systems, development/test environments, reporting databases where an 8-hour outage is acceptable.

---

## 📊 Strategy Comparison Table

| Strategy | RTO | RPO | Cost | Best For |
|----------|-----|-----|------|----------|
| **Active/Active** | Near-zero (~seconds) | Near-zero | $$$$$ | Banking, payments, critical e-commerce |
| **Active/Passive (Warm)** | Minutes (5-15 min) | Minutes | $$$ | Standard enterprise apps |
| **Pilot Light (Cold)** | Hours (1-4 hours) | Hours | $ | Internal tools, batch systems |

---

## ☁️ Azure Services for DR

### For Compute (VMs and AKS)
- **Azure Site Recovery (ASR):** Replicates entire VMs to a secondary region. Can fail over with a single click. RTO of ~15-30 minutes.
- **Terraform/Bicep (IaC):** For Pilot Light scenarios — store all infrastructure as code so you can recreate it in any region in minutes.

### For Databases
| Database | DR Feature | Notes |
|----------|------------|-------|
| **Azure SQL Database** | Active Geo-Replication + Auto-failover Groups | Creates a readable secondary in another region. Auto-failover group gives one connection string that always points to current primary. |
| **Cosmos DB** | Multi-region writes (Active/Active) | Best-in-class for multi-region. Set RPO=0 with strong consistency. |
| **Azure PostgreSQL Flexible** | Geo-redundant backup + Read Replica | For warm standby scenarios |
| **Azure Redis Cache** | Geo-replication (active/passive) | Session state survives regional failover |

### For Routing Traffic
- **Azure Front Door:** Best for HTTP apps. Uses Anycast to detect region failures in <30 seconds and redirect traffic.
- **Azure Traffic Manager:** DNS-based. Works for any protocol. Routes based on priority (primary/secondary) or health probes.

---

## 🧪 DR Testing — "Don't Just Plan, Prove It Works"

> ⚠️ A DR plan that has never been tested is not a DR plan — it's a wish.

Common DR testing approaches:

1. **Tabletop Exercise:** The team talks through "what would we do if X happened?" No systems actually fail. Good for checking your runbook.

2. **Failover Test (Non-destructive):** Manually trigger a failover to the secondary region *without* taking down the primary. Test that users can connect to the secondary. Then fail back to primary.

3. **Chaos Engineering (Full Test):** Use tools like **Azure Chaos Studio** to intentionally inject failures (kill VMs, cut off databases, fill disks) in production or staging and observe whether the system recovers automatically.

**Recommended:** Run a full DR failover test at least **twice a year**. Document the actual RTO achieved and compare to your target.

---

## 📋 DR Strategy Selection Checklist

Before choosing your strategy, answer these questions with the business:

- [x] What is the maximum acceptable downtime? (→ Determines RTO)
- [x] How much data can we afford to lose? (→ Determines RPO)
- [x] What is our budget for DR infrastructure? (→ Determines tier)
- [x] Are there regulatory requirements? (e.g., GDPR, PCI-DSS may mandate specific RPO/RTO)
- [x] Which components are most critical? (Not everything needs Active/Active)
- [x] Have we tested the failover process? When was the last test?
- [x] Is the DR runbook documented and accessible without access to the primary region?
