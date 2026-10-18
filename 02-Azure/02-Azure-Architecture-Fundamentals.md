---
tags: [azure, architecture, regions, availability-zones, hierarchy]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🏗️ Azure Architecture Fundamentals

> "If Azure is a global real estate company, you need to understand how they organize their buildings before you sign a lease."

---

## 📖 Before You Read
Before you dive into Azure Architecture, make sure you understand:
- What the **Cloud** is basically — see [[01-Azure-Fundamentals|Azure-Fundamentals]]

---

## 🤔 What is it?

Azure is absolutely massive. It consists of millions of physical computers spread across the entire globe. To manage this, Microsoft organizes everything into two distinct categories:

1. **Physical Architecture:** Where the actual hardware lives on the planet.
2. **Logical Architecture:** How your billing and security folders are organized.

> 🗺️ **Real-World Analogy:**
> Imagine a massive global bank. 
> - **Physical Architecture** is where the actual brick-and-mortar branch buildings are located (New York, London, Tokyo). 
> - **Logical Architecture** is how the bank organizes its internal accounts (Checking, Savings, Corporate). 

---

## 🧠 Why do we need it?

If you deploy an application without understanding Physical Architecture, a hurricane could destroy the datacenter your app is running in, and your company would go bankrupt. 

If you deploy an application without understanding Logical Architecture, your developers will accidentally delete production servers because everything is dumped into one unorganized folder.

---

## ⚙️ How does it work?

### Part 1: Physical Architecture (Where is the hardware?)

1. **Region:** A specific geographical area on the planet, like `East US` (Virginia) or `West Europe` (Netherlands). You always want to put your app in a region close to your customers so it loads faster!
2. **Availability Zones (AZ):** Within a single Region (like `East US`), Microsoft builds 3 completely separate physical buildings. These are called Zones. They have independent power grids and water supplies. If Zone 1 gets hit by lightning and burns down, Zone 2 and Zone 3 keep running.
3. **Geographies:** Usually lines up with country borders (e.g., "Germany"). This is important for legal reasons. Some countries have strict laws that say "Citizen data cannot leave the country."

### Part 2: Logical Architecture (How is it billed/secured?)

1. **Microsoft Entra ID Tenant:** The absolute top level. This is your company's identity (e.g., `mycompany.com`). It holds all the user accounts (like Dave from HR).
2. **Management Groups:** Folders used to group Subscriptions together so you can apply company-wide rules to them (like "Nobody is allowed to deploy expensive $5,000/month servers").
3. **Subscriptions:** The actual billing boundary. A subscription has a credit card attached to it. Every resource you build goes on this bill.
4. **Resource Groups:** Smaller folders inside the subscription used to group specific projects together. (See [[14-Resource-Groups|Resource-Groups]]).

---

## 💡 Real Example (Storage Redundancy)

Let's look at how Physical Architecture affects how you save files. Azure offers different levels of "Redundancy" (backup copies).

| Model | What it means | What it survives | Cost |
| :--- | :--- | :--- | :--- |
| **LRS** (Locally Redundant) | 3 copies of your file in **one building**. | A hard drive breaking. | 💲 |
| **ZRS** (Zone Redundant) | 3 copies spread across **3 different buildings** in the same city. | The entire building burning down. | 💲💲 |
| **GRS** (Geo-Redundant) | Copies in your city, AND copies in a city 500 miles away. | A massive regional disaster (hurricane, earthquake). | 💲💲💲 |

---

## ⚠️ Common Mistakes Beginners Make

1. **Ignoring Availability Zones:** Beginners often deploy a single Virtual Machine to a region and think they are safe. If that specific physical server rack loses power, your app goes offline. Always deploy at least 2 VMs and spread them across different Availability Zones (e.g., put VM 1 in Zone 1, and VM 2 in Zone 2).
2. **Mixing Lifecycles in Resource Groups:** Putting your temporary "Testing" servers in the exact same Resource Group as your critical "Production Database". When the test is over, someone will click "Delete" on the Resource Group and accidentally wipe out the entire company's database.

---

## 🎯 Key Takeaway
Azure's Physical Architecture (Regions and Zones) helps you design applications that survive disasters. Azure's Logical Architecture (Subscriptions and Resource Groups) helps you organize billing and security so engineers don't accidentally break things.

---

## ❓ Beginner FAQ

**Q1: Can I move a Virtual Machine from `East US` to `West Europe`?**
> Not easily! You can't just drag-and-drop a running server across the ocean. You usually have to take a snapshot backup of the hard drive, copy the backup to Europe, and create a brand new VM from the backup.

**Q2: Does every Region have 3 Availability Zones?**
> No! Older or smaller regions might only have 1 massive datacenter building. If you are designing a highly-available app, you must check the Microsoft documentation to ensure the region you picked supports Availability Zones.

**Q3: Who uses Management Groups?**
> If you are a small startup with 1 subscription, you don't need them. But if you are a massive enterprise with 500 different subscriptions for 500 different teams, Management Groups are the only way to keep everyone following the company rules.