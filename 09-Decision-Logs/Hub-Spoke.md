---
tags: [decision-log, architecture, networking]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Decision Log: Hub and Spoke vs Virtual WAN

## Context
The organization is moving from a single VNet design to a multi-VNet design to support distinct workload subscriptions. We need to decide on the core networking topology.

## Options Considered
1. **Traditional Hub and Spoke:** Manually deploying Hub VNets, configuring VNet peering, and managing User Defined Routes (UDRs).
2. **Azure Virtual WAN (vWAN):** A Microsoft-managed service that handles hub creation, peering, and transitive routing automatically.

## Decision
**Selected Option:** Traditional Hub and Spoke.

## Rationale
- **Scale:** The organization currently only operates in a single Azure region (East US) and expects to have fewer than 10 Spoke VNets over the next two years.
- **Cost:** Azure vWAN has a higher base cost and is designed for massive scale (hundreds of spokes across global regions). The cost is not justified for our current scale.
- **Control:** The team requires fine-grained control over routing tables and NVA placement, which is slightly more opaque in the managed vWAN environment.

## Traffic Flow Architecture
- **Spoke to Internet:** A UDR forces all `0.0.0.0/0` traffic to the Hub Azure Firewall private IP. The Firewall SNATs the traffic to its Public IP.
- **Spoke to Spoke:** Because VNet peering is non-transitive, a UDR in Spoke A forces traffic destined for Spoke B's CIDR block to the Hub Firewall. The Firewall inspects the traffic and routes it to Spoke B.
- **On-Premises to Spoke:** ExpressRoute Gateway is in the Hub. Spokes use the `Use Remote Gateways` peering setting to traverse the Hub.

## Terraform Implementation

### VNet Peering
```hcl
# Hub to Spoke Peering
resource "azurerm_virtual_network_peering" "hub_to_spoke" {
  name                      = "peer-hub-to-spoke1"
  resource_group_name       = azurerm_resource_group.hub_rg.name
  virtual_network_name      = azurerm_virtual_network.hub.name
  remote_virtual_network_id = azurerm_virtual_network.spoke.id
  allow_virtual_network_access = true
  allow_forwarded_traffic      = true
  allow_gateway_transit        = true # Crucial for VPN/ER
}

# Spoke to Hub Peering
resource "azurerm_virtual_network_peering" "spoke_to_hub" {
  name                      = "peer-spoke1-to-hub"
  resource_group_name       = azurerm_resource_group.spoke_rg.name
  virtual_network_name      = azurerm_virtual_network.spoke.name
  remote_virtual_network_id = azurerm_virtual_network.hub.id
  allow_virtual_network_access = true
  use_remote_gateways          = true # Crucial for using Hub's VPN/ER
}
```

### User Defined Routes (UDR)
```hcl
resource "azurerm_route_table" "spoke_rt" {
  name                = "rt-spoke-default"
  location            = azurerm_resource_group.spoke_rg.location
  resource_group_name = azurerm_resource_group.spoke_rg.name

  route {
    name                   = "route-to-firewall"
    address_prefix         = "0.0.0.0/0"
    next_hop_type          = "VirtualAppliance"
    next_hop_in_ip_address = "10.0.1.4" # Private IP of Azure Firewall in Hub
  }
}

resource "azurerm_subnet_route_table_association" "spoke_subnet_assoc" {
  subnet_id      = azurerm_subnet.spoke_app_subnet.id
  route_table_id = azurerm_route_table.spoke_rt.id
}
```

## Future Considerations
If the organization expands to a multi-region deployment (e.g., opening a European branch) and requires full mesh connectivity between global spokes, the operational overhead of managing UDRs and global peerings will become untenable. At that point, we will re-evaluate migrating the Hub VNets to Azure Virtual WAN (vWAN).
