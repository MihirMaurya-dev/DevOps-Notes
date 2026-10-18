---
tags: [landing-zone, billing, entra-id, tenant, fundamentals]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 💳 Azure Billing and the Entra ID Tenant

> "Before you can build anything in the cloud, Microsoft needs to know two things: Who are you, and how are you going to pay for this?"

---

## 📖 Before You Read
Before you dive into Billing and Tenants, make sure you understand:
- The **Azure Hierarchy** — see [[01-Azure-Fundamentals|Azure-Fundamentals]]

---

## 🤔 What is it?

When a company signs up for Azure, the very first two things created are the **Microsoft Entra ID Tenant** and the **Billing Account**.

1. **The Entra ID Tenant (The "Who"):** This is the master directory of all your employees. It is the absolute highest boundary of security. If your company is "Contoso", your tenant is `contoso.onmicrosoft.com`. Every single username and password lives here. *(Note: Microsoft renamed this from "Azure Active Directory" to "Microsoft Entra ID" recently).*
2. **The Billing Account (The "How to Pay"):** This is the financial agreement between your company and Microsoft. It dictates how you are invoiced and who receives the monthly bill.

> 🏢 **Real-World Analogy:**
> Imagine a company renting a massive 50-story office building. 
> 
> The **Entra ID Tenant** is the security desk in the lobby. They hold the master list of all employees and issue the plastic ID badges. If you don't have a badge, you can't get into the elevators.
> 
> The **Billing Account** is the lease agreement locked in the CEO's safe. It dictates how much rent the company pays to the building owner every month.

---

## 🧠 Why do we need it?

We need these separated because **Identity** and **Money** are managed by completely different teams. 

The HR and IT Security teams need total control over the Entra ID Tenant to hire, fire, and manage employee passwords. 
The Finance department (the CFO) needs total control over the Billing Account to pay invoices and forecast budgets. 

By separating them at the very top of the hierarchy, the CFO can pay the bills without accidentally gaining the power to delete the company's databases, and the IT Security team can manage passwords without seeing the corporate credit card number.

---

## ⚙️ How does it work? (The Hierarchy Connection)

The Tenant and the Billing Account sit completely outside of your normal Azure resources (like Virtual Machines). They connect to your resources through **Subscriptions**.

1. The Finance team uses the **Billing Account** to create a new **Subscription** (a bucket of money).
2. The IT team takes that Subscription and links it to the **Entra ID Tenant** (the bucket of users).
3. Now, you can build Virtual Machines inside the Subscription. The Virtual Machines will be billed to Finance, but secured by IT!

---

## 💡 Real Example (Enterprise Agreements)

If you create a personal Azure account at home, you just type in your personal credit card. But massive companies don't pay their cloud bills with a credit card!

Large companies sign an **Enterprise Agreement (EA)** with Microsoft. 
1. The company agrees to commit to spending $1,000,000 over the next 3 years.
2. In exchange, Microsoft gives them massive discounts on Virtual Machines.
3. Microsoft creates a top-level `EA Billing Account` for the company.
4. The company uses that EA account to spin up dozens of Subscriptions for their different departments. All the spending rolls up into one massive, discounted monthly invoice.

---

## ⚠️ Common Mistakes Beginners Make

1. **Confusing Azure with Entra ID:** Beginners think they are the exact same thing. They are not! Entra ID is just an identity service (it manages usernames/passwords). Azure is a cloud hosting service (it manages servers). They are separate services that talk to each other.
2. **Putting Dev and Prod in the same Subscription:** If a developer accidentally writes a bad script that spins up 5,000 servers, the company will get a massive bill. If Dev and Prod share a subscription, it is very hard to tell exactly who caused the massive spike in cost. Always separate environments into different subscriptions!

---

## 🎯 Key Takeaway
The Microsoft Entra ID Tenant manages the identities (users and passwords), while the Billing Account manages the money. They sit at the absolute top of the Landing Zone hierarchy and are joined together at the Subscription level.

---

## ❓ Beginner FAQ

**Q1: Can one company have multiple Entra ID Tenants?**
> Yes! This usually happens during mergers and acquisitions. If Company A buys Company B, they might temporarily have two separate Tenants. However, managing two Tenants is incredibly painful, so companies usually spend months migrating everyone into a single master Tenant.

**Q2: If I delete my Subscription, does my Entra ID Tenant get deleted too?**
> No! Remember, they are separate. Deleting the subscription just stops the billing and deletes the servers inside it. Your user accounts, passwords, and the Tenant itself will remain perfectly safe.
