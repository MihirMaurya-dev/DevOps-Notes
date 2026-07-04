---
tags: [interview, prep, networking, questions]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Networking Interview Questions

A collection of common interview questions regarding Azure and general IT networking.

## Q1: What is the OSI Model, and at which layers do NSGs and Azure Application Gateways operate?
**A:** The OSI model is a conceptual framework used to describe the functions of a networking system. 
- **Network Security Groups (NSGs)** operate primarily at **Layer 4 (Transport Layer)**. They filter traffic based on source/destination IP, port, and protocol (TCP/UDP).
- **Azure Application Gateway** operates at **Layer 7 (Application Layer)**. It can inspect HTTP headers, perform URL-based routing, and act as a Web Application Firewall (WAF).

## Q2: You are designing a VNet with the address space `10.0.0.0/24`. How many usable IPs does this provide?
**A:** A `/24` CIDR block provides 256 total IP addresses. However, Azure reserves 5 IP addresses in every subnet (Network address, Default Gateway, Azure DNS, reserved for future use, and Broadcast address). Therefore, there are **251** usable IP addresses for resources.

## Q3: What is the difference between an Azure Load Balancer and an Azure Application Gateway?
**A:** 
- **Azure Load Balancer** is a Layer 4 (TCP/UDP) load balancer. It is ultra-fast, handles any type of traffic, and does not look at the contents of the packets. It simply forwards traffic based on ports.
- **Azure Application Gateway** is a Layer 7 (HTTP/HTTPS) load balancer. It understands web traffic, can decrypt SSL/TLS, route traffic based on URL paths (e.g., send `/images` to Server A and `/video` to Server B), and provides WAF capabilities.

## Q4: Why would you use Azure Private Link (Private Endpoints)?
**A:** Azure Private Link allows you to access Azure PaaS services (like Azure Storage or Azure SQL Database) securely from your VNet over a private IP address, rather than connecting over the public internet. This ensures that traffic remains entirely on the Microsoft backbone network, significantly improving security and meeting compliance requirements.

## Q5: In a Hub and Spoke network, how do you force all outbound internet traffic from a Spoke VM to go through the Hub Firewall?
**A:** By creating a **Route Table** and adding a **User Defined Route (UDR)**. The route would specify a destination prefix of `0.0.0.0/0` (which represents all unknown/internet traffic) and set the Next Hop Type to `VirtualAppliance`. The Next Hop IP address would be the private IP of the Azure Firewall in the Hub VNet. Finally, I would associate this Route Table with the subnet where the VM resides.

## Q6: What is BGP and how is it used in Azure?
**A:** BGP (Border Gateway Protocol) is the routing protocol of the internet. It is used in Azure in two main contexts:
- **ExpressRoute:** BGP is used to exchange routes between your on-premises network and your Azure VNet through the ExpressRoute circuit. Azure advertises your VNet address spaces to your on-premises router, and your router advertises your on-premises prefixes to Azure.
- **VPN Gateway:** When configured in Active-Active mode or with a BGP-enabled VPN device on-premises, Azure VPN Gateway can use BGP to dynamically learn routes rather than requiring static routes to be configured manually.

## Q7: What is the difference between a VPN Gateway and ExpressRoute?
**A:**
| Feature | VPN Gateway | ExpressRoute |
|---------|-------------|--------------|
| **Connection type** | Public internet (encrypted IPSec tunnel) | Private dedicated circuit through a connectivity provider |
| **Bandwidth** | Up to 10 Gbps | Up to 100 Gbps |
| **Latency** | Higher (internet-dependent) | Consistent, low latency (private line) |
| **SLA** | 99.95% | 99.95% |
| **Cost** | Lower | Much higher |
| **Use case** | Branch offices, remote workers, dev environments | Enterprise production workloads needing guaranteed performance |

## Q8: Explain Azure VNet Peering. What are its limitations?
**A:** VNet Peering creates a low-latency, high-bandwidth network connection between two Azure VNets. Traffic between peered VNets travels over the Microsoft backbone (not the public internet) and is not encrypted by default (it relies on the physical security of the backbone). Key limitations:
1. **Non-transitive:** If VNet A is peered to Hub, and VNet B is peered to Hub, VNet A cannot communicate with VNet B directly — all traffic must flow through the Hub (and a Network Virtual Appliance/Firewall).
2. **No overlapping address spaces:** Two VNets being peered cannot have overlapping CIDR blocks.
3. **Regional vs Global:** Regional peering is free for ingress/egress. Global VNet Peering (across regions) has a data transfer cost.

## Q9: What is DNS and how is name resolution handled in an Azure VNet?
**A:** DNS (Domain Name System) translates human-readable domain names (e.g., `myvm.internal.com`) into IP addresses. In an Azure VNet, name resolution works as follows:
- **Azure-provided DNS (default):** Azure automatically provides a DNS server (`168.63.129.16`) for all VMs in a VNet. It resolves Azure internal hostnames (e.g., `vm1.internal.cloudapp.azure.com`) and forwards public DNS queries to Azure's public DNS.
- **Custom DNS:** For hybrid environments requiring on-premises DNS (e.g., resolving `db.corp.contoso.com`), you configure the VNet DNS settings to point to your on-premises DNS servers or a DNS forwarder VM in Azure.
- **Private DNS Zones:** For Private Endpoints, Azure Private DNS Zones automatically register the private IP of the endpoint, so `myblobaccount.blob.core.windows.net` resolves to a private IP (`10.x.x.x`) instead of the public IP.

## Q10: What is the difference between a Network Security Group (NSG) and Azure Firewall?
**A:**
| Feature | NSG | Azure Firewall |
|---------|-----|----------------|
| **Scope** | Subnet or NIC level | VNet-level (Hub) |
| **Layer** | Layer 4 (IP/Port/Protocol) | Layer 4 + Layer 7 (FQDN filtering, TLS inspection) |
| **FQDN filtering** | ❌ No | ✅ Yes (e.g., allow `*.azure.com`) |
| **Threat intelligence** | ❌ No | ✅ Yes (Microsoft feed) |
| **Cost** | Free | $$$ (hourly + data processing) |
| **Statefulness** | Stateful | Stateful |
| **Use case** | Micro-segmentation within a VNet | Perimeter security, centralized egress control |

> [!tip]
> Use **both** in a defense-in-depth strategy. Azure Firewall controls macro-level traffic between VNets and the internet; NSGs provide micro-segmentation between subnets within a VNet.

## Q11: What is Azure DDoS Protection and when do you need it?
**A:** Azure DDoS (Distributed Denial of Service) Protection defends against volumetric attacks that try to overwhelm your application with traffic. There are two tiers:
- **DDoS Network Protection (Basic/Free):** Automatically enabled for all Azure public IPs. Provides basic rate-limiting and traffic scrubbing at the platform level.
- **DDoS Network Protection (Standard):** Paid tier. Provides adaptive tuning (learns your application's normal traffic patterns), detailed attack metrics and alerts, cost protection (credit for resources scaled out during an attack), and dedicated support from the Microsoft DDoS Rapid Response team.

You need the Standard tier for any production application with public-facing endpoints, especially financial services, healthcare, or gaming applications that are high-value DDoS targets.

## Q12: Explain the concept of Network Address Translation (NAT) in Azure.
**A:** NAT (Network Address Translation) is used to allow resources with private IP addresses to communicate with the public internet without having public IPs assigned directly to them.
- **Azure NAT Gateway:** The recommended outbound-only NAT solution. You associate it with a subnet, and it translates outbound traffic from all VMs in that subnet to one or more static Public IP addresses. This ensures a predictable, stable outbound public IP, which is important when allow-listing your IP with external services.
- **Load Balancer SNAT:** If an Azure Load Balancer is in front of a backend pool, it can perform SNAT (Source NAT), but this has port exhaustion risks under high load. NAT Gateway is preferred for dedicated outbound NAT.
