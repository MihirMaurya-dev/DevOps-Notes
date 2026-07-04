---
category: Terraform
tags: [terraform, locals, hcl, fundamentals, architecture]
type: fundamental
status: active
level: beginner
---

# Terraform Locals

## 📖 Before You Read
- Understand what Variables are by reading [[05-Variables]].

## 🤔 What is it?
If Variables are the inputs provided by the user from the *outside*, **Locals** are internal calculations and fixed values defined on the *inside* of your code. 

A local value allows you to assign a name to a complex calculation or a hardcoded piece of data, so you can reuse that name multiple times without repeating the calculation. 

**Analogy:** Imagine a restaurant recipe. A Variable is like asking the customer, "How spicy do you want this?" (Input from the outside). A Local is like the chef's secret sauce recipe written on the wall. The chef might combine "2 parts garlic + 1 part chili" and call it "SecretSauce." Whenever the recipe calls for "SecretSauce," the chef knows exactly what it means. The customer cannot change the "SecretSauce" recipe from the outside.

## 🧠 Why do we need it?
To keep code clean and prevent mistakes. For example, in large companies, cloud resources must follow strict naming rules (e.g., `az-appname-environment-region`). Instead of forcing the user to type out that long, complicated string perfectly every time, you can ask the user for the simple parts (app name, environment) via Variables, and then use a Local to stick them together programmatically.

## ⚙️ How does it work?
You define a `locals` block in your code. Inside, you can define as many local values as you want. You can combine text, do math, merge lists, or combine existing Variables.
Unlike variables, Locals *cannot* be modified by typing a command in the terminal or editing a `.tfvars` file. They are strictly locked inside the code.

## 💡 Real Example
Here is how you use Locals to enforce a strict naming convention and apply a standard set of tags to resources.

```hcl
# We take simple variables from the user
variable "workload" { default = "billing" }
variable "environment" { default = "prod" }
variable "location_abbr" { default = "eus" }

# We calculate the Locals internally
locals {
  # We stitch the variables together to create a strict prefix
  # Result: "az-billing-prod-eus"
  resource_prefix = "az-${var.workload}-${var.environment}-${var.location_abbr}"
  
  # We define a standard set of "Tags" (sticky notes) that every resource must have
  standard_tags = {
    Environment  = var.environment
    ManagedBy    = "Terraform"
    Architecture = "Hub-and-Spoke"
  }
}

# We use the calculated Locals when building the actual resource
resource "azurerm_virtual_network" "hub" {
  # We reference it using "local." (Notice it's singular!)
  name                = "${local.resource_prefix}-vnet" # Results in "az-billing-prod-eus-vnet"
  location            = "eastus"
  resource_group_name = "rg-hub"
  
  # We inject the whole block of tags instantly
  tags = local.standard_tags
}
```

## ⚠️ Common Mistakes Beginners Make
- **Typing `locals.` instead of `local.`:** When you *create* the block, it is plural: `locals {}`. When you *reference* the value inside a resource, it is singular: `local.resource_prefix`.
- **Overusing Locals for everything:** If a value might need to change depending on the environment (like a server size), it should be a Variable, not a Local.

## 🎯 Key Takeaway
Locals are internal, non-overrideable constants and calculations that help you keep your Terraform code clean, standardized, and "DRY" (Don't Repeat Yourself).

## ❓ Beginner FAQ

**Q: What is the primary difference between a Variable and a Local?**
A: Variables are inputs passed in from the outside (by the user or pipeline). Locals are internal logic and cannot be changed from the outside.

**Q: Can a Local reference another Local?**
A: Yes! As long as you don't create a circular dependency (Local A relies on Local B, and Local B relies on Local A), a local can totally reference another local.

**Q: I have 10 Virtual Machines. They all need the 3 standard tags, but each one needs 1 unique tag. How do I do this?**
A: You define the 3 common tags in a `locals` block. Inside the VM resource block, you use the `merge()` function to combine the `local.standard_tags` with the unique tag specific to that VM.

---
**See Also:**
- [[05-Variables]]
- [[13-Loops-Conditionals]]
- [[01-Terraform/Resource-Library/Resource-Group|Resource Group]]
- [[CAF-Mapping]]