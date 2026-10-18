---
tags: [landing-zone, subscriptions, scaling, limits]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 📦 Subscription Strategy

> "Subscriptions are not just billing accounts. They are the primary units of scale, security, and management in the Azure cloud."

---

## 📖 Before You Read
Before you dive into Subscription Strategy, make sure you understand:
- The **Azure Hierarchy** — see [[01-Azure-Fundamentals|Azure-Fundamentals]]
- How **Management Groups** organize Subscriptions — see [[05-Management-Groups|Management-Groups]]

---

## 🤔 What is it?

**Subscription Strategy (Democratization)** is the architectural decision of *how many* Subscriptions your company should create, and *how* you should divide your applications among them.

In the old days, companies would create exactly one Azure Subscription and dump every single database, Virtual Machine, and network for the entire company into that single bucket. The modern Landing Zone approach dictates that you should create dozens, or even hundreds, of Subscriptions and treat them like isolated folders.

> 🗃️ **Real-World Analogy:**
> Imagine a company's physical filing cabinet. 
> **The Bad Way (Single Subscription):** You take 10,000 pieces of paper from HR, Finance, IT, and Marketing, and shove them all into one massive, overflowing drawer. Finding a document is impossible, and if a coffee spills, everything is ruined.
> 
> **The Good Way (Subscription Democratization):** You buy 50 separate manila folders (Subscriptions). HR gets their own folder. Finance gets their own folder. If Finance spills coffee on their folder, HR's files are completely safe!

---

## 🧠 Why do we need it? (The 3 Big Reasons)

Why not just put everything in one Subscription? Because Azure will break.

1. **Hard Limits (Quotas):** Azure has physical limits per subscription. For example, you can only have 250 Storage Accounts per region per subscription. If your company deploys 251, the entire production environment crashes. By splitting apps into multiple Subscriptions, you multiply your limits!
2. **Security Boundaries:** A Subscription is a hard security boundary. If you give a developer "Owner" rights on the `HR-App` Subscription, they have absolute power there. But they have *zero* power to touch the `Finance-App` Subscription. It limits the "blast radius" if an account is hacked.
3. **Precise Cost Tracking:** While tags are great, tracking costs at the Subscription level is flawless. At the end of the month, the CFO sees exactly what the `Mobile-App-Production` subscription cost without having to filter through millions of individual tags.

---

## ⚙️ How does it work? (Archetypes and Environments)

How do you decide when to create a new Subscription? The Landing Zone Accelerator recommends organizing them by **Application** and by **Environment**.

For a single major application (like the Corporate Payroll System), you would create three separate Subscriptions:
1. **Subscription: `Corp-Payroll-Dev`**
   - Belongs to the "Sandboxes" Management Group.
   - Developers have Contributor rights.
   - Used for testing messy code.
2. **Subscription: `Corp-Payroll-QA`**
   - Belongs to the "Landing Zones" Management Group.
   - Used for final testing before release.
3. **Subscription: `Corp-Payroll-Prod`**
   - Belongs to the "Landing Zones" Management Group.
   - Developers have ZERO rights. Only automated CI/CD pipelines can deploy here.
   - Holds the live, money-making application.

---

## 💡 Real Example (The Subscription Vending Machine)

In an enterprise DevOps environment, the process of creating a new Subscription is entirely automated. This is called a **Subscription Vending Machine**.

1. A development team needs a place to build a new AI Chatbot. 
2. They do not email the IT team. Instead, they fill out an automated web form.
3. A Terraform pipeline runs automatically.
4. In 10 minutes, it creates a new Subscription (`Chatbot-Dev`), places it in the correct Management Group, connects it to the Hub VNet using VNet Peering, and assigns the developers the correct RBAC roles. 
5. The developers receive an email saying: *"Your new Landing Zone Spoke is ready. Start building!"*

---

## ⚠️ Common Mistakes Beginners Make

1. **Creating too few Subscriptions:** Trying to cram Dev, QA, and Prod all into a single subscription called "Corporate-IT". A developer testing a script will accidentally delete the production database because there is no hard boundary stopping them.
2. **Creating too many Subscriptions:** Creating a brand new Subscription for a single, tiny Virtual Machine. Subscriptions are for *workloads* (a complete application consisting of VMs, databases, and networks). Managing 5,000 subscriptions for 5,000 VMs is an administrative nightmare.

---

## 🎯 Key Takeaway
Subscription Democratization is the core scaling mechanism of Azure. By assigning individual applications their own dedicated Subscriptions, you bypass Azure limits, create strict security boundaries, and simplify billing across the enterprise.

---

## ❓ Beginner FAQ

**Q1: Do Subscriptions cost money?**
> No! The Subscription itself is just a logical container and is 100% free. You only pay for the Virtual Machines and databases you put *inside* the Subscription. You can create 100 empty subscriptions and your bill will be $0.00.

**Q2: Can I move a resource from one Subscription to another?**
> Yes, but it is risky! While Azure allows you to move many resources (like a VM or a Storage Account) across Subscriptions, it often breaks networking connections and causes downtime during the move. It is always better to build it in the correct Subscription from Day 1.
