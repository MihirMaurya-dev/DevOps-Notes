---
tags: [landing-zone, management, monitoring, operations]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🛠️ Management and Operations

> "Building the cloud is only 20% of the job. Keeping it running, backed up, and patched is the other 80%."

---

## 📖 Before You Read
Before you dive into Management, make sure you understand:
- What **Azure Monitor and Log Analytics** are — see [[Monitor]] and [[Log-Analytics]]

---

## 🤔 What is it?

In the context of an Azure Landing Zone, **Management** (often called Operations or "Day 2 Ops") refers to the central systems put in place to monitor the health of your servers, back up your data, and install security patches.

When you build a Landing Zone, you don't wait for application teams to build their own backup systems. You build a centralized "Platform Management" environment that automatically protects every single server the moment it is created.

> 🏥 **Real-World Analogy:**
> Imagine building a massive hospital. 
> The doctors and nurses (the Application Developers) are focused on doing surgery (writing code). They shouldn't have to worry about changing the air filters in the AC unit or testing the backup generators. 
> 
> You need a dedicated Facilities Management team (The Landing Zone Management Subscription) whose entire job is to monitor the building's temperature, ensure the power stays on, and keep the floors clean so the doctors can focus on patients.

---

## 🧠 Why do we need it?

If you leave management up to individual development teams:
1. **Inconsistency:** Team A backs up their database every hour. Team B forgets to set up backups entirely. When a database crashes, Team B loses all their data.
2. **Blind Spots:** If a hacker attacks 5 different servers owned by 5 different teams, nobody will realize it's a coordinated attack because all the logs are stored in 5 different, disconnected databases.
3. **Wasted Effort:** Every team wastes 10 hours a week writing their own scripts to install Windows Updates, instead of writing features that make the company money.

---

## ⚙️ How does it work? (Centralized Platform Management)

In a proper Enterprise Landing Zone, you create a dedicated **Management Subscription**. Inside this subscription, you deploy the core centralized tools:

1. **Central Log Analytics Workspace:** The massive database where *every* server in the company sends its telemetry and security logs.
2. **Azure Automation Accounts:** Systems that run scheduled scripts (e.g., "Automatically turn off all Development servers at 7:00 PM to save money").
3. **Azure Update Manager:** The system that automatically schedules and installs Windows and Linux security patches across the entire company estate.
4. **Recovery Services Vaults:** The central vault that orchestrates automated daily backups for Virtual Machines and databases.

---

## 💡 Real Example (Policy-Driven Automation)

How do you guarantee that a developer's brand new server gets backed up? You use **Governance (Azure Policy)** combined with your **Management** tools!

1. The DevOps team creates an Azure Policy that says: *"If anyone creates a Virtual Machine, automatically install the Azure Monitor Agent and link the VM to the Central Recovery Services Vault."*
2. A developer in the Web Team deploys a new Ubuntu VM using Terraform.
3. Azure Policy detects the deployment. In the background, without the developer doing anything, it secretly installs the logging agent and configures a daily backup schedule.
4. The VM is instantly monitored and protected on Day 1!

---

## ⚠️ Common Mistakes Beginners Make

1. **Decentralized Logging:** Creating a new Log Analytics Workspace for every single application. When the security team needs to search for a hacker's IP address, they have to run the search 50 different times across 50 different workspaces. Always use one centralized workspace for the entire Landing Zone!
2. **Ignoring Alert Fatigue:** Setting up Azure Monitor to send an email every time a server's CPU hits 70%. The IT team will receive 4,000 emails a day, set up an Outlook rule to send them all to the Trash folder, and completely miss the email when the server actually crashes. Only alert on critical, actionable failures!

---

## 🎯 Key Takeaway
Landing Zone Management provides centralized, automated operations for the entire cloud environment. By centralizing logging, backups, and patching into a dedicated Management Subscription, you ensure consistency, increase security visibility, and free up developers to focus on their applications.

---

## ❓ Beginner FAQ

**Q1: What is Microsoft Defender for Cloud?**
> It is the ultimate centralized security management tool. It constantly scans your entire Landing Zone looking for vulnerabilities (like an open port or an unencrypted hard drive) and gives your environment a "Secure Score" out of 100%.

**Q2: If all the logs go to one central workspace, can developers see logs from other teams?**
> Not if you configure it correctly! Azure Log Analytics supports **Resource-Context RBAC**. This means a developer can log into the central workspace, but Azure will *only* show them the log lines generated by servers they personally own!
