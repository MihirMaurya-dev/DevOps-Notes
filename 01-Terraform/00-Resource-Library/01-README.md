# 📚 Terraform Resource Library

This directory contains **ready-to-use Terraform resource templates** for common Azure services. Each file is a focused, production-grade snippet that can be copied directly into your Terraform projects.

## Files in This Directory

| File | Azure Service | Key Features |
|------|--------------|-------------|
| [VNet.md](10-VNet.md) | Azure Virtual Network | Address space, DNS, peering |
| [Subnet.md](08-Subnet.md) | Subnets | Delegation, service endpoints |
| [NSG.md](05-NSG.md) | Network Security Groups | Rules, associations |
| [VM.md](09-VM.md) | Virtual Machines | Linux VM, NIC, SSH |
| [AKS.md](02-AKS.md) | Azure Kubernetes Service | Node pools, RBAC, CNI |
| [Key-Vault.md](03-Key-Vault.md) | Azure Key Vault | Secrets, access policies, Private Endpoint |
| [Log-Analytics.md](04-Log-Analytics.md) | Log Analytics Workspace | Retention, diagnostic settings |
| [Storage-Account.md](07-Storage-Account.md) | Storage Account | Blob, lifecycle, encryption |
| [Resource-Group.md](06-Resource-Group.md) | Resource Groups | Tags, locks |
| [Public-IP.md](Public-IP.md) | Azure Public IP | Static vs Dynamic allocations |
| [Network-Interface.md](Network-Interface.md) | Network Interface (NIC) | IP Configurations, connecting VMs |
| [NAT-Gateway.md](NAT-Gateway.md) | Azure NAT Gateway | Secure outbound internet routing |

## How to Use

1. Find the resource you need in the table above.
2. Copy the HCL snippet from the relevant file.
3. Adjust variables (`name`, `location`, `resource_group_name`) to match your project.
4. Reference outputs from these resources in your root module.

> **Tip:** All snippets follow the naming conventions defined in [01-Terraform/15-Best-Practices.md](../15-Best-Practices.md).
