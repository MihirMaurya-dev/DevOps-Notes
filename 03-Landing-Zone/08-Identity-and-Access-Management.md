---
tags: [landing-zone, identity, rbac, iam, security]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🔐 Identity and Access Management (IAM)

> "Identity is the new perimeter. It doesn't matter if you have a massive firewall if you accidentally hand the keys to the castle to the wrong person."

---

## 📖 Before You Read
Before you dive into IAM, make sure you understand:
- The basics of the **Entra ID Tenant** — see [[16-Azure-Billing-and-Entra-Tenant|Azure-Billing-and-Entra-Tenant]]
- What **RBAC** is — see [[35-RBAC|RBAC]]

---

## 🤔 What is it?

**Identity and Access Management (IAM)** is the framework of policies and technologies ensuring that the *right people* have the *appropriate access* to technology resources. 

In an Azure Landing Zone, IAM is the very first line of defense. It defines how users prove who they are (Authentication) and what buttons they are allowed to click once they are logged in (Authorization).

> 🎟️ **Real-World Analogy:**
> Imagine a high-security concert venue. 
> - **Identity (Authentication):** The security guard at the front door checks your driver's license to prove you are who you say you are. 
> - **Access Management (Authorization):** Once inside, your ticket dictates where you can go. A "General Admission" ticket lets you stand in the crowd. A "VIP" ticket lets you go backstage. You cannot go backstage with a General Admission ticket, even though you successfully made it into the building!

---

## 🧠 Why do we need it?

Historically, companies relied on physical firewalls. If you were sitting inside the corporate office connected to the corporate WiFi, you were trusted. 

In the cloud, anyone can reach the Azure Portal login screen from anywhere on Earth. If an attacker guesses an employee's weak password (like `Summer2024!`), they are inside. A robust IAM strategy ensures that even if a password is stolen, the attacker is blocked, or their blast radius is severely limited.

---

## ⚙️ How does it work? (The Core Tools)

Building IAM in a Landing Zone relies on three critical Azure features:

### 1. Microsoft Entra ID (The Directory)
This is the central database holding all the user accounts, groups, and passwords. You do not assign permissions directly to a single user (like "Dave"). You assign permissions to an Entra ID Group (like "Database Admins"), and then you put Dave inside that group. This makes managing 10,000 employees infinitely easier.

### 2. Azure RBAC (The Permissions)
Role-Based Access Control is how you define the "VIP Tickets." You assign a specific Role (like `Virtual Machine Contributor`) to a specific Group, at a specific Scope (like a Resource Group). 

### 3. Privileged Identity Management (PIM)
This is the crown jewel of enterprise IAM. Instead of giving a developer permanent "Admin" rights 24/7/365, they have zero rights by default. When they need to fix a server, they log into PIM and click "Activate." They must provide a justification and pass an MFA prompt. They are granted Admin rights for exactly 2 hours, and then the rights automatically vanish.

---

## 💡 Real Example (The Landing Zone Setup)

When building an Enterprise Landing Zone, the DevOps team will create several standard Entra ID groups and assign them baseline RBAC roles.

For example, for a newly created "Spoke" Subscription designed for the Web Team:
- **Group A: `Web-Team-Readers`** (Assigned the `Reader` role). They can view the servers and look at metrics, but cannot change anything.
- **Group B: `Web-Team-Contributors`** (Assigned the `Contributor` role). They can deploy new web servers and restart existing ones.
- **Group C: `Security-Auditors`** (Assigned the `Security Reader` role). A central corporate team that can view security logs across the entire company, but cannot touch the web servers.

---

## ⚠️ Common Mistakes Beginners Make

1. **Using "Owner" or "Contributor" for Everything:** Beginners hate dealing with "Access Denied" errors, so they just grant everyone the massive `Owner` role on the entire Subscription. This is incredibly dangerous and violates the **Principle of Least Privilege**. Only assign the exact role needed for the job.
2. **Assigning roles to Users instead of Groups:** If you assign the `Reader` role directly to "Alice", and then Alice leaves the company, you have to remember to manually hunt down and remove her permissions. Always assign roles to Groups, and let the HR automated systems add/remove people from the Groups.

---

## 🎯 Key Takeaway
Identity and Access Management (IAM) replaces the physical firewall as the primary security boundary in the cloud. By utilizing Entra ID Groups, strict RBAC roles, and Just-In-Time access (PIM), you ensure users can only impact the exact resources they are authorized to touch.

---

## ❓ Beginner FAQ

**Q1: What is a "Managed Identity"?**
> Normal identities are for humans (Dave). A Managed Identity is an identity for a *robot* (a Virtual Machine or an App Service). It allows an Azure server to securely authenticate to a database without needing a hardcoded password!

**Q2: What is Multi-Factor Authentication (MFA)?**
> Proving your identity using two different methods: Something you *know* (your password) AND something you *have* (a code texted to your phone, or an Authenticator App). It is the single most effective way to stop hackers.
