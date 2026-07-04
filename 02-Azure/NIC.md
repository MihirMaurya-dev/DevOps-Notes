---
tags: [azure, networking, nic, compute]
source: devopsinsiders/batch-18
created: 2026-06-14
updated: 2026-06-14
---

# Network Interfaces (NIC)

A Network Interface (NIC) is the interconnection between a Virtual Machine (VM) and an Azure Virtual Network (VNet). While they are often created implicitly when deploying a VM via the Azure Portal, in Infrastructure as Code (Terraform), they are distinct, standalone resources.

## Key Concepts

1. **Independent Lifecycle:**
   - A NIC exists independently of a VM. If you delete a VM, the NIC remains unless explicitly deleted. 
   - You can detach a NIC from one VM and attach it to another, which is useful for migrating IP addresses or preserving NSG associations.

2. **IP Configuration:**
   - A NIC holds the Private IP address assignment (Dynamic or Static) from the subnet it is connected to.
   - If a VM needs a Public IP address, that Public IP is attached to the NIC, *not* the VM directly.

3. **NSG Association:**
   - Network Security Groups (NSGs) can be associated directly with a NIC or with the Subnet the NIC is in.
   - **Best Practice:** Always associate NSGs at the Subnet level to ensure consistent security policies across all VMs in that tier. Avoid attaching NSGs to individual NICs unless it is a very specific edge case (like a management jumpbox), as it creates management overhead and conflicting rules.

4. **Multiple NICs:**
   - An Azure VM can have multiple NICs attached to it (useful for network appliances like Firewalls or load balancers).
   - One NIC must be designated as the "Primary" NIC.

## Terraform Implementation Snippet

```hcl
# First, create the Public IP (Optional, normally avoid in enterprise)
resource "azurerm_public_ip" "web_pip" {
  name                = "pip-web-01"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

# Second, create the Network Interface
resource "azurerm_network_interface" "web_nic" {
  name                = "nic-web-01"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.web_subnet.id
    private_ip_address_allocation = "Dynamic" # Or Static with private_ip_address
    public_ip_address_id          = azurerm_public_ip.web_pip.id # Optional
  }
}

# Third, associate the VM to the NIC
resource "azurerm_linux_virtual_machine" "web_vm" {
  name                = "vm-web-01"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name
  # ... other VM config ...

  network_interface_ids = [
    azurerm_network_interface.web_nic.id,
  ]
}
```

## IP Forwarding
By default, a NIC will drop packets if the destination IP address does not match the NIC's own IP address. If the VM is acting as a router, firewall, or NAT device (a Network Virtual Appliance), you must explicitly enable **IP Forwarding** on the NIC.

```hcl
resource "azurerm_network_interface" "nva_nic" {
  # ... standard config ...
  enable_ip_forwarding = true
}
```
