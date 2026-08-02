---
tags: [terraform, azure, network-interface, nic, azurerm_network_interface]
source: devopsinsiders/batch-18
created: 2026-08-01
level: beginner
---

# 🔌 Terraform Resource: azurerm_network_interface

> "A Network Interface is the plug that connects your Virtual Machine to the Virtual Network."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What a **Virtual Network (VNet)** and **Subnet** are — see [[VNet]] and [[Subnet]]
- What a **Public IP** is — see [[Public-IP]]

---

## 1. 🤔 What is `azurerm_network_interface`?

### 🤔 What is it?

In Azure, a **Network Interface (NIC)** is a critical networking resource that serves as the bridge between a Virtual Machine (VM) and a Virtual Network (VNet). 

In Terraform, the `azurerm_network_interface` block creates this plug. Without a NIC, a Virtual Machine cannot communicate with other Azure resources, the internet, or on-premises networks.

> 📁 **Real-World Analogy:**
> Think of a Virtual Machine like a brand-new desktop computer you just bought. It has power and storage, but no internet. 
> To connect it to your home router, you need an Ethernet port on the back of the PC, and an Ethernet cable plugged into it. 
> The `azurerm_network_interface` represents that physical Ethernet port and cable, firmly plugging your VM into the Azure Subnet.

---

## 2. 🧠 Why do we need it?

Azure intentionally decouples the Network Interface from the Virtual Machine. They are separate resources. This design is powerful because:
1. **Flexibility:** You can delete a VM but keep the NIC (and its static private IP) to attach to a new VM later.
2. **Multiple IPs:** A single NIC can hold multiple IP configurations (e.g., a primary IP and a secondary IP).
3. **Multi-NIC VMs:** Large enterprise appliances (like a firewall VM) might need multiple NICs to connect to different subnets (e.g., one NIC in an "Untrusted" subnet and one in a "Trusted" subnet).

---

## 3. ⚙️ How does it work?

The `azurerm_network_interface` block requires:
1. `name`, `location`, `resource_group_name`: Standard Azure resource parameters.
2. `ip_configuration`: A mandatory sub-block where you specify:
   - A name for the configuration (usually just "internal" or "ipconfig1").
   - The `subnet_id` to plug into.
   - The `private_ip_address_allocation` (Dynamic or Static).
   - (Optional) A `public_ip_address_id` if you want it accessible from the internet.

---

## 4. 💡 Real Example (Line-by-Line)

### `variables.tf` (The Inputs)
```hcl
variable "nic_name" {
  type    = string
  default = "nic-myapp-web-01"
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
  description = "The ID of the Subnet where this NIC will live."
}

# Optional Public IP ID
variable "public_ip_id" {
  type        = string
  default     = null
}
```

### `main.tf` (The Actual Resource)
```hcl
resource "azurerm_network_interface" "main" {
  name                = var.nic_name
  location            = var.location
  resource_group_name = var.resource_group_name

  # The IP Configuration block tells the NIC how to get an IP address
  ip_configuration {
    name                          = "internal" # Just a logical name for this block
    subnet_id                     = var.subnet_id
    private_ip_address_allocation = "Dynamic"  # Azure assigns a private IP automatically

    # If a public_ip_id was provided, attach it. Otherwise, ignore it.
    public_ip_address_id          = var.public_ip_id
  }
}
```

### `outputs.tf` (The Results)
```hcl
output "nic_id" {
  description = "The ID of the Network Interface (to attach to a VM)."
  value       = azurerm_network_interface.main.id
}

output "private_ip_address" {
  description = "The Private IP assigned to this NIC."
  value       = azurerm_network_interface.main.private_ip_address
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Trying to assign an IP inside the VM block:** You cannot assign IP addresses, subnets, or Public IPs directly in an `azurerm_linux_virtual_machine` block. All IP networking MUST be done on the `azurerm_network_interface`. The VM block will only ask for the `network_interface_ids`.
2. **Hardcoding Private IPs:** While you can set `private_ip_address_allocation = "Static"` and provide a specific `private_ip_address = "10.0.1.4"`, it is highly discouraged unless strictly necessary (like for a Domain Controller). Using "Dynamic" avoids IP conflict headaches; Azure guarantees the VM will keep that dynamic IP for its lifetime anyway.
3. **Forgetting NSG Association:** Creating a NIC and a Network Security Group (NSG) separately doesn't link them automatically. You must use the `azurerm_network_interface_security_group_association` resource to actually apply the firewall rules to the NIC.

---

## 6. 🎯 Key Takeaway

The `azurerm_network_interface` is the glue between your Virtual Machines and your Virtual Network. Always configure your Private and Public IPs on the NIC, and then pass the NIC's output `id` to the Virtual Machine resource.

---

## 7. ❓ Beginner FAQ

**Q1: Can I attach multiple Public IPs to one NIC?**
> Yes, Azure supports assigning multiple IP configurations to a single NIC, and each configuration can have its own Public IP if needed.

**Q2: What happens to the Private IP if I reboot the VM?**
> Even if you use `Dynamic` allocation, the Private IP assigned by Azure is reserved for that NIC as long as the VM exists. A simple reboot will not change the Private IP. It is only released if the VM is completely deallocated or the NIC is destroyed.
