---
tags: [azure, networking, routing, udr]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🛣️ Azure Route Tables (UDR)

> "A Route Table is the digital GPS for your network traffic. If you don't like the default path Azure takes, you write a UDR to force traffic down a different road."

---

## 📖 Before You Read
Before you dive into Route Tables, make sure you understand:
- What a **VNet** and **Subnet** are — see [[VNet]] and [[Subnets]]
- What a **Firewall** is — see [[Architecture]]

---

## 🤔 What is it?

In Azure, traffic naturally knows how to move around. If you put two Virtual Machines in the same VNet, they can talk to each other. If you try to reach google.com, the traffic automatically goes out to the internet. These are called **System Routes**.

A **Route Table** is a custom list of directions you create. Inside the table, you write **User Defined Routes (UDRs)**, which are specific rules that override Azure's default GPS. 

> 🚦 **Real-World Analogy:**
> Imagine a VNet is a small town, and the Subnets are different neighborhoods. By default, there are roads (System Routes) connecting everything. You can drive directly from Neighborhood A to Neighborhood B, or straight out to the Highway (the Internet).
> 
> However, the Town Mayor (You) decides this is unsafe. You want to inspect every car leaving town. So, you build a massive Toll Booth / Security Checkpoint (a Firewall). You then put up detours and road signs (**User Defined Routes**) that say: "No matter where you are trying to go, you MUST drive through the Toll Booth first."

---

## 🧠 Why do we need it?

If you don't use Route Tables, any Virtual Machine in your network can reach out to the public internet. If a hacker gets onto your VM, they can download malware directly from a bad website.

In an enterprise environment, we use Route Tables to **Force Tunnel** all traffic. We force every single packet of data to pass through a central Firewall (like Azure Firewall or Palo Alto) so we can inspect it, block bad websites, and keep the network secure.

---

## ⚙️ How does it work?

A Route Table must be attached to a **Subnet**. Once attached, all traffic leaving that subnet must follow the rules in the table.

When you create a rule (a UDR), you have to tell Azure two things:
1. **Destination:** Where is the traffic trying to go? (Usually `0.0.0.0/0`, which means "Anywhere on the Internet").
2. **Next Hop Type:** Who do I hand this traffic to instead? 

### The 4 "Next Hop" Types
1. **Virtual Appliance (NVA):** The most common. This means "Hand the traffic to my Firewall." You must provide the IP address of the firewall.
2. **Virtual Network Gateway:** "Hand the traffic to the VPN so it goes back to our physical corporate office."
3. **Internet:** "Let this traffic go straight to the internet, bypassing the firewall." (Usually an exception rule).
4. **None:** "Drop the traffic immediately into a black hole."

---

## 💡 Real Example (Architecture Concept)

**The Hub & Spoke Problem (Transitivity)**

A major reason we need Route Tables is because **VNet Peering is NOT transitive.**

- **VNet A (Web App)** is connected to **VNet B (Hub/Firewall)**.
- **VNet C (Database)** is connected to **VNet B (Hub/Firewall)**.

Can the Web App talk directly to the Database? **NO.** Azure does not allow traffic to "pass through" the Hub by default. 

**The Solution:**
You must create a Route Table and attach it to VNet A. You write a UDR that says: "If you want to talk to VNet C, send your traffic to the Firewall in VNet B." You do the same for VNet C. Now, the Firewall acts as a router, inspecting the traffic and passing it along!

---

## ⚠️ Common Mistakes Beginners Make

1. **Asymmetric Routing:** This is a classic networking nightmare. Imagine traffic leaves VNet A, goes through the Firewall, and reaches VNet C. But VNet C *doesn't* have a Route Table attached. VNet C tries to reply *directly* to VNet A, bypassing the Firewall. The Firewall sees half a conversation and blocks everything. **Always attach Route Tables to all communicating subnets!**
2. **Attaching to the Gateway Subnet:** Beginners sometimes attach a Route Table with a `0.0.0.0/0` rule to the special `GatewaySubnet` (where the VPN lives). This breaks the VPN completely because the VPN can no longer talk to the actual internet!

---

## 🎯 Key Takeaway
System Routes handle basic traffic flow in Azure automatically. But for enterprise security, you must use Route Tables with User Defined Routes (UDRs) to override the defaults and force traffic through a central firewall or inspection point.

---

## ❓ Beginner FAQ

**Q1: Do I need a Route Table for my personal test project?**
> Usually, no. If you just have one VNet and want things to talk to the internet normally, Azure's System Routes do that for free. Route Tables are for advanced security architectures.

**Q2: What happens if a UDR conflicts with a System Route?**
> Azure uses the "Longest Prefix Match" rule (the most specific IP range wins). If the ranges are identical, Azure prefers UDRs over System Routes. Your custom rules will almost always win!

**Q3: Are Route Tables expensive?**
> No, the Route Table resource itself is completely free in Azure! You only pay for the Virtual Appliances (Firewalls) that you route the traffic to.
