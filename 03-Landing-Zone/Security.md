---
tags: [landing-zone, security, defender, sentinel]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🛡️ Security in the Landing Zone

> "In the cloud, you are no longer protecting a building; you are protecting data that can be accessed from anywhere on Earth."

---

## 📖 Before You Read
Before you dive into Security, make sure you understand:
- The concept of **Zero Trust** — see [[Zero-Trust-Basics]]
- The role of **Identity (IAM)** — see [[Identity-and-Access-Management]]

---

## 🤔 What is it?

**Security** in an Azure Landing Zone is the overarching design area that focuses on protecting your applications, data, and infrastructure from malicious attacks, accidental leaks, and compliance failures.

Unlike traditional IT where security was an "add-on" installed right before a project went live, Landing Zone security is **"Secure by Design."** It is baked into the foundation so that every single application inherits baseline protections automatically.

> 🏦 **Real-World Analogy:**
> Imagine a high-security bank.
> - **Identity (IAM)** is the vault door combination.
> - **Governance (Policy)** is the rulebook stating vault doors must be closed at 5 PM.
> - **Security** is the ecosystem of armed guards, the bulletproof glass, the laser sensors, the encrypted safes, and the security cameras actively watching for bank robbers.

---

## 🧠 Why do we need it?

The public cloud is hostile territory. Within 5 minutes of deploying a Virtual Machine with a Public IP address, automated hacker bots from across the globe will begin attacking it, trying to guess the password or exploit known vulnerabilities.

If security is not centralized in the Landing Zone:
1. Application teams will forget to encrypt their databases.
2. Servers will be left exposed to the public internet.
3. If an attack occurs, the security team won't get an alert until the data is already stolen.

---

## ⚙️ How does it work? (Defense in Depth)

Microsoft uses a strategy called **Defense in Depth**. This means relying on multiple layers of security, so if a hacker breaches one layer, the next layer stops them.

### Layer 1: Physical Security
Microsoft handles this. They hire the armed guards and build the concrete datacenters.

### Layer 2: Identity & Access (Zero Trust)
You enforce Multi-Factor Authentication (MFA) and strict RBAC roles. (See IAM).

### Layer 3: Perimeter & Network Security
You place an **Azure Firewall** in the Hub VNet to block malicious incoming traffic. You use **Network Security Groups (NSGs)** on your Spokes to ensure the Web servers can only talk to the Database servers on a specific port. You deploy **Azure DDoS Protection** to stop attackers from crashing your site with fake traffic.

### Layer 4: Compute & Application Security
You ensure VMs are patched using Azure Update Manager. You place a **Web Application Firewall (WAF)** in front of your website to block SQL Injection attacks.

### Layer 5: Data Security
You use **Azure Key Vault** to hide passwords. You ensure all Storage Accounts and Databases have **Encryption at Rest** turned on so that if someone physically stole the hard drive from Microsoft, the data is unreadable.

---

## 💡 Real Example (Microsoft Defender for Cloud)

The core tool that monitors all these layers in the Landing Zone is **Microsoft Defender for Cloud (MDC)**.

When you deploy a Landing Zone, you turn MDC on at the top-level Management Group. 
MDC acts as an automated security auditor that never sleeps. 
1. It scans every Subscription and produces a **Secure Score** (e.g., 65%). 
2. It gives you a prioritized checklist to improve the score: *"You have 5 Storage Accounts without firewalls. Click here to fix them."*
3. If a hacker actually manages to install malware on a VM, MDC detects the anomalous behavior and instantly fires a high-severity alert to the security team's pagers!

---

## ⚠️ Common Mistakes Beginners Make

1. **Ignoring the Shared Responsibility Model:** Assuming that because you are using Microsoft's cloud, Microsoft will protect your data. Microsoft secures the physical building; YOU are entirely responsible for securing the operating systems, the network rules, and the data itself.
2. **"Security by Obscurity":** Assuming a hacker won't find your database just because you gave it a weird name and didn't publish the URL. Hackers use automated scanners that find open databases in milliseconds. Always use real encryption and authentication.

---

## 🎯 Key Takeaway
Landing Zone Security relies on "Defense in Depth" and "Zero Trust." By centralizing firewalls, encryption policies, and threat detection tools (like Defender for Cloud) at the foundational level, you ensure all workloads are protected against modern cyber threats.

---

## ❓ Beginner FAQ

**Q1: What is Microsoft Sentinel?**
> While Defender for Cloud protects Azure resources, **Microsoft Sentinel** is a massive SIEM (Security Information and Event Management) tool. It collects security logs from *everywhere*—Azure, AWS, your physical office routers, and employee laptops—and uses AI to detect massive, coordinated cyber-attacks across your entire company.

**Q2: What is a WAF?**
> A **Web Application Firewall (WAF)** is a specialized firewall designed specifically for websites. While a normal firewall blocks basic ports (like blocking port 22 for SSH), a WAF actively reads the HTTP web traffic to stop hackers from submitting malicious code (like SQL injections) into your website's login forms.
