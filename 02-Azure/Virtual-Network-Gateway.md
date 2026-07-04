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

## 1. VPN Gateway (Site-to-Site / Point-to-Site)
- **Site-to-Site (S2S):** Connects an entire on-premises network (via an edge router/firewall like Cisco or Palo Alto) to the Azure VNet over an IPsec/IKE VPN tunnel.
- **Point-to-Site (P2S):** Connects individual client laptops to the Azure VNet using an Azure VPN Client (SSTP, OpenVPN, IKEv2). Often uses Entra ID for user authentication.

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
