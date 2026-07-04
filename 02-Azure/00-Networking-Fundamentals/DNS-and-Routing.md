---
tags: [azure, networking, rfc1918, dns, routing]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🗺️ Azure DNS and Routing Fundamentals

> "If IP Addresses are coordinates on a map, DNS is the friendly tour guide giving you the street names, and Routing is the paved road getting you there."

---

## 📖 Before You Read
Before you dive into DNS and Routing, make sure you understand:
- What an **IP Address** and **CIDR** block is — see [[IP-Addressing-and-CIDR]]
- What a **VNet** and **Subnet** are — see [[VNet]] and [[Subnets]]

---

## 1. 🤔 What is DNS?

### 🤔 What is it?
**DNS (Domain Name System)** is the phonebook of the internet. Humans are terrible at remembering numbers like `142.250.190.46`. We are great at remembering words like `google.com`. DNS is the system that translates the word into the number so your computer knows who to call.

> 📒 **Real-World Analogy:**
> You don't memorize your best friend's 10-digit phone number. You just open your phone, tap "Dave," and your phone automatically dials the hidden number. DNS is the contacts app on your phone.

### ⚙️ How does it work in Azure?
By default, Azure provides a magical, hidden DNS server for every VNet you create. It always lives at the exact same IP address: `168.63.129.16`. 
If you create two VMs in the same VNet named `web-server` and `db-server`, Azure's default DNS allows `web-server` to talk to `db-server` just by using its name!

**Custom DNS:**
If your company has its own private "Phonebook" (like a Windows Active Directory server on-premises), you can change the VNet settings to point to your Custom DNS Server instead of Azure's default one.

---

## 2. 🤔 What is Routing?

### 🤔 What is it?
**Routing** is the process of deciding which path a packet of data should take to reach its destination. 

### ⚙️ How does it work in Azure?
Azure handles basic routing automatically using **System Routes**.
- If two VMs are in the same VNet, Azure automatically knows how to route traffic between them.
- If a VM wants to talk to the public internet, Azure automatically routes it out to the web.

**User Defined Routes (UDRs):**
Sometimes, you don't want Azure to use the default path. For example, you might want to force all internet traffic to go through a massive security Firewall first. To do this, you create a custom map called a **Route Table**, write a UDR (a detour sign), and attach it to your Subnet. (See [[Route-Tables]]).

---

## 💡 Real Example (The 5 Reserved IPs)

When you are designing the routing and addressing for a Subnet in Azure, you have to be aware of a massive "gotcha": Azure steals 5 IP addresses from every single subnet you make!

If you create a subnet with the range `10.0.0.0/24` (which mathematically holds 256 IPs), you can only actually use 251 of them. Azure reserves:
1. `10.0.0.0` - The Network Address (Standard networking rule).
2. `10.0.0.1` - **The Azure Default Gateway** (The router that handles System Routes).
3. `10.0.0.2` - **The Azure DNS Server** (The hidden phonebook).
4. `10.0.0.3` - Reserved by Azure for future use.
5. `10.0.0.255` - The Broadcast Address (Standard networking rule).

---

## ⚠️ Common Mistakes Beginners Make

1. **Forgetting Peering is NOT Transitive:** If VNet A is connected to VNet B, and VNet B is connected to VNet C... VNet A **cannot** talk to VNet C! Azure does not route traffic "through" a middleman by default. You have to build a router or Firewall in VNet B and write custom UDRs to make this work.
2. **Making Subnets too small:** Because Azure steals 5 IPs, if you create a tiny `/29` subnet (which holds 8 IPs), you only have 3 usable IPs left for your Virtual Machines! Always make your subnets slightly larger than you think you need.

---

## 🎯 Key Takeaway
DNS translates human-readable names into IP addresses (Azure provides a default one at `168.63.129.16`). Routing determines how data travels between those IPs (Azure provides default System Routes, but you can override them with UDRs for security).

---

## ❓ Beginner FAQ

**Q1: What is a Private DNS Zone?**
> If you don't want to build a whole Custom DNS server, but you still want your database to have a pretty custom name like `database.mycompany.internal`, you can use Azure Private DNS Zones. It's a managed phonebook service that integrates directly with your VNet!

**Q2: Can I use `8.8.8.8` (Google's DNS) in my Azure VNet?**
> Technically yes, you can set `8.8.8.8` as your Custom DNS server. However, if you do this, your VMs will completely lose the ability to resolve the private names of other Azure resources inside your VNet!
