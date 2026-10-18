---
tags: [landing-zone, governance, policy, compliance]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🏛️ Governance in the Landing Zone

> "Governance is the digital police force of your cloud environment. It ensures everyone follows the company rules, even when the security team is asleep."

---

## 📖 Before You Read
Before you dive into Governance, make sure you understand:
- What **CAF** is — see [[02-CAF-Overview|CAF-Overview]]
- The basics of **Resource Groups** — see [[14-Resource-Groups|Resource-Groups]]

---

## 🤔 What is it?

**Governance** is the set of rules, policies, and guardrails that a company puts in place to control what happens inside their cloud environment. 

In a traditional physical datacenter, governance is slow and manual. If you wanted a new server, you filled out a paper form, a manager signed it, and the security team checked it. In the cloud, developers can build servers in seconds using code. You cannot rely on paper forms anymore; you need *automated* governance.

> 🛣️ **Real-World Analogy:**
> Imagine a highway. The goal of the highway is to get cars to their destination as fast as possible. 
> But you can't just let people drive 200 mph on the wrong side of the road! You need **Governance**:
> - Speed Limits (Rules).
> - Guardrails on the side of cliffs (Prevention).
> - Traffic Cameras that issue tickets (Auditing/Reporting).
> 
> Governance doesn't stop people from driving; it just ensures everyone drives safely.

---

## 🧠 Why do we need it?

If a company hands 500 developers the keys to an ungoverned Azure environment, chaos will ensue within hours:
1. **Cost Explosions:** A developer will deploy the largest, most expensive Virtual Machine possible ($10,000/month) just to run a tiny script.
2. **Compliance Violations:** A team will deploy a database containing European citizen data into a US datacenter, massively violating GDPR privacy laws.
3. **Security Risks:** A junior engineer will spin up a storage account without a firewall, exposing corporate data to the public internet.

Governance prevents all of this automatically.

---

## ⚙️ How does it work? (Azure Policy)

In Azure, the primary tool for Governance is **Azure Policy**.

Azure Policy is a JSON document that evaluates your resources against business rules. 
When an engineer tries to create a resource, Azure Policy steps in and says "Hold on, let me check the rules."

### The 3 Main Effects of Azure Policy:
1. **Audit:** "I will let you create this unsecured server, but I am going to flag it in bright red on the security dashboard so your boss sees it."
2. **Deny:** "You are trying to build a server in Europe, but our rules say US only. I am instantly blocking the deployment. Error!"
3. **Append / Modify:** "You forgot to add the 'CostCenter' tag to this server. I will automatically add it for you behind the scenes."

---

## 💡 Real Example (The DevOps Workflow)

**The Problem:** The CFO is angry because cloud costs are too high. They demand that developers only use cheap `B-Series` (Basic) Virtual Machines for testing.

**The Governance Solution:**
The DevOps engineer writes an Azure Policy using Terraform. The policy states: *Allowed Virtual Machine SKUs = Standard_B1s, Standard_B2s*. 
They apply this policy to the "Development" Management Group.

The next day, a developer writes code to deploy a massive `E-Series` (Enterprise) memory-optimized server. When they run `terraform apply`, Azure Policy rejects the code instantly with a custom error message: *"Deployment Failed: You are only allowed to use B-Series VMs in this environment."* The CFO is happy, and the environment is governed!

---

## ⚠️ Common Mistakes Beginners Make

1. **Denying Everything (The Brick Wall):** Overzealous security teams often write so many strict "Deny" policies that developers literally cannot deploy anything. If governance blocks productivity, developers will find shadow-IT ways to bypass the cloud entirely. Always start with "Audit" policies to see what people are doing *before* switching them to "Deny."
2. **Managing Policies Manually:** Clicking through the Azure Portal to assign 100 different policies to 50 different subscriptions is a nightmare. Always use the Landing Zone Accelerator (Enterprise-Scale) Terraform modules to deploy your governance as code!

---

## 🎯 Key Takeaway
Governance is the automated enforcement of corporate rules in the cloud. Using tools like Azure Policy, you can automatically block expensive, insecure, or non-compliant deployments without slowing down developer velocity.

---

## ❓ Beginner FAQ

**Q1: What is the difference between Azure Policy and RBAC?**
> This is a classic interview question! 
> **RBAC (Role-Based Access Control)** dictates *WHO* can do something (e.g., "Alice is allowed to create Virtual Machines"). 
> **Azure Policy** dictates *WHAT* they can create (e.g., "Alice is only allowed to create Virtual Machines if they are in the East US region").

**Q2: What are Azure Resource Tags?**
> Tags are name/value pairs (like `Environment = Prod` or `Department = HR`) that you attach to resources. Governance relies heavily on tags to organize billing. You can use Azure Policy to *force* developers to add tags to their resources!
