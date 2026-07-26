---
tags: [project, networking, enterprise, vwan]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Project: Global Enterprise Network

## Overview
Design a global networking topology for a multinational corporation with headquarters in New York and London.

## Architecture Diagram

```
  NYC Office                           London Office
  192.168.0.0/16                       172.16.0.0/16
       │                                      │
  ExpressRoute                         ExpressRoute
       │                                      │
       ▼                                      ▼
┌──────────────────┐               ┌──────────────────┐
│  Virtual Hub EUS │◄──── vWAN ───►│  Virtual Hub UKS │
│  10.100.0.0/23   │  (BGP sync)   │  10.200.0.0/23   │
│  ● AZ Firewall   │               │  ● AZ Firewall   │
│  ● ER Gateway    │               │  ● ER Gateway    │
└─────────┬────────┘               └────────┬─────────┘
          │ Spoke connections                │ Spoke connections
    ┌─────┴──────┐                    ┌──────┴─────┐
    ▼            ▼                    ▼            ▼
[Prod Spoke]  [Dev Spoke]        [Prod Spoke]  [Test Spoke]
10.10.0.0/16  10.20.0.0/16      10.30.0.0/16  10.40.0.0/16
```

> **Traffic Flow:** All inter-spoke and internet traffic routes through Azure Firewall Premium (Routing Intent). On-premises ↔ Azure uses ExpressRoute with BGP.

## Architecture Description
- **Topology:** Azure Virtual WAN (vWAN) with two Virtual Hubs (East US and UK South).
- **On-Premises Connectivity:** ExpressRoute circuits connecting the NYC office to the East US Hub, and the London office to the UK South Hub.
- **Security:** Secured Virtual Hub configuration. All internet-bound and cross-spoke traffic is forced through Azure Firewall.
- **Workloads:** Multiple Spoke VNets (Prod, Dev, Test) connected to their respective Hubs.

## Terraform Implementation Snippets

### Virtual WAN and Hubs
```hcl
resource "azurerm_virtual_wan" "vwan" {
  name                = "vwan-global-prod"
  resource_group_name = azurerm_resource_group.net_rg.name
  location            = azurerm_resource_group.net_rg.location
  type                = "Standard"
}

resource "azurerm_virtual_hub" "hub_eus" {
  name                = "vhub-eus"
  resource_group_name = azurerm_resource_group.net_rg.name
  location            = "eastus"
  virtual_wan_id      = azurerm_virtual_wan.vwan.id
  address_prefix      = "10.100.0.0/23"
}

resource "azurerm_virtual_hub" "hub_uks" {
  name                = "vhub-uks"
  resource_group_name = azurerm_resource_group.net_rg.name
  location            = "uksouth"
  virtual_wan_id      = azurerm_virtual_wan.vwan.id
  address_prefix      = "10.200.0.0/23"
}
```

### Secured Hub Firewall & Routing Intent
```hcl
resource "azurerm_firewall" "fw_eus" {
  name                = "fw-eus-hub"
  location            = azurerm_virtual_hub.hub_eus.location
  resource_group_name = azurerm_resource_group.net_rg.name
  sku_name            = "AZFW_Hub"
  sku_tier            = "Premium"
  firewall_policy_id  = azurerm_firewall_policy.global_policy.id

  virtual_hub {
    virtual_hub_id  = azurerm_virtual_hub.hub_eus.id
    public_ip_count = 1
  }
}

resource "azurerm_virtual_hub_routing_intent" "routing_eus" {
  name           = "routing-intent-eus"
  virtual_hub_id = azurerm_virtual_hub.hub_eus.id

  routing_policy {
    name         = "InternetTrafficPolicy"
    destinations = ["Internet"]
    next_hop     = azurerm_firewall.fw_eus.id
  }

  routing_policy {
    name         = "PrivateTrafficPolicy"
    destinations = ["PrivateTraffic"]
    next_hop     = azurerm_firewall.fw_eus.id
  }
}
```

## BGP and ExpressRoute
- **ExpressRoute Gateways** were deployed in each Virtual Hub.
- **BGP Configuration:** Azure automatically handles BGP route propagation within the vWAN. We configured our on-premises Edge Routers to advertise `192.168.0.0/16` (NYC) and `172.16.0.0/16` (London).
- Azure vWAN dynamically advertises the Spoke VNet prefixes back to on-premises.

## DNS Resolution across Hubs
Used **Azure Private DNS Resolver** to forward DNS queries from on-premises to Azure Private DNS Zones.
- An Inbound Endpoint was created in a dedicated DNS Spoke VNet attached to the Hub.
- On-premises DNS servers conditionally forward `*.database.windows.net` (Private Link) to the Inbound Endpoint IP.

## Lessons Learned

| # | Problem Faced | Root Cause | Solution Applied |
|---|--------------|------------|------------------|
| 1 | **Routing loops between hubs** | Default routes from both hubs conflicting via BGP | Enabled **Routing Intent** on each hub to explicitly define next-hop as Azure Firewall |
| 2 | **Private Link DNS not resolving from on-premises** | On-prem DNS servers couldn't resolve `*.database.windows.net` to private IPs | Deployed **Azure Private DNS Resolver** with Inbound Endpoint; configured conditional forwarders on on-prem DNS |
| 3 | **High Azure Firewall cost** | Deployed separate firewalls per spoke VNet initially | Migrated to **Secured Virtual Hub** — one Firewall per Hub covers all spokes automatically |
| 4 | **BGP route leakage between regions** | vWAN was advertising all prefixes to both hubs equally | Applied **Custom Route Tables** per hub to scope route advertisement to the correct region |
| 5 | **ExpressRoute failover too slow** | Single ER circuit — outage caused 4-hour downtime | Added a **second ER circuit** (different provider/peering location) with active-active routing |

## Monitoring & Optimization
- **Network Watcher:** Enabled Connection Monitor to track latency and packet loss between the NYC office and Azure East US VMs.
- **Traffic Analytics:** NSG Flow Logs enabled on Spoke subnets and sent to Log Analytics for traffic visualization.
- **Cost Optimization:** Azure Firewall Premium base cost is high. We consolidated multiple smaller firewalls into the Hubs to reduce overhead, taking advantage of vWAN's automated routing intent.

## Production Readiness Checklist
- [ ] Routing Intent enabled on all Virtual Hubs (forces all traffic through Firewall)
- [ ] ExpressRoute has redundant circuits (two providers or two peering locations)
- [ ] Azure Firewall Premium with IDPS in **Deny** mode
- [ ] Private DNS Resolver deployed with on-premises conditional forwarders
- [ ] BGP route tables audited — no unintended cross-region leakage
- [ ] Network Watcher Connection Monitor active between on-prem and Azure VMs
- [ ] Traffic Analytics enabled on all Spoke NSG Flow Logs
