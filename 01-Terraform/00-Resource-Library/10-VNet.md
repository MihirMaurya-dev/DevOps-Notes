---
tags: [terraform, azure, networking, azurerm_virtual_network]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🌐 Terraform Resource: azurerm_virtual_network

> "A Virtual Network is the empty plot of land you buy before you can build any houses (servers) in Azure."

---

## 📖 Before You Read

Before writing Terraform code for a VNet, you should understand the theory behind it. Please read:
- What a **VNet** actually is — see [[VNet]]
- What **CIDR** (IP address ranges) means — see [[02-IP-Addressing-and-CIDR|IP-Addressing-and-CIDR]]
- How to create a **Resource Group** (which holds the VNet) — see [[06-Resource-Group|Resource-Group]]

---

## 1. 🤔 What is `azurerm_virtual_network`?

### 🤔 What is it?

In Azure, a **Virtual Network (VNet)** is your private, isolated slice of the cloud network. 

In Terraform, the `azurerm_virtual_network` block is the code you write to create this private network.

> 🛣️ **Real-World Analogy:**
> Imagine you are a real estate developer building a new gated community. The very first thing you do is buy a giant plot of land and draw a big fence around it. You haven't built any streets or houses yet, but you've claimed the space.
>
> The `azurerm_virtual_network` is the code that buys that plot of land and draws the fence. The `address_space` (CIDR block) tells Azure exactly how big that plot of land is (how many IP addresses fit inside the fence).

---

## 2. 🧠 Why do we need it?

If you want to deploy Virtual Machines, databases, or private applications in Azure, they need an IP address to communicate. They must be placed inside a VNet.

Why write it in Terraform? 
Because networking is the most critical part of your infrastructure. If someone accidentally clicks the wrong button in the Azure Portal and deletes a VNet, your entire company goes offline. By writing it as Terraform code, the network is version-controlled, auditable, and easily reproducible.

---

## 3. ⚙️ How does it work?

To create a VNet in Terraform, you must provide:
1. `name`: What to call the network.
2. `resource_group_name`: Which "folder" to put it in.
3. `location`: Which Azure datacenter physically hosts the network.
4. `address_space`: A list of IP address ranges (written in CIDR notation, like `10.0.0.0/16`) that belong to this network.

*(Optional)* `dns_servers`: If your company has custom DNS servers (servers that translate names like `google.com` into IP addresses), you can specify them. Otherwise, Azure provides a default one automatically.

---

## 4. 💡 Real Example (Line-by-Line)

Here is the exact code to deploy a VNet.

### `variables.tf` (The Inputs)
```hcl
variable "vnet_name" {
  type        = string
  description = "The name of the Virtual Network."
  default     = "vnet-hub-prod-eus" # 'vnet' = resource type, 'hub' = purpose, 'prod' = env, 'eus' = East US
}

variable "resource_group_name" {
  type        = string
  description = "The name of the resource group this VNet will live inside."
}

variable "location" {
  type        = string
  description = "The Azure region (must match the Resource Group usually)."
}

# Notice this is a LIST of strings, because a VNet can have multiple address ranges!
variable "address_space" {
  type        = list(string)
  description = "The IP address ranges that belong to this VNet."
  default     = ["10.0.0.0/16"] # /16 gives us ~65,000 IP addresses
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- THE RESOURCE BLOCK ----
# "azurerm_virtual_network" is the official Microsoft resource type.
# "main" is our local Terraform nickname for it.
resource "azurerm_virtual_network" "main" {
  
  # 1. The name of the VNet
  name                = var.vnet_name
  
  # 2. Where it physically lives
  location            = var.location
  
  # 3. Which Resource Group it belongs to
  resource_group_name = var.resource_group_name
  
  # 4. The list of IP address ranges it owns
  address_space       = var.address_space

  # We attach some tags for billing/tracking
  tags = {
    Environment = "Production"
    Purpose     = "Hub Network"
  }
}
```

### `outputs.tf` (The Results)
```hcl
# Other resources (like Subnets) will need to know the name of this VNet
# so they can be placed inside it. We output those details here.
output "vnet_id" {
  description = "The unique Azure ID of the Virtual Network."
  value       = azurerm_virtual_network.main.id
}

output "vnet_name" {
  description = "The Name of the Virtual Network."
  value       = azurerm_virtual_network.main.name
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Inline Subnets:** Terraform allows you to define `subnet {}` blocks *inside* the `azurerm_virtual_network` block. **DO NOT DO THIS.** It causes massive headaches later when you try to add new subnets or manage security groups. Always use the separate `azurerm_subnet` resource!
2. **Overlapping Address Spaces:** If you create `VNet A` with `10.0.0.0/16` and `VNet B` with `10.0.0.0/16`, you will **never** be able to connect them together (VNet Peering). The IP addresses clash. Always plan your CIDR ranges on a spreadsheet before writing Terraform code!
3. **Making the VNet too small:** If you use `10.0.0.0/24`, you only get 256 IPs. If your company grows, you run out of space. Using a `/16` (65,000 IPs) is the standard best practice for an enterprise VNet.

---

## 6. 🎯 Key Takeaway

The `azurerm_virtual_network` resource carves out a private section of Azure's network for your use. Always define it using variables, give it a large enough `address_space` (like a `/16`), and **never** define subnets inline—always use a separate `azurerm_subnet` resource to keep your code clean and manageable.

---

## 7. ❓ Beginner FAQ

**Q1: Why is `address_space` a list? Can a VNet have more than one range?**
> Yes! You might start with `["10.0.0.0/16"]`. Five years later, your company buys another company and you run out of IPs. You can add a completely different range to the list: `["10.0.0.0/16", "172.16.0.0/16"]`. Both ranges now belong to the same VNet!

**Q2: Does creating an `azurerm_virtual_network` cost money?**
> No! The VNet itself is completely free. You only pay for things you put *inside* it (like Virtual Machines) or for data passing *between* VNets (VNet Peering data transfer costs).

**Q3: Can I change the `address_space` later?**
> Yes, but with a catch. You can easily ADD new address spaces. However, you CANNOT remove or shrink an address space if you already have resources (like VMs) actively using IP addresses in that range.

**Q4: I heard about "Azure DNS". Do I need to configure `dns_servers`?**
> By default, if you don't provide the `dns_servers` argument, Azure provides a magical hidden DNS server (`168.63.129.16`) that handles everything for you automatically. Only define `dns_servers` if your company has custom Active Directory Domain Controllers they want to use instead.
