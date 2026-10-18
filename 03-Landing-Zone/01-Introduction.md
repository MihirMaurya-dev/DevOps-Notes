---
tags: [landing-zone, azure, architecture, basics]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🏗️ Introduction to Azure Landing Zones

> "You don't build a 50-story skyscraper on a patch of dirt. You must pour a massive concrete foundation first. In Azure, that foundation is called a Landing Zone."

---

## 📖 Before You Read
Before you dive into Landing Zones, make sure you understand:
- The **Azure Hierarchy** (Subscriptions, Resource Groups) — see [[01-Azure-Fundamentals|Azure-Fundamentals]]
- The basics of **Virtual Networks (VNets)** — see [[VNet]]

---

## 🤔 What is it?

An **Azure Landing Zone** is the foundational cloud environment that has been fully prepared, secured, and networked to host your company's applications. 

Before a software developer is allowed to spin up a single Virtual Machine, the Cloud DevOps team must build the Landing Zone. It contains the core "plumbing" of the cloud.

> 🏠 **Real-World Analogy:**
> Imagine you are building a new residential neighborhood. 
> Before the carpenters show up to build the actual houses (the Applications), the city must build the roads (Networking), install the streetlights and police stations (Security & Governance), and run the water pipes (Centralized Management). 
> 
> The fully prepped, empty neighborhood with all its roads and security cameras is the **Landing Zone**.

---

## 🧠 Why do we need it?

If a company moves to Azure *without* building a Landing Zone first, three disastrous things happen:
1. **Security Breaches:** Developers spin up servers directly facing the public internet because there is no central firewall forcing traffic to be inspected.
2. **IP Overlaps:** Team A creates a VNet using `10.0.0.0/16`. Team B creates a VNet using the exact same `10.0.0.0/16`. When they try to connect them later, the entire network crashes.
3. **Billing Nightmares:** Everyone deploys expensive $5,000/month servers into a single, chaotic subscription. At the end of the month, the CFO has no idea which team spent the money.

A Landing Zone provides **Guardrails** so developers can work fast without accidentally destroying the company.

---

## ⚙️ How does it work?

An effective Landing Zone addresses several critical "Design Areas" simultaneously. When you build one using Terraform, you are writing code to build these 6 pillars:

1. **Billing & Identity:** Creating the Microsoft Entra ID Tenant and organizing Subscriptions.
2. **Access Management:** Writing the strict RBAC roles (Who is allowed to touch what?).
3. **Network Topology:** Building the central Hub VNet, the Firewalls, and the VPNs back to the corporate office.
4. **Resource Organization:** Organizing everything neatly into Management Groups.
5. **Security & Governance:** Applying **Azure Policies** (e.g., "Nobody is allowed to deploy a server without a hard drive encryption tag").
6. **Management & Monitoring:** Creating a central Log Analytics Workspace to collect logs from every future server.

---

## 💡 Real Example (The DevOps Workflow)

**Step 1:** The Cloud Engineering team spends 3 months writing complex Terraform code. This code deploys Management Groups, a Hub Virtual Network, an Azure Firewall, and strict Azure Policies. This is the **Landing Zone**.

**Step 2:** The Software Development team asks for a place to host their new "HR Payroll" application. 

**Step 3:** The Cloud team hands them an empty "Spoke" Subscription inside the Landing Zone. Because the foundation is already built, the developers can immediately deploy their web servers safely, knowing the network is already routed through the central firewall and backed up to the central logging database.

---

## ⚠️ Common Mistakes Beginners Make

1. **Skipping the Planning Phase:** Treating a Landing Zone like a weekend project. Enterprise Landing Zones require weeks of architectural planning on whiteboards (especially IP addressing) before a single line of code is written. If you get the IP math wrong on day one, you have to tear the whole thing down later.
2. **Too Much Restriction:** Creating so many strict security policies in the Landing Zone that developers literally cannot do their jobs. The goal is to provide safe guardrails, not a brick wall.

---

## 🎯 Key Takeaway
A Landing Zone is the prerequisite, foundational architecture in Azure. It provides the centralized networking, security, identity, and governance required to safely host enterprise applications at scale.

---

## ❓ Beginner FAQ

**Q1: Do I need a Landing Zone for my personal test account?**
> No! If you are just studying or testing a single Web App, a Landing Zone is massive overkill. Landing Zones are designed for enterprise companies hosting dozens of applications and hundreds of employees.

**Q2: Is a Landing Zone a specific Azure Resource?**
> No. You cannot search the Azure Portal and click "Create Landing Zone." It is a *concept*. It is a collection of dozens of different resources (VNets, Policies, Firewalls, Subscriptions) configured to work together as a foundation.

**Q3: How do we actually build one?**
> Manually clicking buttons to build a Landing Zone takes weeks and is prone to human error. Professional teams use Infrastructure as Code (Terraform) to deploy the entire foundation automatically in minutes.
