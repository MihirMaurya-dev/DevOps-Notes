---
category: IaC-Fundamentals
tags:
  - terraform
  - iac
  - declarative
  - imperative
  - idempotency
  - architecture
type: fundamental
status: active
---
# Declarative vs. Imperative IaC

## The Core Concept
When provisioning cloud infrastructure, there are two fundamentally different paradigms for interacting with the provider's API (like the Azure Resource Manager):

* **Imperative (The "How"):** You write step-by-step instructions. You tell the system *how* to achieve the end state. 
  * *Examples:* Bash scripting, Azure CLI commands, PowerShell, or standard programming languages like C#.
* **Declarative (The "What"):** You describe the desired end state, and the execution engine figures out the steps required to get there. 
  * *Examples:* [[01-Introduction|Terraform]], ARM Templates, Kubernetes YAMLs.

Unlike imperative object-oriented languages like C# where you define specific execution logic, control flows, and methods, declarative languages like HashiCorp Configuration Language (HCL) simply define the required objects. You define that an Azure Resource Group *must exist*, and Terraform handles the creation, update, or deletion logic behind the scenes.

## Under the Hood
The magic of the declarative model relies entirely on **[[State-Theory|State Management]]**. 

When you run an imperative script twice, it will execute the exact same commands twice (often resulting in errors like "Resource Already Exists"). 

When you run a declarative Terraform configuration, the Terraform core engine performs a specific operational loop:
1. **Refresh:** Checks the current reality of the cloud environment.
2. **Compare:** Compares the current reality against your `terraform.tfstate` file and your `.tf` configuration files.
3. **Plan:** Calculates the delta (the exact API calls needed to make reality match your configuration).
4. **Apply:** Executes those specific changes.

This process guarantees **Idempotency**—the property that no matter how many times you run the operation, the end result remains exactly the same, with no unintended side effects.

## Why We Care in DevOps
1. **Drift Detection:** In enterprise environments, someone will inevitably make a manual change in the Azure Portal (Configuration Drift). Imperative scripts cannot fix this easily. A declarative `terraform plan` instantly detects the drift and `terraform apply` reverts the environment back to the documented code.
2. **Reviewability (GitOps):** Because declarative code describes the exact state of the infrastructure, pull requests become meaningful architectural reviews. Reviewers can see exactly *what* the infrastructure will look like, rather than having to mentally trace a 500-line bash script.
3. **Dependency Graphing:** You don't have to worry about the order of creation. If your Azure App Service depends on a specific Azure SQL Database, Terraform's engine automatically builds a Directed Acyclic Graph (DAG) to provision the database first. 

## Interview Questions
* **Q: Why would an enterprise choose Terraform over writing automated Azure CLI scripts in a CI/CD pipeline?**
  * *A:* Azure CLI scripts are imperative and lack built-in state awareness. Handling updates, deletions, or error recovery requires writing complex, custom idempotency logic. Terraform is declarative; it inherently understands the current state of the infrastructure and calculates the exact delta needed, reducing human error and maintenance overhead.
* **Q: Explain "Idempotency" in the context of Infrastructure as Code.**
  * *A:* Idempotency means that applying the same configuration multiple times will yield the exact same result without causing errors or duplicating resources. If I define one Virtual Machine and run the code ten times, I still only have one Virtual Machine.
* **Q: Can Terraform be used imperatively?**
  * *A:* While Terraform is inherently declarative, engineers sometimes force imperative behavior using `local-exec` or `remote-exec` provisioners to run scripts. This is generally considered an anti-pattern and should only be used as a last resort.

## Links to Implementation
* [[State-Theory]]: Deep dive into how the delta is calculated.
* [[04-Resources]]: Defining the declarative blocks in HCL.
* [[Terraform-Pipeline]]: How this theory applies inside GitHub Actions.
* [[Azure-Fundamentals]]: How the Azure Resource Manager (ARM) processes these declarative requests.