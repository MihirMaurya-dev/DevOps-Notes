---
tags: [terraform, azure, nat-gateway, azurerm_nat_gateway]
source: devopsinsiders/batch-18
created: 2026-08-01
level: beginner
---

# 🛡️ Terraform Resource: azurerm_nat_gateway

> "A NAT Gateway is the company mailroom for your Virtual Machines. It securely handles all outbound mail (internet requests) and stamps them with a single corporate address."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What a **Virtual Network (VNet)** and **Subnet** are — see [[VNet]] and [[08-Subnet|Subnet]]
- What a **Public IP** is — see [[Public-IP]]

---

## 1. 🤔 What is `azurerm_nat_gateway`?

### 🤔 What is it?

In Azure, a **NAT (Network Address Translation) Gateway** is a fully managed and highly resilient service that provides outbound-only internet connectivity for one or more subnets of a virtual network. 

In Terraform, the `azurerm_nat_gateway` block creates this resource, which you then link to a Public IP and a Subnet.

> 📁 **Real-World Analogy:**
> Imagine an office building where the employees (Virtual Machines) are not allowed to have their own direct outside phone lines (they don't have Public IPs). 
> When they need to call the outside world (the internet), they route their calls through the company Switchboard (the NAT Gateway). The Switchboard makes the call on their behalf using the company's main phone number (the NAT Gateway's Public IP). 
> If the outside world tries to call that number unprompted, the Switchboard blocks it. It is strictly for outbound calls and their direct replies.

---

## 2. 🧠 Why do we need it?

If a Virtual Machine in a private subnet (with no Public IP) tries to access the internet (e.g., to download `apt` updates, pull a Docker image, or reach an external API), Azure provides a default outbound access IP. 

However, this default IP is unpredictable, can change, and is shared. 
You need a **NAT Gateway** when:
1. **IP Whitelisting:** A third-party API or partner requires you to provide a static, unchanging IP address that they can whitelist on their firewall.
2. **Port Exhaustion:** You have hundreds of VMs making outbound requests simultaneously and need a dedicated gateway that can handle massive amounts of outbound traffic without dropping connections.
3. **Security:** You want strict, predictable, and outbound-only internet routing for your private tiers (like App and DB tiers).

---

## 3. ⚙️ How does it work?

Creating a functional NAT Gateway in Terraform is actually a 4-step process. You don't just create the gateway; you have to plug it in!
1. **Create a Public IP:** (Must be the `Standard` SKU).
2. **Create the NAT Gateway:** (`azurerm_nat_gateway`).
3. **Link the IP to the Gateway:** (`azurerm_nat_gateway_public_ip_association`).
4. **Link the Gateway to the Subnet:** (`azurerm_subnet_nat_gateway_association`).

---

## 4. 💡 Real Example (Line-by-Line)

Here is exactly how you write the Terraform code to create and associate a NAT Gateway.

### `variables.tf` (The Inputs)
```hcl
variable "nat_gateway_name" {
  type    = string
  default = "nat-myapp-prod-eus"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "resource_group_name" {
  type    = string
}

variable "subnet_id" {
  type        = string
  description = "The ID of the Subnet that needs outbound internet access."
}
```

### `main.tf` (The Actual Resource)
```hcl
# 1. First, we need a Public IP for the NAT Gateway to use
resource "azurerm_public_ip" "nat_pip" {
  name                = "${var.nat_gateway_name}-pip"
  location            = var.location
  resource_group_name = var.resource_group_name
  allocation_method   = "Static"
  sku                 = "Standard" # MUST be Standard for NAT Gateway
}

# 2. Create the NAT Gateway itself
resource "azurerm_nat_gateway" "main" {
  name                    = var.nat_gateway_name
  location                = var.location
  resource_group_name     = var.resource_group_name
  sku_name                = "Standard"
  idle_timeout_in_minutes = 4 # How long to keep inactive connections open
}

# 3. Associate the Public IP with the NAT Gateway
resource "azurerm_nat_gateway_public_ip_association" "pip_assoc" {
  nat_gateway_id       = azurerm_nat_gateway.main.id
  public_ip_address_id = azurerm_public_ip.nat_pip.id
}

# 4. Associate the NAT Gateway with your Subnet
resource "azurerm_subnet_nat_gateway_association" "subnet_assoc" {
  subnet_id      = var.subnet_id
  nat_gateway_id = azurerm_nat_gateway.main.id
}
```

### `outputs.tf` (The Results)
```hcl
output "nat_gateway_id" {
  description = "The ID of the NAT Gateway."
  value       = azurerm_nat_gateway.main.id
}

output "nat_gateway_public_ip" {
  description = "The static outbound Public IP used by the Subnet."
  value       = azurerm_public_ip.nat_pip.ip_address
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Forgetting the Associations:** It is incredibly common to write the `azurerm_nat_gateway` block and forget the `azurerm_subnet_nat_gateway_association`. Without the association, the NAT Gateway sits there doing absolutely nothing.
2. **Using a Basic SKU Public IP:** A NAT Gateway requires a `Standard` SKU Public IP. Using `Basic` will result in a Terraform apply failure.
3. **Trying to use it for Inbound Traffic:** A NAT Gateway cannot be used to host a website or accept incoming SSH connections. It is strictly for traffic *initiating* from inside Azure going out.

---

## 6. 🎯 Key Takeaway

The `azurerm_nat_gateway` provides secure, dedicated, and static outbound internet access for private subnets. Implementing it in Terraform requires managing four separate resources (the IP, the Gateway, and the two association links) to fully connect the circuit.

---

## 7. ❓ Beginner FAQ

**Q1: What happens if a VM in the subnet has its own Public IP?**
> If a VM has a Public IP attached directly to its Network Interface, its *inbound* traffic comes through that Public IP. However, all of its *outbound* traffic will override the VM's Public IP and be routed through the NAT Gateway's Public IP instead. 

**Q2: Can a NAT Gateway span multiple Availability Zones?**
> A single NAT Gateway resource is deployed to a specific Availability Zone (or no zone). However, subnets spanning multiple zones can all use the same NAT Gateway for outbound traffic.

**Q3: Can multiple subnets share one NAT Gateway?**
> Yes! You can create multiple `azurerm_subnet_nat_gateway_association` blocks to link many subnets within the same Virtual Network to a single NAT Gateway.
