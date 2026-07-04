---
tags: [interview, terraform, hcl, state, modules]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Terraform: High-Quality Interview Questions

These questions test your deep understanding of Terraform's architecture, state management, and HCL logic. They are designed to mimic real-world scenario questions asked during DevOps or Cloud Engineering interviews.

---

## Question 1: The State File Catastrophe
**Scenario:** 
You have a Terraform project deploying your company's production databases. An engineer accidentally deleted the `terraform.tfstate` file from your Azure Storage Account backend. The next day, you run `terraform apply` to add a new tag to the database.

**Question:** 
What exactly will Terraform attempt to do when you run the apply? How do you fix the missing state file without causing downtime?

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>What will happen:</b> Because the state file is missing, Terraform looks at your HCL code and believes <i>nothing</i> has been deployed yet. It will attempt to recreate the production database from scratch. In Azure, because the database name already exists, the deployment will fail with a "Resource Already Exists" error. If it were a resource that supported duplicate names, it would spin up a brand new, empty database alongside the old one!<br><br>
<b>How to fix it:</b> You absolutely must <i>not</i> run `apply`. You must run the `terraform import` command (or use import blocks) to manually pull the existing cloud resources back into a newly generated state file. Alternatively, if Blob Versioning was enabled on the Azure Storage Account (as per best practice), you could simply restore the previous version of the `.tfstate` file.
</details>

---

## Question 2: The `depends_on` Anti-Pattern
**Scenario:**
A junior engineer wrote Terraform code to deploy an Azure Virtual Network and a Subnet. They added `depends_on = [azurerm_virtual_network.main]` inside the Subnet resource block to ensure the VNet is built first. 

**Question:**
Is this `depends_on` block necessary? Explain how Terraform builds its execution graph and why explicitly using `depends_on` is generally considered an anti-pattern.

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>No, the `depends_on` block is completely unnecessary here.</b><br><br>
Terraform is a declarative language that builds a <b>Directed Acyclic Graph (DAG)</b> to determine execution order. When the subnet block references the VNet's name (e.g., `virtual_network_name = azurerm_virtual_network.main.name`), Terraform's engine automatically detects this implicit dependency. It knows it <i>must</i> build the VNet first to get the name to pass to the subnet.<br><br>
Using explicit `depends_on` is considered an anti-pattern because it forces Terraform to wait, often slowing down parallel resource creation. It should only be used in rare "hidden dependency" scenarios (e.g., waiting for an RBAC role assignment to propagate before starting a Virtual Machine script) where Terraform cannot detect the connection through variables.
</details>

---

## Question 3: The `dynamic` Block vs `count`
**Scenario:**
You need to deploy 5 Virtual Machines, but you also need to apply 10 different inbound security rules to a single Network Security Group (NSG). 

**Question:**
Which Terraform looping mechanism (`count`/`for_each` vs `dynamic` block) would you use for the VMs, and which would you use for the NSG rules? Explain the fundamental difference between them.

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>For the VMs:</b> You would use `count` or `for_each` on the `azurerm_linux_virtual_machine` resource. <br>
<b>For the NSG Rules:</b> You would use a `dynamic` block inside the `azurerm_network_security_group` resource.<br><br>
<b>The Difference:</b><br>
- `count` and `for_each` are used to stamp out entirely separate <b>Resource Blocks</b>. If you use `count = 5`, Terraform creates 5 distinct Virtual Machine resources in the state file.<br>
- `dynamic` blocks are used to stamp out <b>Nested Blocks</b> <i>inside</i> a single resource. A Network Security Group is only one Azure resource, but it requires multiple `security_rule {}` sub-blocks inside it. A dynamic block loops through a variable map to generate those inner sub-blocks cleanly without duplicating the parent resource.
</details>

---

## Question 4: Module Variable Traps
**Scenario:**
You wrote a brilliant Terraform Module that deploys a complete Web App environment. You hardcoded the region as `location = "eastus"` directly inside the module's `main.tf` file. Your team in Europe tries to use your module to deploy to `westeurope`.

**Question:**
Why is hardcoding the location an anti-pattern in module design? How must you alter the module to allow the European team to use it without changing your module's source code?

<details>
<summary><b>Show Answer</b></summary>
<br>
Hardcoding values inside a module defeats the entire purpose of modularity, which is <b>reusability</b>. If a value is hardcoded, the module can only ever be used for that exact specific scenario.<br><br>
To fix this, you must "parameterize" the module. <br>
1. Inside the module, you declare a variable: `variable "location" {}`.<br>
2. You replace the hardcoded string in the module's code with `location = var.location`.<br>
3. When the European team calls the module in their root code, they pass the parameter in: <br>
```hcl
module "web_app" {
  source   = "./modules/webapp"
  location = "westeurope"
}
```
</details>
