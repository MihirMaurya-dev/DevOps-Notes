---
tags: [security, zero-trust, fundamentals]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🛑 Zero Trust Security Basics

> "Zero Trust is the paranoid security guard of the cloud. It doesn't care if you have the key to the front door; it's going to check your ID again at every single room inside."

---

## 📖 Before You Read
Before you dive into Zero Trust, make sure you understand:
- The basics of **Authentication and Authorization** — see [[01-Azure-Fundamentals|Azure-Fundamentals]]

---

## 🤔 What is it?

**Zero Trust** is a modern security philosophy that assumes hackers are already inside your network. 

Its core motto is: **"Never trust, always verify."** Regardless of where a user is logging in from, or what network they are on, the system refuses to grant them access to a resource until their identity and device health are explicitly proven.

> 🏰 **Real-World Analogy:**
> **The Old Way (Castle and Moat):** A medieval castle has a massive moat and a heavily guarded drawbridge (A Corporate Firewall). If you make it across the bridge, the guards assume you are friendly. You can wander into the King's bedroom, the armory, and the kitchen without anyone stopping you. If a spy sneaks across the bridge, the kingdom falls.
> 
> **The New Way (Zero Trust):** The drawbridge is still there. But now, there is a heavily armed guard standing in front of *every single door* inside the castle. Even if you are already inside the walls, the guard at the kitchen door asks for your ID, checks if you are sick, and asks the King if you are allowed to be there. 

---

## 🧠 Why do we need it?

The "Castle and Moat" perimeter defense worked in 2005 when all employees sat at physical desks inside a corporate office building. 

Today, the perimeter is dead. Employees work from coffee shops in Paris, they use their personal iPads to check email, and servers are hosted in public Azure datacenters. You can no longer trust a user just because they are connected to the "Corporate WiFi."

If an employee falls for a phishing email and a hacker steals their password, Zero Trust stops the hacker from moving sideways through the network to steal the company databases.

---

## ⚙️ How does it work? (The 3 Guiding Principles)

Zero Trust relies on three fundamental pillars:

### 1. Verify Explicitly
Do not just ask for a password. Ask for everything!
- *Who are you?* (Require Multi-Factor Authentication / MFA)
- *Where are you?* (Are you logging in from a known location, or suddenly from a strange country?)
- *What device are you using?* (Is your laptop managed by the company? Does it have the latest antivirus update?)
If *any* of these signals look suspicious, access is denied.

### 2. Use Least Privilege Access
Only give people the exact permissions they need, for the exact amount of time they need it.
- **Just-In-Time (JIT):** If an engineer needs to restart a server, they don't get permanent Admin rights. They push a button to request Admin rights, it is granted for exactly 2 hours, and then it is automatically revoked.
- **Just-Enough-Access (JEA):** An engineer should be allowed to restart the Virtual Machine, but they should absolutely not be allowed to change the billing credit card.

### 3. Assume Breach
Assume the hacker is already inside your network right now. 
- Cut the network into tiny pieces (Micro-segmentation) using Subnets and NSGs. If a hacker takes over a Web Server, the network rules should physically block them from talking to the Database server.
- Encrypt all data, both when it is sitting on the hard drive (At Rest) and when it is traveling over the wires (In Transit).

---

## 💡 Real Example (Azure Conditional Access)

Microsoft implements Zero Trust primarily through an Entra ID (Active Directory) feature called **Conditional Access Policies**.

Imagine a hacker steals the username and password of the company CEO. 

1. The hacker tries to log into the Azure Portal from an unmanaged laptop in a foreign country.
2. The Azure Conditional Access Policy (The Zero Trust engine) evaluates the request.
3. It sees the correct password. BUT, it sees the location is highly suspicious, and the device is not a registered corporate laptop.
4. **Action:** The system immediately blocks the login and forces a password reset, saving the company from a massive data breach.

---

## ⚠️ Common Mistakes Beginners Make

1. **Thinking Zero Trust is a product you buy:** Beginners often ask, "Which Azure button do I click to turn on Zero Trust?" It is not a software product. It is a strategic mindset. You achieve Zero Trust by combining Firewalls, MFA, RBAC, and Policies together over many months.
2. **Ignoring Device Health:** Many companies enforce MFA (verifying the *user*) but completely forget to verify the *device*. If a user logs in via MFA on a personal computer heavily infected with malware, the malware now has access to your cloud!

---

## 🎯 Key Takeaway
Zero Trust abandons the outdated idea of a "trusted internal network." It assumes the network is already compromised and demands continuous, explicit verification of identity, location, and device health for every single access request.

---

## ❓ Beginner FAQ

**Q1: Does Zero Trust mean we don't need Firewalls anymore?**
> No! You still absolutely need firewalls to block basic internet noise and attacks. Zero Trust just means that the firewall is no longer your *only* line of defense. It's a layered security model (Defense in Depth).

**Q2: Is Zero Trust annoying for employees?**
> It can be if implemented poorly! However, a good Zero Trust implementation uses Single Sign-On (SSO) and biometric authentication (like Windows Hello face recognition or fingerprints). Employees often find it *easier* because they don't have to remember complex passwords anymore!
