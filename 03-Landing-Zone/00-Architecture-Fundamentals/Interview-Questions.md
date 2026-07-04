---
tags: [interview, networking, architecture, zero-trust]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Architecture Fundamentals: High-Quality Interview Questions

These questions test your deep understanding of Zero Trust security and Hub-and-Spoke network topologies. They are designed to mimic real-world scenario questions asked during DevOps or Cloud Engineering interviews.

---

## Question 1: The Transitivity Trap
**Scenario:** 
You have built a standard Hub and Spoke network. 
- You have a Hub VNet with an Azure Firewall.
- Spoke-Web is peered to the Hub.
- Spoke-Database is peered to the Hub.
A developer deploys a Web VM in Spoke-Web and a SQL VM in Spoke-Database. They try to connect the Web VM directly to the SQL VM's private IP, but the connection times out. 

**Question:** 
Why did the connection fail? What exact networking components must you configure to fix this?

<details>
<summary><b>Show Answer</b></summary>
<br>
The connection failed because <b>VNet Peering is not transitive.</b> Just because Spoke-Web and Spoke-Database are both peered to the Hub does not mean they can natively talk to each other.<br><br>
To fix this and establish Spoke-to-Spoke communication, you must:
1. <b>Create User Defined Routes (UDRs):</b> Create a Route Table and attach it to the Spoke-Web subnet. Add a rule stating that traffic destined for the Spoke-Database IP range must be routed to the <b>Private IP Address of the Azure Firewall in the Hub</b> (Next Hop: Virtual Appliance). Do the same in reverse for the Database subnet.
2. <b>Configure Firewall Rules:</b> Add a Network Rule inside the Azure Firewall explicitly allowing traffic from Spoke-Web's IP to Spoke-Database's IP on port 1433 (SQL).
</details>

---

## Question 2: Zero Trust vs. The Perimeter
**Scenario:**
The Chief Security Officer (CSO) at a legacy company states: "We don't need Multi-Factor Authentication (MFA) for our internal apps, because users can only access those apps if they are physically inside the corporate office connected to the corporate WiFi behind our massive physical firewall."

**Question:**
Explain why the CSO's strategy is dangerous in the modern era, and how the "Zero Trust" model addresses this exact flaw.

<details>
<summary><b>Show Answer</b></summary>
<br>
The CSO is relying on the outdated <b>"Castle and Moat"</b> (Perimeter) security model. This model assumes that anyone inside the physical office is trustworthy. It is dangerous because if a single employee's laptop gets infected with malware via a phishing email, the attacker is now "inside the moat" and has unrestricted lateral movement across the entire internal network.<br><br>
<b>Zero Trust</b> addresses this by destroying the concept of a "trusted internal network." Its motto is <i>"Never trust, always verify."</i> Under Zero Trust, the network location (being in the corporate office) does not grant you access. Every single request to an internal app must be explicitly verified based on User Identity (requiring MFA) and Device Health (checking if the laptop is patched), assuming a breach has already occurred on the network.
</details>

---

## Question 3: The Cost of Architecture
**Scenario:**
Your company has 30 different isolated application teams. The security team mandates that every application must be protected by a Premium Firewall and must have a secure VPN connection back to the corporate office. 

**Question:**
If you deploy these 30 applications in an isolated, "flat" architecture (each app in its own standalone VNet), what are the financial and operational consequences? How does the Hub and Spoke architecture solve this?

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>The Consequences:</b> If you use a flat, isolated architecture, you would be forced to deploy 30 separate Premium Firewalls and 30 separate VPN Gateways. Because these are incredibly expensive, enterprise-grade resources, the monthly Azure bill would skyrocket unnecessarily. Operationally, the security team would have to manage 30 different firewall rule sets independently.<br><br>
<b>The Hub and Spoke Solution:</b> By transitioning to a Hub and Spoke topology, you deploy <b>exactly one</b> Premium Firewall and <b>one</b> VPN Gateway inside a central Hub VNet. You then peer all 30 application VNets (Spokes) to the Hub. All 30 applications can now share the centralized security and connectivity resources, saving hundreds of thousands of dollars and giving the security team a single pane of glass to manage rules.
</details>
