---
tags: [azure, networking, vpn, expressroute]
source: devopsinsiders/batch-18
created: 2026-06-14
updated: 2026-06-14
---

# Virtual Network Gateway (VPN / ExpressRoute)

A Virtual Network Gateway is a specialized virtual machine deployed in a specific subnet of your Virtual Network. It is used to send encrypted traffic between an Azure VNet and an on-premises location over the public internet (VPN), or to send traffic over a dedicated, private connection (ExpressRoute).

## Gateway Subnet
- A Virtual Network Gateway **MUST** be deployed into a subnet named exactly `GatewaySubnet`.
- This subnet must not contain any other resources.
- A `/27` or larger subnet mask is strongly recommended by Microsoft.
- Do NOT apply a Network Security Group (NSG) to the `GatewaySubnet`.

## 1. VPN Gateway (Site-to-Site, Point-to-Site, VNet-to-VNet)
A VPN Gateway is a specific type of virtual network gateway that is used to send encrypted traffic between an Azure virtual network and an on-premises location over the public internet.

### Connection Types
- **Site-to-Site (S2S):** Connects an entire on-premises network (via an edge router/firewall like Cisco or Palo Alto) to the Azure VNet over an IPsec/IKE VPN tunnel.
- **Point-to-Site (P2S):** Connects individual client laptops to the Azure VNet using an Azure VPN Client.
  - **Protocols Supported:** OpenVPN, SSTP (Secure Socket Tunneling Protocol), and IKEv2.
  - **Authentication Methods:** Entra ID (formerly Azure AD), RADIUS server, or Azure native Certificate authentication.
- **VNet-to-VNet:** Connecting two Azure VNets using VPN gateways (though VNet Peering is often preferred unless encryption over the Azure backbone is strictly required).

### Routing Types
- **Route-Based (Recommended):** Uses dynamic routing (like BGP) or static routes to determine which traffic goes through the tunnel. Supports IKEv2 and allows multiple S2S connections. All modern SKUs require route-based.
- **Policy-Based (Legacy):** Traffic is encrypted based on explicit IP address prefixes defined in the IPsec policies. Only supports IKEv1 and basic SKUs.

### High Availability (HA) Architecture
By default, VPN Gateways are deployed with two instances in an Active-Standby configuration for high availability within the same region.
- **Active-Standby (Default):** One instance is active, the other is on standby. If the active instance fails, the standby takes over (brief drop in connection).
- **Active-Active:** Both instances are active and establish independent IPsec tunnels to the on-premises router. Requires BGP. Provides higher throughput and better fault tolerance.
- **Zone-Redundant (AZ):** SKUs with the "AZ" suffix (e.g., VpnGw1AZ) deploy instances across different Availability Zones to protect against zone-level failures.

### BGP (Border Gateway Protocol)
- BGP enables dynamic routing between your on-premises network and Azure.
- Automatically exchanges routing information, so you don't have to manually update static routes when new subnets are added.
- Essential for Active-Active gateway configurations and complex multi-path networks.

### SKUs and Generations
- **Basic:** Legacy, not recommended for production. Supports max 10 S2S tunnels, 100 Mbps throughput.
- **Generation 1 (VpnGw1, VpnGw2, VpnGw3):** Standard SKUs. VpnGw1 provides up to 650 Mbps.
- **Generation 2 (VpnGw2 - VpnGw5):** Higher performance, lower latency. VpnGw5 supports up to 10 Gbps and 100 S2S tunnels.

## 2. ExpressRoute Gateway
- ExpressRoute bypasses the public internet completely. Traffic goes through a connectivity provider (like Equinix or AT&T) directly into the Microsoft edge.
- **Latency & Reliability:** Offers highly reliable speeds (up to 100 Gbps) and very low latency compared to a standard VPN.
- **Cost:** Significantly more expensive than a VPN Gateway, with a monthly port fee plus data outbound costs (or an unlimited data plan).

## Coexistence
You can deploy both a VPN Gateway and an ExpressRoute Gateway in the same `GatewaySubnet`. This is often done to use the VPN as a backup path if the ExpressRoute circuit goes down.

## Terraform Implementation Snippet (VPN Gateway)

```hcl
# Must be named exactly GatewaySubnet
resource "azurerm_subnet" "gateway_subnet" {
  name                 = "GatewaySubnet"
  resource_group_name  = azurerm_resource_group.hub_rg.name
  virtual_network_name = azurerm_virtual_network.hub.name
  address_prefixes     = ["10.0.254.0/27"]
}

# Public IP required for the VPN Gateway
resource "azurerm_public_ip" "vpn_pip" {
  name                = "pip-vpngw-prod"
  location            = azurerm_resource_group.hub_rg.location
  resource_group_name = azurerm_resource_group.hub_rg.name
  allocation_method   = "Dynamic" # Basic/Dynamic often used for legacy VPNs, Standard/Static for newer Gen2 SKUs
}

# The Virtual Network Gateway
resource "azurerm_virtual_network_gateway" "vpn_gw" {
  name                = "vgw-hub-vpn"
  location            = azurerm_resource_group.hub_rg.location
  resource_group_name = azurerm_resource_group.hub_rg.name

  type     = "Vpn"
  vpn_type = "RouteBased"
  sku      = "VpnGw1" # Generation 1 SKU

  ip_configuration {
    name                          = "vnetGatewayConfig"
    public_ip_address_id          = azurerm_public_ip.vpn_pip.id
    private_ip_address_allocation = "Dynamic"
    subnet_id                     = azurerm_subnet.gateway_subnet.id
  }
}

# Local Network Gateway (Represents the On-Premises Router)
resource "azurerm_local_network_gateway" "onprem" {
  name                = "lng-onprem-datacenter"
  location            = azurerm_resource_group.hub_rg.location
  resource_group_name = azurerm_resource_group.hub_rg.name
  gateway_address     = "203.0.113.1" # Public IP of on-prem router
  address_space       = ["192.168.0.0/16"] # On-prem IP ranges
}

# The actual IPsec connection
resource "azurerm_virtual_network_gateway_connection" "s2s" {
  name                       = "con-hub-to-onprem"
  location                   = azurerm_resource_group.hub_rg.location
  resource_group_name        = azurerm_resource_group.hub_rg.name
  type                       = "IPsec"
  virtual_network_gateway_id = azurerm_virtual_network_gateway.vpn_gw.id
  local_network_gateway_id   = azurerm_local_network_gateway.onprem.id
  shared_key                 = "SuperSecretIPsecKey123!" # Pre-shared key
}
```
