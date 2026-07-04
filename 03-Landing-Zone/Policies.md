---
tags: [landing-zone, policy, governance, compliance]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 📜 Policies in the Landing Zone

> "If RBAC controls who is allowed to play the game, Azure Policy sets the rules of the game."

---

## 📖 Before You Read
Before you dive into Policies, make sure you understand:
- The overarching concept of **Governance** — see [[Governance]]
- How **Management Groups** work — see [[Management-Groups]]

---

## 🤔 What is it?

**Azure Policy** is the technical engine that enforces your company's Governance rules. 

It is a free Azure service that evaluates all of your resources to see if they are compliant with your corporate rules. It acts as an automated compliance auditor and security enforcer. If a resource breaks a rule, Azure Policy can log it, block it, or even automatically fix it.

> 👮 **Real-World Analogy:**
> Imagine a massive airport. 
> **RBAC** is the employee badge that lets a pilot through the security doors (Who are you?).
> **Azure Policy** is the metal detector and luggage scanner (Are you following the rules?). 
> Even if you are a verified pilot with the highest level badge (Owner RBAC), the metal detector will still sound an alarm and block you if you try to bring a forbidden item through the gate!

---

## 🧠 Why do we need it?

Humans make mistakes. A tired developer might accidentally deploy a server with an unencrypted hard drive. A distracted engineer might accidentally create a database in the "Asia" region instead of the "US" region, violating international data laws.

You cannot rely on humans reading a 50-page PDF security manual. You need an automated system that checks every single deployment in real-time, 24/7, and blocks dangerous actions before the resources are even created.

---

## ⚙️ How does it work? (The JSON Engine)

Azure Policies are written in JSON. A standard policy has three main parts:
1. **The Condition:** (e.g., "If the resource being created is a Virtual Machine...")
2. **The Rule:** (...and if the VM does not have the 'CostCenter' tag attached to it...)
3. **The Effect:** (...then DENY the creation of the VM.)

You take this JSON document and assign it to a Scope (usually a **Management Group**). Thanks to inheritance, every Subscription inside that Management Group is now governed by that policy.

### The 3 Core Effects:
- `Audit`: Do not block the user, but flag the resource as "Non-Compliant" in the central security dashboard. (Great for testing new rules without breaking things).
- `Deny`: Physically block the deployment. Terraform will return an error instantly.
- `DeployIfNotExists (DINE)`: The most powerful effect. If the user forgets to do something, Azure Policy will silently do it for them in the background!

---

## 💡 Real Example (The DINE Policy Magic)

The security team mandates that every single Virtual Machine must have the "Azure Monitor Agent" installed so logs can be collected centrally.

**Without Policy:** The DevOps team has to email all 500 developers and beg them to remember to install the agent in their code. Nobody remembers.
**With Azure Policy (DINE):** 
1. The DevOps team assigns a `DeployIfNotExists` policy to the Landing Zone.
2. A developer deploys a plain Ubuntu VM and completely forgets about the agent.
3. Azure Policy detects the new VM. It realizes the agent is missing.
4. Within 10 minutes, Azure Policy automatically triggers a background script that secretly installs the agent onto the developer's VM. 
5. The developer is happy (they didn't have to do extra work), and the security team is happy (the logs are flowing)!

---

## ⚠️ Common Mistakes Beginners Make

1. **Deploying "Deny" policies immediately:** If you suddenly apply a strict "Deny" policy to an existing production environment, you might accidentally block critical automated deployments and cause an outage. Always deploy policies in `Audit` mode first! Let it run for a week, see who is breaking the rules, warn them, and *then* switch it to `Deny`.
2. **Ignoring Policy Exemptions:** Sometimes, a specific project legitimately needs to break a rule. Instead of turning the policy off for the whole company, you should create a documented "Policy Exemption" for that specific resource group, which allows auditors to track exactly why the exception was made.

---

## 🎯 Key Takeaway
Azure Policy is the automated enforcement engine for Landing Zone governance. By applying JSON-based rules at the Management Group level, you can audit, block, or automatically remediate non-compliant resources across your entire cloud environment.

---

## ❓ Beginner FAQ

**Q1: What is a "Policy Initiative"?**
> A single policy checks one rule (e.g., "Must have tags"). A **Policy Initiative** (or Policy Set) is a bundle of dozens of policies grouped together. For example, Microsoft provides a built-in "ISO 27001" initiative that contains over 100 policies bundled together to help you pass that specific security audit.

**Q2: Does Azure Policy scan resources that already exist?**
> Yes! If you assign a new policy today, it evaluates everything you try to build *tomorrow*, but it also scans all your existing servers and flags the ones that are currently breaking the new rule as "Non-Compliant."
