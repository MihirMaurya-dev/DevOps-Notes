---
tags: [terraform, azure, networking, azurerm_subnet]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🔲 Terraform Resource: azurerm_subnet

> "If a VNet is a large plot of land, a Subnet is drawing lines on the grass to say 'This is where the web servers go, and this is where the databases go.'"

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What a **VNet** is in Azure and Terraform — see [[VNet]]
- What **Subnets** are conceptually (including the 5 reserved IPs rule!) — see [[04-Subnets|Subnets]]
- How to write a Terraform loop (`for_each`) — see [[20-Loops-Conditionals|13-Loops-Conditionals]]

---

## 1. 🤔 What is `azurerm_subnet`?

### 🤔 What is it?

In Azure, a **Subnet** is a smaller, logically divided section carved out of your larger Virtual Network (VNet) address space. 

In Terraform, `azurerm_subnet` is the resource block used to carve out that section and give it a name.

> 🏢 **Real-World Analogy:**
> If the `azurerm_virtual_network` represents buying a 10-story office building, the `azurerm_subnet` represents assigning specific floors to different departments. 
> Floor 1 (Subnet A) is for the public lobby (Web Servers). 
> Floor 2 (Subnet B) is the private HR department (Databases). 

---

## 2. 🧠 Why do we need it?

You cannot place a Virtual Machine or a database directly into a VNet. They *must* be placed inside a Subnet. 

Why do we use Terraform to create Subnets instead of the Azure Portal?
1. **Bulk Creation:** Large enterprise networks often need 10 to 20 subnets. Clicking through the portal 20 times is tedious. With Terraform, we can use a `for_each` loop to create all 20 in seconds.
2. **Preventing Overlaps:** Terraform validates your code before deploying. If you accidentally type the same IP address range for two different subnets, Terraform catches the error before you break the network.

---

## 3. ⚙️ How does it work?

To create a subnet, the `azurerm_subnet` block needs to know exactly **four** things:
1. `name`: What to call this subnet (e.g., `snet-web`).
2. `resource_group_name`: The Resource Group where the parent VNet lives.
3. `virtual_network_name`: The exact name of the parent VNet this subnet belongs to.
4. `address_prefixes`: A list containing the CIDR block (IP range) for this specific subnet.

*(Note: Unlike most Azure resources, a subnet does NOT need a `location` argument, because it inherits its location from the parent VNet!)*

---

## 4. 💡 Real Example (Line-by-Line)

Here is how you create multiple subnets at once using a best-practice Terraform loop.

### `variables.tf` (The Inputs)
```hcl
# We define a MAP (a dictionary) of our subnets.
# This makes it super easy to add a new subnet later without copying blocks of code!
variable "subnets" {
  type = map(object({
    address_prefix = string
  }))
  description = "A map of subnets to create inside the VNet."
  
  default = {
    # Key = Name of the subnet
    "snet-frontend" = { address_prefix = "10.0.1.0/24" } # 251 usable IPs for web servers
    "snet-backend"  = { address_prefix = "10.0.2.0/24" } # 251 usable IPs for app servers
    "snet-database" = { address_prefix = "10.0.3.0/27" } # 27 usable IPs for databases
  }
}

# We also need the names of the VNet and Resource Group that already exist
variable "vnet_name" {
  type    = string
  default = "vnet-hub-prod-eus"
}

variable "resource_group_name" {
  type    = string
  default = "rg-network-prod-eus"
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- THE RESOURCE BLOCK ----
# We only write ONE block, but Terraform will create THREE subnets because of the loop!
resource "azurerm_subnet" "multiple_subnets" {
  
  # "for_each" tells Terraform to loop through the variable map
  for_each             = var.subnets
  
  # each.key represents the name (e.g., "snet-frontend")
  name                 = each.key
  
  # The parent VNet and Resource Group
  resource_group_name  = var.resource_group_name
  virtual_network_name = var.vnet_name
  
  # each.value.address_prefix extracts the CIDR block from the map
  address_prefixes     = [each.value.address_prefix]
  
  # Optional: Service Endpoints allow secure connections to Azure PaaS services
  service_endpoints    = ["Microsoft.Storage", "Microsoft.KeyVault"]
}
```

### `outputs.tf` (The Results)
```hcl
# We output the IDs of all the subnets we just created so we can place VMs inside them later.
output "subnet_ids" {
  description = "A map of subnet names to their unique Azure IDs."
  # This returns a map like: {"snet-frontend" = "/subscriptions/.../snet-frontend"}
  value       = { for key, subnet in azurerm_subnet.multiple_subnets : key => subnet.id }
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Inline Subnets:** Sometimes beginners put `subnet { ... }` blocks directly inside the `azurerm_virtual_network` resource. **Never do this!** It makes it nearly impossible to attach Network Security Groups (NSGs) or manage the subnets independently later. Always use the standalone `azurerm_subnet` resource shown above.
2. **Forgetting the 5 Reserved IPs:** If you create a `/29` subnet (8 total IPs), Azure instantly reserves 5 of them. You only have 3 left for your VMs! Always plan your `address_prefixes` generously.
3. **Misspelling the Bastion Subnet:** If you are creating a subnet for Azure Bastion, the `name` argument **MUST** be exactly `"AzureBastionSubnet"`. If you name it "snet-bastion", the Azure Bastion service will refuse to deploy.

---

## 6. 🎯 Key Takeaway

The `azurerm_subnet` resource divides your VNet into usable segments. Best practice dictates using a `for_each` loop to deploy them based on a map variable, and you should **never** define them inline inside the VNet resource.

---

## 7. ❓ Beginner FAQ

**Q1: Why does `address_prefixes` have an 's' and take a list `[]`, when it usually only has one CIDR block?**
> Azure technically supports adding multiple IPv4 or IPv6 address ranges to a single subnet (though it's rare in basic setups). Because it *can* support more than one, the Terraform provider requires you to provide it as a list, even if it only has one item.

**Q2: What are `service_endpoints`?**
> Normally, if a Virtual Machine in your subnet wants to talk to an Azure Storage Account, the traffic travels out over the public internet. By adding `"Microsoft.Storage"` to the `service_endpoints` list, Azure creates a private, hidden tunnel on the Microsoft backbone network directly from your subnet to the Storage Account. It's much faster and more secure!

**Q3: Does a subnet get tags?**
> No! Unlike Resource Groups and VNets, the Azure Subnet resource does not support tags. It inherits its billing and organizational grouping from its parent VNet.
