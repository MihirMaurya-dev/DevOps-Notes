---
tags: [landing-zone, automation, devops, iac, terraform]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🤖 Platform Automation and DevOps

> "If you are clicking buttons in the Azure Portal to build your Landing Zone, you are doing it wrong. The cloud must be written as code."

---

## 📖 Before You Read
Before you dive into Platform Automation, make sure you understand:
- The concept of **Infrastructure as Code (IaC)** — see [[02-Introduction|Terraform Introduction]]
- What **CI/CD Pipelines** are — see [[01-Pipelines|Azure DevOps Pipelines]]

---

## 🤔 What is it?

**Platform Automation and DevOps** is the design area that dictates *how* the Landing Zone is actually built and maintained over time.

A Landing Zone contains hundreds of resources (Management Groups, Policies, VNets, Firewalls, Role Assignments). Managing these manually is impossible. Therefore, the entire Landing Zone must be defined as text files (code) and deployed using automated robots (pipelines).

> 🏭 **Real-World Analogy:**
> Imagine a car manufacturing plant. 
> You could have 50 mechanics manually bolting pieces together with wrenches (Clicking buttons in the Azure Portal). It is slow, people make mistakes, and every car comes out slightly different.
> 
> Or, you can spend a month programming massive robotic arms (Infrastructure as Code and Pipelines). Once programmed, you press a button, and the robots build 1,000 identical, perfect cars in a day. That is Platform Automation.

---

## 🧠 Why do we need it?

1. **Disaster Recovery (Immutability):** If a rogue administrator accidentally deletes your entire Hub Virtual Network, how long will it take to rebuild it from memory? Weeks. If it is defined in code, you run your pipeline and the network is rebuilt perfectly in 10 minutes.
2. **Auditing and Version Control:** When you click a button in the portal, there is no historical record of *why* you clicked it. When you use Git (code), every single change is tracked. You can see that "Alice modified the Firewall rules on Tuesday at 4 PM to allow traffic for Project X."
3. **Consistency:** Code doesn't suffer from typos on a Friday afternoon. If the code deploys successfully in the Development environment, it will deploy identically in the Production environment.

---

## ⚙️ How does it work? (The DevOps Workflow)

The architecture of a Landing Zone is brought to life using a standard DevOps workflow:

1. **The Code (Terraform/Bicep):** The Cloud Engineering team writes the infrastructure code. They use the official `Azure/caf-enterprise-scale` Terraform module to define the Management Groups and Policies.
2. **The Repository (Git):** They save this code into a secure repository, like GitHub or Azure Repos. 
3. **The Pull Request (Peer Review):** When an engineer wants to add a new Spoke VNet, they change the code and submit a Pull Request. Another engineer must review the code and approve it before it can be merged.
4. **The Pipeline (CI/CD):** Once approved, an automated system (like GitHub Actions or Azure DevOps) takes the code, authenticates to Azure securely, and runs `terraform apply` to physically build the new network in the cloud.

---

## 💡 Real Example (Policy as Code)

Imagine the security team wants to enforce a new rule: *"All Storage Accounts must block public network access."*

**The Bad Way:** An engineer logs into the portal and clicks through 50 subscriptions to manually apply the policy.
**The DevOps Way:** 
1. The engineer adds 5 lines of JSON to the Landing Zone code repository defining the new policy.
2. They commit the code.
3. The CI/CD pipeline runs overnight.
4. By morning, the pipeline has automatically applied the policy to the top-level Management Group, enforcing it instantly across the entire company.

---

## ⚠️ Common Mistakes Beginners Make

1. **"Click-Ops":** Using the Azure Portal UI to make quick "temporary" fixes to production environments. This causes **Configuration Drift**. The actual cloud environment no longer matches the Terraform code. The next time the pipeline runs, Terraform will overwrite and delete the manual fix!
2. **Hardcoding Secrets:** Committing Terraform code to Git that contains plain-text passwords or API keys. Hackers scan GitHub 24/7 for this exact mistake. Always use Azure Key Vault to inject secrets into the pipeline dynamically!

---

## 🎯 Key Takeaway
A Landing Zone must be treated like a software product. It must be defined entirely as Infrastructure as Code (Terraform or Bicep), stored in version control (Git), and deployed strictly through automated CI/CD pipelines to ensure consistency, security, and rapid disaster recovery.

---

## ❓ Beginner FAQ

**Q1: Should I use Terraform or Azure Bicep?**
> Both are excellent! Bicep is Microsoft's native language, meaning it gets new Azure features on Day 1. Terraform is third-party (HashiCorp), but it is cloud-agnostic, meaning you can use it to build AWS and Google Cloud Landing Zones as well. Terraform is currently the industry standard for large enterprises.

**Q2: Who is allowed to run the deployment pipeline?**
> In a true DevOps environment, no human runs the pipeline manually. The pipeline triggers automatically when code is successfully merged into the `main` branch after passing a peer review.
