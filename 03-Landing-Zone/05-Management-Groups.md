---
tags: [landing-zone, management-groups, hierarchy, organization]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🗂️ Management Groups

> "If Subscriptions are folders holding your servers, Management Groups are the massive filing cabinets holding your folders."

---

## 📖 Before You Read
Before you dive into Management Groups, make sure you understand:
- The **Azure Hierarchy** — see [[01-Azure-Fundamentals|Azure-Fundamentals]]
- What **Azure Policy** and **RBAC** are — see [[12-Governance|Governance]] and [[35-RBAC|RBAC]]

---

## 🤔 What is it?

A **Management Group** is a logical container used to organize Azure Subscriptions. 

They sit directly below the top-level Entra ID Tenant, but *above* your Subscriptions. You can nest Management Groups inside other Management Groups to create a massive, company-wide organizational tree.

> 🏢 **Real-World Analogy:**
> Imagine a global corporation's filing system.
> - The top-level **Management Group** is the file room labeled "Global Corporation."
> - Inside that room are two smaller **Management Groups**: A cabinet labeled "Human Resources" and a cabinet labeled "Finance."
> - Inside the "Finance" cabinet are individual manila folders (**Subscriptions**) for specific projects.
> - Inside the manila folders are the actual pieces of paper (**Resources** like Virtual Machines).

---

## 🧠 Why do we need it?

If a company only has 1 Subscription, they don't need Management Groups. 
But enterprise companies often have **hundreds** of Subscriptions. 

If the Chief Security Officer mandates a new rule: *"No servers can be built outside of the United States,"* how do they enforce it? 
Without Management Groups, an engineer would have to manually apply that Azure Policy to 500 individual Subscriptions one by one. It would take weeks, and they would inevitably miss one.

With Management Groups, the engineer applies the policy ONCE to the "Global Corporation" top-level Management Group. Because of **Inheritance**, that policy automatically flows downhill and locks down all 500 Subscriptions instantly!

---

## ⚙️ How does it work? (The Enterprise-Scale Hierarchy)

When you deploy the official Azure Landing Zone Accelerator, it automatically builds a highly optimized Management Group tree for you. It usually looks like this:

1. **Tenant Root Group:** The absolute top.
   2. **Contoso (Company Name):** The main container. You apply global policies here.
      3. **Platform:** Contains the core IT infrastructure.
         - *Management Subscription:* (Log Analytics, Automation)
         - *Connectivity Subscription:* (Hub VNet, Firewalls, ExpressRoute)
         - *Identity Subscription:* (Domain Controllers)
      4. **Landing Zones:** Contains the actual business applications.
         - **Corp:** Internal applications (No public internet access allowed).
         - **Online:** Public-facing websites (Strict web application firewall rules applied).
      5. **Sandboxes:** Unrestricted environments for developers to experiment. (Strict cost limits applied so they don't bankrupt the company).

---

## 💡 Real Example (Inheritance in Action)

Let's look at how RBAC (Permissions) flow down the tree.

- You assign the `Network Contributor` role to the IT Networking Team at the **"Connectivity" Management Group** level.
- The Networking Team automatically gains access to every single VNet, Firewall, and VPN located in any Subscription placed inside that "Connectivity" folder. 
- However, they have ZERO access to the Subscriptions sitting inside the "Landing Zones" folder!

This allows you to grant massive, sweeping permissions securely and efficiently.

---

## ⚠️ Common Mistakes Beginners Make

1. **Creating a flat structure:** Creating 50 Management Groups directly under the Root, without nesting them logically by business unit or security profile. This completely defeats the purpose of the inheritance hierarchy.
2. **Applying Policies too high:** A junior engineer might apply a strict policy like "Deny all Public IP Addresses" at the absolute Top-Level Root group. This successfully secures the internal apps, but instantly breaks the company's public-facing website because the rule flowed down into the "Online" group too! Always apply policies at the correct level of the tree.

---

## 🎯 Key Takeaway
Management Groups provide an enterprise-grade scope above Subscriptions. They allow cloud architects to efficiently organize hundreds of Subscriptions and apply RBAC permissions and Azure Policies in bulk using top-down inheritance.

---

## ❓ Beginner FAQ

**Q1: How many levels deep can I nest Management Groups?**
> Azure allows you to nest Management Groups up to **6 levels deep** (not including the Root level or the Subscriptions at the bottom).

**Q2: Can a Subscription belong to two Management Groups at the same time?**
> No. A Subscription can only have one direct parent Management Group.

**Q3: Do Management Groups cost money?**
> No! Management Groups are purely logical organizational folders. They are 100% free to create and use.
