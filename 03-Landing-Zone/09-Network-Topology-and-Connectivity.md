---
tags: [landing-zone, networking, connectivity, virtual-wan]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🌐 Network Topology and Connectivity

> "The network is the circulatory system of the cloud. If the blood stops flowing, the applications die."

---

## 📖 Before You Read
Before you dive into Network Topology, make sure you understand:
- The basics of **Virtual Networks (VNets)** — see [[VNet]]
- The **Hub and Spoke** architecture — see [[01-Hub-Spoke-Theory|Hub-Spoke-Theory]]

---

## 🤔 What is it?

In an Azure Landing Zone, **Network Topology and Connectivity** refers to the physical and logical design of how all your cloud resources talk to each other, how they talk to the public internet, and how they talk to your company's physical office buildings.

It is the most complex and critical pillar of a Landing Zone. You must design the IP addressing, the firewalls, the DNS resolution, and the VPN connections before anyone deploys a single server.

> 🛣️ **Real-World Analogy:**
> Designing a cloud network is like designing the highway system for a brand-new country.
> You must plan out the massive multi-lane interstates connecting major cities (ExpressRoute to the physical office), the local city streets (Subnets), the border patrol checkpoints (Firewalls), and the street signs so people know where to go (DNS). 
> If you build the roads too narrow, traffic jams will ruin the economy.

---

## 🧠 Why do we need it?

If you get the network topology wrong on Day 1, it is almost impossible to fix on Day 100 without completely deleting your servers and starting over.

1. **IP Overlap Catastrophes:** If Team A and Team B both decide to build their networks using the exact same IP range (`10.0.0.0/16`), you can never connect them together. The routers will be confused and traffic will drop.
2. **Security Vulnerabilities:** Without a centralized topology, developers will put Public IP addresses directly on their Virtual Machines, bypassing corporate security and exposing the company to hackers.
3. **Hybrid Connectivity:** Enterprises need their cloud servers to securely talk to their physical on-premises databases without traversing the dangerous public internet.

---

## ⚙️ How does it work? (The Standard Architecture)

The official Azure Landing Zone Accelerator mandates a **Hub and Spoke** network topology.

### The Connectivity Subscription (The Hub)
You create a dedicated "Connectivity" Subscription. Inside it, you build the **Hub VNet**. This Hub is the central routing point for the entire company. It contains:
- **Azure Firewall:** Inspects all traffic leaving the cloud.
- **VPN / ExpressRoute Gateway:** The dedicated hardware that connects the Azure Cloud directly to your physical corporate office.
- **Private DNS Zones:** Ensures that servers can find each other by name (e.g., `sql-prod.internal.corp`) instead of trying to remember IP addresses.

### The Landing Zone Subscriptions (The Spokes)
Every time a new application needs to be deployed, you create a new Subscription. Inside it, you create a **Spoke VNet**. 
You then connect the Spoke VNet to the Hub VNet using **VNet Peering**. 

Because of this connection, the application in the Spoke can securely use the Firewall and the VPN located in the Hub!

---

## 💡 Real Example (The Developer Experience)

A developer at the physical London office needs to update the code on a Dev Web Server located in Azure.

1. The developer types `ssh dev-web.internal` into their laptop.
2. The laptop sends the traffic through the physical office router, across the secure corporate **ExpressRoute** cable, and into the **Hub VNet** in Azure.
3. The **Azure Firewall** in the Hub inspects the traffic, verifies it is legitimate SSH traffic from the London office, and permits it.
4. The traffic is routed across the **VNet Peering** link directly into the **Dev Spoke VNet**, successfully connecting to the Web Server!

The developer never touched the public internet, and they never needed a Public IP address on their server.

---

## ⚠️ Common Mistakes Beginners Make

1. **Failing to plan IP spaces:** Throwing random CIDR blocks (like `/16` or `/24`) at VNets without a master Excel spreadsheet tracking them. Eventually, you will overlap IP spaces and break your network. Enterprise IP planning takes weeks of math.
2. **Ignoring Transitivity:** Assuming that because Spoke A is connected to the Hub, and Spoke B is connected to the Hub, that Spoke A can talk to Spoke B. **VNet Peering is NOT transitive!** You must explicitly configure Route Tables to push that traffic through the Hub Firewall.

---

## 🎯 Key Takeaway
Network Topology in a Landing Zone relies on a centralized Hub-and-Spoke design. By centralizing connectivity components (Firewalls, VPNs, DNS) in the Hub, you provide secure, scalable, and cost-effective networking to dozens of Application Spokes.

---

## ❓ Beginner FAQ

**Q1: What is the difference between a VPN and an ExpressRoute?**
> A **VPN (Site-to-Site)** encrypts your traffic and sends it over the public internet to Azure. It is cheap but can be slow. 
> An **ExpressRoute** is a literal, physical fiber-optic cable that your telecom provider runs from your office directly into the Azure Datacenter. It is completely private, incredibly fast, and very expensive.

**Q2: What is Azure Virtual WAN (vWAN)?**
> vWAN is Microsoft's fully managed version of Hub and Spoke. Instead of you manually building the Hub VNet and configuring complex routing tables, you pay Microsoft to run a massive, global "Virtual Hub" that handles all the routing for you automatically.
