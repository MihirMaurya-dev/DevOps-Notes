---
tags: [project, security, networking, firewall]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Project: Secure Hub and Spoke Architecture

## Overview
Implement a highly secure Hub and Spoke network topology with advanced threat protection, traffic inspection, and private PaaS access.

## Security Architecture Elements
- **Azure Firewall Premium:** Provides TLS inspection, IDPS (Intrusion Detection and Prevention), and URL filtering.
- **DDoS Protection Standard:** Attached to the Hub VNet to protect any exposed public IPs.
- **Azure Bastion:** Deployed in the Hub for secure, RDP/SSH access to internal VMs without public IPs.
- **Private Endpoints:** Used extensively in the Spokes to access PaaS services (SQL, Storage) privately.
- **Private DNS Zones:** Linked to the Hub VNet to resolve Private Endpoint IPs across all peered Spokes.

## Terraform Implementation Snippets

### Azure Firewall with Policy
```hcl
resource "azurerm_firewall_policy" "fw_policy" {
  name                = "premium-fw-policy"
  resource_group_name = azurerm_resource_group.hub_rg.name
  location            = azurerm_resource_group.hub_rg.location
  sku                 = "Premium"

  intrusion_detection {
    mode = "Deny"
  }
}

resource "azurerm_firewall_policy_rule_collection_group" "app_rules" {
  name               = "app-rule-group"
  firewall_policy_id = azurerm_firewall_policy.fw_policy.id
  priority           = 200

  application_rule_collection {
    name     = "allow-windows-update"
    priority = 100
    action   = "Allow"
    rule {
      name = "windows-update"
      protocols {
        type = "Https"
        port = 443
      }
      source_addresses  = ["10.0.0.0/8"]
      destination_fqdns = ["*.update.microsoft.com"]
    }
  }
}
```

### NSG for 3-Tier App (Spoke)
```hcl
resource "azurerm_network_security_group" "db_nsg" {
  name                = "db-subnet-nsg"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name

  security_rule {
    name                       = "AllowAppTier"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_port_range          = "*"
    destination_port_range     = "1433"
    source_address_prefix      = "10.1.1.0/24" # App Subnet
    destination_address_prefix = "10.1.2.0/24" # DB Subnet
  }

  security_rule {
    name                       = "DenyAllInbound"
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
```

### Private Endpoint for Key Vault
```hcl
resource "azurerm_private_endpoint" "kv_pe" {
  name                = "kv-private-endpoint"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name
  subnet_id           = azurerm_subnet.spoke_pe_subnet.id

  private_service_connection {
    name                           = "kv-privateserviceconnection"
    private_connection_resource_id = azurerm_key_vault.kv.id
    is_manual_connection           = false
    subresource_names              = ["vault"]
  }

  private_dns_zone_group {
    name                 = "kv-dns-zone-group"
    private_dns_zone_ids = [azurerm_private_dns_zone.privatelink_vaultcore.id]
  }
}
```

## Microsoft Defender for Cloud Integration
- Enabled Defender CSPM for posture management and vulnerability scanning.
- Enabled Defender for Servers (Plan 2) to get Just-In-Time VM access and Adaptive Application Controls.

## Security Audit Checklist
- [x] All VMs lack Public IPs.
- [x] All VNet-to-Internet traffic routes via Azure Firewall (UDR `0.0.0.0/0`).
- [x] SQL Databases have "Allow access to Azure services" set to FALSE (rely on Private Link).
- [x] Storage Accounts have public network access disabled.
- [x] NSGs applied to every subnet with explicit Deny rules.
