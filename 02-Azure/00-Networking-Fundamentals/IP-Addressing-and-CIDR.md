---
tags: [networking, ip-address, cidr, public-private, subnets]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🔢 IP Addressing and CIDR Basics

> "An IP Address is your house number. A CIDR block tells the mailman how many houses are on your street."

---

## 📖 Before You Read
Before you dive into IP Addresses, make sure you understand:
- What a **Virtual Network (VNet)** is — see [[VNet]]

---

## 🤔 What is it?

To make two computers talk to each other, they both need a unique identifier. This is called an **IP (Internet Protocol) Address**. It looks like this: `192.168.1.5`.

When you build a network in the cloud, you can't just pick random IP addresses out of thin air. You have to reserve a specific "block" of addresses. The size of this block is defined using **CIDR (Classless Inter-Domain Routing) Notation**, which looks like a slash and a number at the end: `10.0.0.0/16`.

> 🏘️ **Real-World Analogy:**
> Imagine you are a real estate developer. You buy a plot of land and tell the city: "I need addresses for this neighborhood. The neighborhood starts at 100 Main Street, and there will be 256 houses." 
> 
> The IP Address is "100 Main Street." The CIDR notation (`/24`) is the math that proves there are exactly 256 houses on the street.

---

## 🧠 Why do we need it?

If you don't understand CIDR blocks, you will break your company's network.

If you build an Azure VNet that uses the `10.0.0.0/16` addresses, and your physical corporate office also uses the `10.0.0.0/16` addresses, they **cannot talk to each other**. It would be like having two houses with the exact same address; the mailman wouldn't know where to deliver the package! 

DevOps engineers must carefully plan out IP addresses so nothing overlaps.

---

## ⚙️ How does it work?

### 1. Public vs Private IPs
There are only about 4 billion IPv4 addresses in the world, and we ran out of them years ago. To solve this, the internet is split in two:
- **Public IPs:** Used on the public internet (like Google or Netflix). They must be 100% globally unique.
- **Private IPs (RFC 1918):** Used *inside* your private network (like your home Wi-Fi or a private Azure VNet). Millions of people can use the exact same private IP (like `192.168.1.5`) in their own homes because the traffic never touches the public internet! 

When building Azure VNets, you **always** use Private IPs. 

### 2. The CIDR Math Cheat Sheet
The number after the slash (`/`) tells you how many IPs are in the block. 
**The Golden Rule: The smaller the number, the LARGER the amount of IPs!**

| CIDR Prefix | Total IPs | What we use it for in Azure |
| :--- | :--- | :--- |
| **`/8`** | ~16.7 Million IPs | The entire massive global corporate network. |
| **`/16`** | 65,536 IPs | The standard size for an entire Azure **Virtual Network (VNet)**. |
| **`/24`** | 256 IPs | The standard size for a **Subnet** (holding a cluster of web servers). |
| **`/32`** | 1 single IP | A specific, individual computer. |
| **`/0`** | Every IP on Earth | Used in Firewalls to mean "The entire Public Internet". |

---

## 💡 Real Example (Designing a VNet)

Let's build a network for an application using proper CIDR planning.

1. **The VNet (The big plot of land):**
   You assign the VNet the address space `10.1.0.0/16`. This gives you 65,536 IPs to play with.

2. **The Subnets (The neighborhoods):**
   You chop the VNet into smaller `/24` chunks.
   - **Frontend Subnet:** `10.1.1.0/24` (256 IPs for Web Servers)
   - **Backend Subnet:** `10.1.2.0/24` (256 IPs for App Servers)
   - **Database Subnet:** `10.1.3.0/24` (256 IPs for Databases)

Because none of these numbers overlap, the network works perfectly!

---

## ⚠️ Common Mistakes Beginners Make

1. **Overlapping CIDR Blocks:** Creating VNet A with `10.0.0.0/16` and VNet B with `10.0.0.0/16`, and then trying to connect them via VNet Peering. Azure will block this connection because the IPs overlap! Always map out your IP ranges on a spreadsheet before typing Terraform code.
2. **Making Subnets too small:** A junior engineer might think, "I only need 2 databases, so I'll make a `/30` subnet which gives me 4 IPs." They forget that Azure reserves 5 IPs for itself in every subnet! The deployment will instantly fail. Always use at least a `/29` or larger.

---

## 🎯 Key Takeaway
IP Addresses are how computers find each other. Private IPs are used inside Azure, while Public IPs face the internet. CIDR notation (`/16`, `/24`) is the mathematical shorthand used to define exactly how many IP addresses are available in a given network block.

---

## ❓ Beginner FAQ

**Q1: Why do we use `10.x.x.x` so much in Azure?**
> The Internet Engineering Task Force (IETF) wrote a rulebook called "RFC 1918". It declared that the `10.0.0.0` to `10.255.255.255` range is permanently reserved for Private Networks. Because it's a massive block, enterprise companies love using it for their cloud environments.

**Q2: Will we ever run out of Private IPs?**
> Inside your own private network, no. The `10.x.x.x` block gives you 16.7 million IPs. Unless you are running 17 million Virtual Machines, you won't run out!

**Q3: What is IPv6?**
> Because the world ran out of Public IPv4 addresses, scientists invented IPv6. Instead of looking like `192.168.1.1`, an IPv6 address is massive and looks like `2001:0db8:85a3:0000:0000:8a2e:0370:7334`. Azure fully supports it, but IPv4 is still the dominant standard for internal cloud networks.