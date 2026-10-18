---
tags: [terraform, azure, networking, azurerm_network_security_group]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🛡️ Terraform Resource: azurerm_network_security_group

> "An NSG is a bouncer with a clipboard, standing at the door of your subnet. If you aren't on the list, you don't get in."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What an **NSG (Network Security Group)** actually is — see [[NSG]]
- What a **Subnet** is — see [[08-Subnet|Subnet]]
- How to write a Terraform **dynamic block** — see [[20-Loops-Conditionals|13-Loops-Conditionals]]

---

## 1. 🤔 What is `azurerm_network_security_group`?

### 🤔 What is it?

In Azure, a **Network Security Group (NSG)** is a cloud firewall. It uses a list of rules (Allow port 80, Deny port 22) to filter traffic going in and out of a subnet or a virtual machine.

In Terraform, the `azurerm_network_security_group` is the resource block you write to create that firewall and define its rules.

> 🏢 **Real-World Analogy:**
> Imagine a high-security office building. The building manager creates a master "Security Policy" document that lists who is allowed into which rooms. 
> 
> The `azurerm_network_security_group` is the code you write to generate that master Security Policy document.

---

## 2. 🧠 Why do we need it?

If you deploy servers in the cloud without a firewall, they are sitting naked on the internet. Automated bots will find them and try to hack them within minutes.

Why write it in Terraform instead of clicking in the portal?
Because security rules are incredibly easy to mess up. By writing them in Terraform:
1. **Peer Review:** Another developer can review your pull request to make sure you didn't accidentally open port 22 (SSH) to the entire internet.
2. **Reusability:** You can write a strict "baseline" NSG template and apply it to 50 different subnets instantly.

---

## 3. ⚙️ How does it work?

In Terraform, there are two ways to add rules to an NSG. Understanding the difference is critical:

**1. Inline Rules (The Best Practice for Enterprise):**
You define the rules *inside* the `azurerm_network_security_group` block. In enterprise environments, we use a `dynamic` block and a loop to read rules from a list of variables, keeping the code clean.

**2. Standalone Rules (The Messy Way):**
You use completely separate `azurerm_network_security_rule` blocks for every single rule. If you have 20 rules, you write 20 separate blocks of code. This is very repetitive and hard to read.

> ⚠️ **CRITICAL RULE:** Pick ONE method and stick to it. If you mix Inline Rules and Standalone Rules on the same NSG, Terraform gets confused and they will fight each other in a never-ending loop of deleting and recreating rules.

---

## 4. 💡 Real Example (Line-by-Line)

Here is the industry-standard way to deploy an NSG using **Dynamic Inline Rules**.

### `variables.tf` (The Inputs)
```hcl
# We define a MAP of objects. Each object represents one security rule.
# This makes it super easy to add a new rule: just add one item to this list!
variable "nsg_rules" {
  type = map(object({
    priority                   = number
    direction                  = string
    access                     = string
    protocol                   = string
    source_port_range          = string
    destination_port_range     = string
    source_address_prefix      = string
    destination_address_prefix = string
  }))
  
  description = "A list of security rules for the NSG."
  
  default = {
    # Rule 1: Allow web traffic (HTTP on port 80)
    "allow_web" = {
      priority                   = 100
      direction                  = "Inbound"
      access                     = "Allow"
      protocol                   = "Tcp"
      source_port_range          = "*"
      destination_port_range     = "80"
      source_address_prefix      = "Internet"
      destination_address_prefix = "*"
    }
    # Rule 2: Deny all other traffic
    "deny_all" = {
      priority                   = 4096
      direction                  = "Inbound"
      access                     = "Deny"
      protocol                   = "*"
      source_port_range          = "*"
      destination_port_range     = "*"
      source_address_prefix      = "*"
      destination_address_prefix = "*"
    }
  }
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- RESOURCE 1: Create the NSG ----
resource "azurerm_network_security_group" "nsg" {
  name                = "nsg-frontend-prod"
  location            = "eastus"
  resource_group_name = "rg-network-prod"

  # The "dynamic" block acts like a loop.
  # It will stamp out a "security_rule" block for every item in our variable map.
  dynamic "security_rule" {
    for_each = var.nsg_rules
    
    content {
      name                       = security_rule.key  # e.g., "allow_web"
      priority                   = security_rule.value.priority
      direction                  = security_rule.value.direction
      access                     = security_rule.value.access
      protocol                   = security_rule.value.protocol
      source_port_range          = security_rule.value.source_port_range
      destination_port_range     = security_rule.value.destination_port_range
      source_address_prefix      = security_rule.value.source_address_prefix
      destination_address_prefix = security_rule.value.destination_address_prefix
    }
  }
}

# ---- RESOURCE 2: Attach the NSG to a Subnet ----
# Creating the NSG is like printing the security policy.
# You still have to hand it to the bouncer at the door!
resource "azurerm_subnet_network_security_group_association" "association" {
  subnet_id                 = azurerm_subnet.frontend.id  # Assuming this subnet exists
  network_security_group_id = azurerm_network_security_group.nsg.id
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Forgetting the Association Resource:** Beginners often write the `azurerm_network_security_group` block and think they are done. Creating an NSG does *absolutely nothing* until you actively link it to a subnet using the `azurerm_subnet_network_security_group_association` block!
2. **Mixing Inline and Standalone Rules:** As mentioned above, if you mix a `dynamic "security_rule"` block inside the NSG with an external `azurerm_network_security_rule` resource, Terraform will go into a perpetual state war, deleting the standalone rule every time it runs.
3. **Pasting "Any-Any" Rules:** Using `source_address_prefix = "*"` and `destination_port_range = "22"` (SSH) allows the entire internet to try and hack into your Linux servers. Never do this.

---

## 6. 🎯 Key Takeaway

The `azurerm_network_security_group` creates a firewall policy for your cloud resources. In professional environments, you should use a `dynamic` block to loop through a variable map of rules to keep your code clean, and you must **never** forget to associate the NSG with a subnet using the separate association resource.

---

## 7. ❓ Beginner FAQ

**Q1: Why is the subnet association a completely separate resource? Why isn't it just a property inside the Subnet or NSG blocks?**
> HashiCorp designed it this way to prevent "circular dependency" errors. If the Subnet block required the NSG name, and the NSG block required the Subnet name, Terraform wouldn't know which one to build first! By making the association a separate 3rd piece, Terraform can build the Subnet, build the NSG, and *then* glue them together.

**Q2: What is the `priority` number in a security rule?**
> Azure processes rules in order from lowest number to highest number (e.g., 100, then 101, then 200). The first rule that matches the traffic wins. If Rule 100 says "Allow" and Rule 200 says "Deny", the traffic is allowed because 100 is checked first.

**Q3: Can I attach one NSG to multiple subnets?**
> Yes! You can write multiple `azurerm_subnet_network_security_group_association` blocks linking the exact same NSG to 5 different subnets. This is great for enforcing a standard baseline policy across your company.