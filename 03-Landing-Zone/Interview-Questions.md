---
tags: [interview, landing-zone, architecture, caf]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Landing Zone Architecture: High-Quality Interview Questions

These questions test your deep understanding of Azure Landing Zones, CAF, Governance, and Subscription Democratization. They are designed to mimic real-world scenario questions asked during DevOps or Cloud Engineering interviews.

---

## Question 1: The Out-of-Control Cloud Bill
**Scenario:** 
You are hired as a Lead Cloud Engineer. The CFO is furious because the monthly Azure bill is $150,000, and they have no idea which departments are spending the money. They demand you "fix the billing transparency by tomorrow."

**Question:** 
How do you solve this issue using Resource Organization and Governance? Walk through the technical steps.

<details>
<summary><b>Show Answer</b></summary>
<br>
The solution is a strict <b>Tagging Strategy enforced by Azure Policy</b>.<br><br>
<b>Step 1:</b> Define mandatory tags (e.g., `CostCenter`, `Department`, `Owner`).<br>
<b>Step 2:</b> Write an Azure Policy using the `Deny` effect. The policy states: "If anyone attempts to create a Resource Group without these tags, block the deployment." Apply this policy to the top-level Management Group so it inherits down to all subscriptions.<br>
<b>Step 3:</b> Write a second Azure Policy using the `Modify` or `DeployIfNotExists` effect. This policy states: "Any Virtual Machine or database created inside a Resource Group automatically inherits the tags of that Resource Group."<br><br>
Now, developers are physically forced to provide billing codes, and the CFO can use Azure Cost Management to instantly generate pie charts showing exactly which department spent the $150,000.
</details>

---

## Question 4: Subscription Democratization
**Scenario:**
A startup is migrating to Azure. The lead developer says: "Let's keep things simple. We will create one massive Azure Subscription called 'Startup-Prod' and put all our Dev, Test, and Production servers inside it, separated by Resource Groups."

**Question:**
As the Cloud Architect, why do you strongly disagree with this approach? Provide at least two technical reasons why "Subscription Democratization" is critical.

<details>
<summary><b>Show Answer</b></summary>
<br>
I disagree because a single-subscription model creates massive risk and prevents scaling. <br><br>
<b>Reason 1: Azure Quotas and Hard Limits.</b> Azure places hard limits on resources per subscription (e.g., maximum number of ExpressRoute circuits or Storage Accounts). By dumping everything into one subscription, you will eventually hit these physical limits and break production. Subscriptions are the primary unit of scale; separating workloads into different subscriptions multiplies your limits.<br><br>
<b>Reason 2: Security Blast Radius.</b> A Subscription is a hard security boundary. If Dev and Prod are in the same subscription, a developer with "Contributor" rights could accidentally run a Terraform script that deletes the Production database instead of the Dev database. By placing them in separate subscriptions under different Management Groups, you eliminate the risk of accidental cross-environment destruction.
</details>

---

## Question 3: Policy Effects
**Scenario:**
You need to ensure that every Virtual Machine deployed in your Landing Zone has the Azure Monitor Agent installed. You assign an Azure Policy with the `Deny` effect to enforce this. The next day, the development team complains that all their automated CI/CD pipelines are failing.

**Question:**
Why did their pipelines fail, and which Policy Effect should you have used instead to achieve your goal without breaking their automation?

<details>
<summary><b>Show Answer</b></summary>
<br>
Their pipelines failed because the developers' Terraform code did not explicitly include the Azure Monitor Agent extension. The `Deny` effect acts as a brick wall; if the configuration isn't perfect, it blocks the entire VM deployment.<br><br>
Instead, you should have used the <b>DeployIfNotExists (DINE)</b> or <b>Modify</b> effect. <br>
With DINE, the developer's pipeline would successfully deploy the plain VM. Then, Azure Policy would detect the missing agent and silently trigger a background deployment to install it for them. This achieves 100% compliance without breaking developer velocity.
</details>

---

## Question 4: Management Group Inheritance
**Scenario:**
You have a Management Group structure: Root -> "Landing Zones" -> "Online Apps". 
At the "Landing Zones" level, you assign an Azure Policy stating: "Only allow deployments in the `East US` region."
At the "Online Apps" level, a junior engineer assigns an Azure Policy stating: "Allow deployments in `East US` and `West Europe`."

**Question:**
A developer attempts to deploy a Web App to `West Europe` inside a subscription under the "Online Apps" Management Group. Will the deployment succeed or fail? Why?

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>The deployment will fail.</b><br><br>
In Azure Policy, when rules conflict, the most restrictive rule (or the <b>Deny</b> action) always wins, regardless of where it is in the hierarchy.<br><br>
Because the parent Management Group ("Landing Zones") explicitly restricts deployments to <i>only</i> `East US`, that restriction flows down. The junior engineer's policy at the lower level cannot override or bypass a restrictive policy set higher up in the tree.
</details>
