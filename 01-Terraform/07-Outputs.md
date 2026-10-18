---
category: Terraform
tags: [terraform, outputs, hcl, fundamentals, data-flow]
type: fundamental
status: active
level: beginner
---

# Terraform Outputs

## 📖 Before You Read
- Make sure you understand Variables [[05-Variables]] and Resources [[04-Resources]].

## 🤔 What is it?
If Variables are the inputs passed *into* your Terraform code, **Outputs** are the return values that come *out* of your code after it runs. 

When Terraform builds things in the cloud, Azure often generates dynamic data that you couldn't possibly know beforehand. For example, if you ask Azure to create a new Public IP Address, Azure assigns a random string of numbers (like `203.0.113.50`). 

**Analogy:** Think of a vending machine. The Variable is the $1 bill you insert (Input). The Resource is the mechanism inside that grabs the soda. The Output is the actual can of soda dropping into the tray for you to collect (Return Value).

## 🧠 Why do we need it?
Without Outputs, all that dynamically generated data (IP addresses, Database connection strings, unique IDs) would be trapped inside Terraform's internal memory. 
We need Outputs to:
1. Show important information to the engineer on their screen when the deployment finishes.
2. Pass data to the *next* step in an automated pipeline. (e.g., Step 1: Build the database. Step 2: Give the database password to the application team).

## ⚙️ How does it work?
You write an `output` block. Inside, you define a `value`, which tells Terraform exactly which piece of information you want it to fetch from the newly built resources.
When you run `terraform apply`, Terraform builds the resources, queries Azure for the final properties, and prints the outputs to your terminal screen.

## 💡 Real Example
Here is how you capture the dynamically generated IP address of a new server.

```hcl
# We build a Public IP Resource. 
# Notice we don't know the actual IP address yet! Azure decides that.
resource "azurerm_public_ip" "frontend" {
  name                = "pip-frontend"
  location            = "eastus"
  resource_group_name = "rg-web"
  allocation_method   = "Static"
}

# We define an Output block to capture the final IP address
output "frontend_public_ip" {
  description = "The public IP address of the main application load balancer."
  
  # We reference the resource, and ask for its specific ".ip_address" property
  value       = azurerm_public_ip.frontend.ip_address
}

# Example of a more complex output: getting a list of IDs for all subnets
output "vnet_subnets" {
  description = "A map of all subnet names to their Azure Resource IDs."
  # This uses a 'for' loop to get data from multiple subnets at once
  value       = { for s in azurerm_subnet.spoke : s.name => s.id }
}
```

## ⚠️ Common Mistakes Beginners Make
- **Outputting secrets in plain text:** If your output is a database password, it will print right on your computer screen or inside the pipeline logs for everyone to see! You must tell Terraform to hide it by using the `sensitive = true` argument.
- **Trying to output data from a resource that doesn't exist yet:** An output depends on the resource being created successfully.

## 🎯 Key Takeaway
Output blocks extract dynamically generated data from your cloud resources and present it to the user or to automated pipelines.

## ❓ Beginner FAQ

**Q: How do I output a database password without showing it in the CI/CD logs?**
A: You add the argument `sensitive = true` inside the output block. Terraform will still capture the value, but it will display `<sensitive>` on the screen instead of the actual password.

**Q: Can you define an output that is not tied to a specific resource?**
A: Yes! Outputs can return any valid Terraform expression. You could output a hardcoded string, a local variable, or a mathematical calculation if you wanted to.

**Q: How are Outputs used with Terraform Modules?**
A: When you start breaking your code into reusable "Modules" (like mini-programs), Outputs are the only way a child module can pass data back up to the parent module. For example, a networking module outputs the Subnet ID, so a compute module can receive it and know where to put the Virtual Machine.

---
**See Also:**
- [[05-Variables]]
- [[10-Modules]]
- [[12-Data-Sources]]
- [[02-GitHub-Actions|GitHub-Actions]]