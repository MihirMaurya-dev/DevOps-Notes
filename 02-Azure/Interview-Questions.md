---
tags: [interview, azure, rbac, security, architecture]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Azure Core: High-Quality Interview Questions

These questions test your deep understanding of top-level Azure services like RBAC, Managed Identities, Key Vault, and Virtual Networks. They are designed to mimic real-world scenario questions asked during DevOps or Cloud Engineering interviews.

---

## Question 1: The Identity Secret Leak
**Scenario:** 
A developer asks for the database connection string and password so they can hardcode it into their Python web app running on Azure App Service. You refuse. Instead, you tell them you have placed the password inside an Azure Key Vault. The developer asks, "But how does my web app get the password out of the Key Vault without me giving the web app a password to unlock the Key Vault?"

**Question:** 
Explain the Azure service that solves this "chicken and egg" secret problem, and how it works under the hood.

<details>
<summary><b>Show Answer</b></summary>
<br>
The solution is <b>Managed Identity</b> (specifically, a System-Assigned Managed Identity).<br><br>
Instead of giving the web app a password, you flip a switch in Azure that gives the Web App its own unique "ID Card" in Microsoft Entra ID. Because Microsoft owns the physical server running the Web App, Azure automatically rotates the invisible credentials for this identity in the background. <br><br>
You then go to the Key Vault and use <b>Azure RBAC</b> to grant the "Key Vault Secrets User" role directly to the Web App's Managed Identity. When the Python code requests the secret, Azure verifies the server's invisible identity token and seamlessly opens the vault. No human passwords are ever handled!
</details>

---

## Question 2: RBAC Scope Inheritance
**Scenario:**
You are the Cloud Administrator. You grant an engineer the "Virtual Machine Contributor" role at the **Subscription** level. Ten minutes later, a project manager complains that this same engineer just accidentally restarted a critical production database (Azure SQL), causing an outage. 

**Question:**
If you only gave them "Virtual Machine Contributor", how did they have access to restart a database? What fundamental concept of Azure RBAC did you misunderstand?

<details>
<summary><b>Show Answer</b></summary>
<br>
The issue here is <b>Scope Inheritance</b> and misunderstanding the role definitions.<br><br>
However, if they <i>only</i> had the "Virtual Machine Contributor" role, they actually <b>cannot</b> restart an Azure SQL database. Azure RBAC roles are strictly defined JSON files that only allow actions like `Microsoft.Compute/virtualMachines/*`. <br><br>
If the engineer restarted the database, one of two things happened:
1. You accidentally gave them the blanket "Contributor" role (which allows managing <i>all</i> resources) instead of "Virtual Machine Contributor". Because you applied it at the Subscription level, that access flowed downhill to every Resource Group and database in the subscription.
2. The database was not an Azure SQL PaaS resource, but rather a SQL server installed manually inside a Virtual Machine. Because they had VM Contributor rights, they restarted the underlying Virtual Machine, which took the database offline.
<br><br>
The best practice is the <b>Principle of Least Privilege</b>: Only assign specific roles (like VM Contributor), and assign them at the lowest scope possible (the specific Resource Group), not the entire Subscription.
</details>

---

## Question 3: Spoke-to-Spoke Communication
**Scenario:**
You have built a Hub-and-Spoke network topology. VNet-Hub contains an Azure Firewall. VNet-Spoke-1 contains a Web Server. VNet-Spoke-2 contains a Database. 
You set up VNet Peering between Spoke-1 and the Hub, and between Spoke-2 and the Hub. 
The Web Server attempts to connect to the Database. The connection times out.

**Question:**
Why does the connection fail, and what two Azure Networking components must you configure to fix it?

<details>
<summary><b>Show Answer</b></summary>
<br>
The connection fails because <b>Azure VNet Peering is NOT transitive</b>. Traffic from Spoke-1 goes to the Hub, but Azure will not automatically forward it out to Spoke-2.<br><br>
To fix this, you must:
1. <b>Create User Defined Routes (UDRs):</b> Create a Route Table and attach it to Spoke-1. Add a rule stating that traffic destined for Spoke-2's IP range must be sent to the Azure Firewall's private IP address in the Hub (Next Hop: Virtual Appliance). Do the exact same thing in reverse for Spoke-2.
2. <b>Configure Firewall Rules:</b> Ensure the Azure Firewall in the Hub actually has a network rule allowing traffic from Spoke-1's IP to Spoke-2's IP on the database port (e.g., 1433).
</details>

---

## Question 4: Stateful vs Stateless Firewalls
**Scenario:**
You create a Virtual Machine with a public IP. You attach a Network Security Group (NSG) to its subnet. You create an Inbound rule to Allow Port 80 (HTTP) so users can view the website. You do not create any Outbound rules.

**Question:**
When a user visits the website, will the website be able to send the HTML code back to the user? Why or why not? What if this was a traditional stateless firewall?

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Yes, the website will successfully send the HTML back to the user.</b><br><br>
This is because Azure Network Security Groups (NSGs) are <b>Stateful</b> firewalls. A stateful firewall tracks the "state" of the connection. When it allows an inbound packet through on Port 80, it remembers that connection and automatically creates an invisible, temporary rule to allow the return traffic out, regardless of your outbound rules.<br><br>
If this were a <b>Stateless</b> firewall (like traditional Network ACLs in AWS), it would forget the connection the instant the packet arrived. You would be required to manually write a second Outbound rule allowing traffic back to the user on ephemeral ports, or the website would fail to load.
</details>
