---
tags: [architecture, landing-zone, overview]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🏗️ Landing Zone Architecture Overview

> "A Landing Zone is the foundation of your digital house. You wouldn't build a mansion on sand; you wouldn't build enterprise cloud apps without a Landing Zone."

---

## 📖 Before You Read
Before digging into Landing Zones, make sure you understand the following:
- What a **Virtual Network (VNet)** is — see [[VNet]] and [[Subnets]]
- What **Azure** is fundamentally — see [[Azure-Fundamentals]]
- The basics of **Identity** and **RBAC** — see [[RBAC]]
- What **Infrastructure as Code (IaC)** is — see [[01-Introduction]] (Terraform)

---

## 🤔 What is a Landing Zone?

### 🤔 What is it?
An **Azure Landing Zone** is the output of a multi-subscription Azure environment that accounts for scale, security, governance, networking, and identity. 

> 🏙️ **Real-World Analogy:**
> Imagine you are a city planner preparing land for new businesses. You wouldn't just tell companies "build wherever you want." You have to lay down the roads (Networking), set up the police and fire stations (Security), write the city zoning laws (Governance/Policies), and issue ID cards to residents (Identity) *before* the buildings (Applications) can be built.
> 
> An **Azure Landing Zone** is the fully prepped "digital city" where your application teams can come and safely build their apps, knowing all the plumbing and security is already handled by the cloud engineers.

---

## 🧠 Why do we need it?
Without a Landing Zone, cloud adoption becomes a chaotic "Wild West."
- Developers will create resources with public IP addresses, risking security breaches.
- Every team will build their own isolated networks, making it impossible for apps to communicate.
- Your company will lose track of spending because resources aren't organized or tagged properly.
- You'll have 50 different ways of logging errors, making troubleshooting a nightmare.

A Landing Zone provides a **standardized, secure, and governed** baseline. It ensures that no matter how many apps your company builds, they all follow the same strict enterprise rules.

---

## ⚙️ How does it work? (The Big Picture / HLD)

A Landing Zone integrates several core domains into a cohesive **High Level Design (HLD)**. Let's break down the 4 pillars:

### 1. 🪪 Identity & Access Management
- **Microsoft Entra ID:** This is the ultimate boss of identity (think: the digital HR department). Everything starts here.
- **RBAC (Role-Based Access Control):** Access is given via Security Groups, never directly to individuals. (See [[RBAC]]).
- **PIM (Privileged Identity Management):** Even administrators don't have permanent access. They must "request" temporary access when they need to perform dangerous tasks.

### 2. 🗂️ Resource Organization
- **Management Groups:** Think of these as folders for your Subscriptions. We arrange them in a hierarchy: 
  - `Tenant Root` (The whole company)
    - `Platform` (Shared IT services)
    - `Workloads` (The actual business applications)
    - `Sandboxes` (Playgrounds for developers)
- **Azure Policy:** Rules enforced at the Management Group level. Example: "Nobody is allowed to deploy a Virtual Machine larger than 4 CPUs to save money." (See [[Policies]]).

### 3. 🌐 Networking (Hub & Spoke Topology)
- **Hub VNet:** The central "airport hub." It contains shared services like the **Azure Firewall** (security guard) and **VPN Gateway** (secure tunnel to your physical office).
- **Spoke VNets:** The "destination cities." Each application gets its own Spoke VNet. 
- **The Rule:** Spokes *never* talk directly to each other. All traffic must pass through the Hub VNet so the Azure Firewall can inspect it. We use **UDRs (User Defined Routes)** to force this traffic flow.

### 4. 🛡️ Security & Monitoring
- **Log Analytics Workspace:** A central "black box" where all logs, metrics, and errors from every server are stored.
- **Microsoft Defender for Cloud:** A built-in security tool constantly scanning for vulnerabilities.
- **Azure Key Vault:** A digital safe used to store all application passwords and secrets. (See [[Key-Vault]]).

---

## 💡 Real Example: Deployment Strategy (IaC)

A Landing Zone is incredibly complex. You should **never** deploy it manually by clicking around in the Azure Portal (a practice derisively called "Click-Ops"). 

Instead, you use **Infrastructure as Code (IaC)**. You write code that describes your Landing Zone, and tools like Terraform build it for you exactly the same way every time.

```hcl
# Example Terraform block deploying a Management Group (Resource Organization)
# This creates a folder to hold our application subscriptions
resource "azurerm_management_group" "workloads" {
  display_name               = "Corp-Workloads"
  parent_management_group_id = azurerm_management_group.root.id
}

# Example Terraform block assigning a Policy to that Management Group
# This policy forces everyone to add an "Environment" tag to their resources
resource "azurerm_management_group_policy_assignment" "require_tags" {
  name                 = "require-env-tag"
  management_group_id  = azurerm_management_group.workloads.id
  policy_definition_id = "/providers/Microsoft.Authorization/policyDefinitions/..."
}
```

### The "Subscription Vending Machine"
Once the Landing Zone is built, how do developers get a place to work? 
Cloud Engineers use a CI/CD pipeline (like GitHub Actions) called a **Subscription Vending Machine**. 
When a developer team requests a new environment, the pipeline automatically:
1. Creates a new Azure Subscription.
2. Creates a Spoke VNet.
3. Peers the Spoke VNet to the Hub VNet.
4. Assigns the correct RBAC permissions to the developers.
5. Applies all security policies.
...all in a few minutes without human intervention!

---

## ⚠️ Common Mistakes Beginners Make

1. **Click-Ops Deployment:** Trying to build a Landing Zone manually in the portal. You will make mistakes, and you will not be able to recreate it in a disaster. Always use Terraform or Bicep (Microsoft's IaC language).
2. **Ignoring Management Groups:** Just putting all Subscriptions in a flat list. This makes applying policies and permissions incredibly painful as you grow.
3. **Spoke-to-Spoke Peering:** Connecting application VNets directly to each other to save time. This bypasses your central firewall and is a massive security risk. Always route traffic through the Hub.

---

## 🎯 Key Takeaway
A Landing Zone is the foundational cloud architecture for an enterprise. It combines Identity, Organization, Networking, and Security into a cohesive, governed environment built entirely with Infrastructure as Code. It prepares the "digital city" so application teams can safely build their "buildings."

---

## ❓ Beginner FAQ

**Q1: Is a Landing Zone a specific Azure service I can buy?**
> No! A Landing Zone is an *architectural pattern*—a combination of many different Azure services (VNets, Policies, Management Groups, Firewalls) assembled in a specific way following Microsoft's best practices.

**Q2: What is "CAF" and how does it relate to Landing Zones?**
> CAF stands for **Cloud Adoption Framework**. It is Microsoft's massive guidebook on how to move to the cloud. The Landing Zone architecture is the technical implementation of the rules outlined in the CAF.

**Q3: Do I need a Landing Zone for my personal blog?**
> Definitely not. Landing Zones are designed for enterprise scale (dozens or hundreds of applications, large teams, strict security compliance). For a personal project or a startup's first app, a simple Resource Group and VNet is usually enough.

**Q4: What is the `Azure/caf-enterprise-scale` Terraform module?**
> Microsoft provides an official, massive, pre-written chunk of Terraform code that automatically deploys a best-practice Landing Zone. Instead of writing 10,000 lines of code yourself, you just use their module and customize the settings for your company.
