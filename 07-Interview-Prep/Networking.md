---
tags: [interview, prep, networking, questions, azure]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-07-26
---

# Networking Interview Questions

A comprehensive collection of interview questions regarding Azure and general IT networking.

---

## Basics

### Q1: What is the OSI Model, and at which layers do NSGs and Azure Application Gateways operate?
**A:** The OSI model is a conceptual framework describing network communication across 7 layers. Network Security Groups (NSGs) operate at **Layer 4 (Transport)**, filtering traffic based on source/destination IPs, ports, and protocols (TCP/UDP). Azure Application Gateway operates at **Layer 7 (Application)**, allowing it to inspect HTTP headers, route based on URLs, and act as a Web Application Firewall (WAF).

### Q2: What is an IP address, and what is the difference between IPv4 and IPv6?
**A:** An IP address is a unique numerical identifier assigned to devices on a network for communication. IPv4 uses a 32-bit address scheme allowing for about 4.3 billion addresses, written in dotted-decimal format (e.g., `192.168.1.1`). IPv6 was created to solve IPv4 exhaustion, using a 128-bit address scheme written in hexadecimal format (e.g., `2001:0db8::ff00:42:8329`), providing a virtually limitless pool of addresses.

### Q3: What are public vs private IP addresses, and how do they apply in Azure?
**A:** Public IP addresses are globally routable on the internet. In Azure, they are used for resources that must accept external traffic, like Load Balancers or App Gateways. Private IP addresses are non-routable over the internet and are used for communication within a local network or Azure VNet. Azure VMs default to using private IPs for secure, internal communication.

### Q4: What is a Subnet, and why do we use subnetting?
**A:** A subnet is a logical subdivision of a larger IP network (like an Azure VNet). Subnetting improves network performance by reducing broadcast domains and enhances security by allowing micro-segmentation. In Azure, you use subnets to logically group resources (e.g., a frontend subnet and a backend database subnet) and apply distinct Network Security Groups (NSGs) or route tables to each.

### Q5: You are designing a VNet with the address space `10.0.0.0/24`. How many usable IPs does this provide?
**A:** A `/24` CIDR block provides 256 total IP addresses. However, Azure reserves 5 IP addresses in every subnet: the network address, the default gateway, Azure DNS, one reserved for future use, and the broadcast address. Therefore, there are exactly **251** usable IP addresses for your resources in that subnet.

### Q6: What is DNS and how is name resolution handled in an Azure VNet?
**A:** DNS translates human-readable domain names into IP addresses. In Azure, internal name resolution is handled automatically by Azure-provided DNS (`168.63.129.16`), which resolves Azure internal hostnames. For hybrid environments or custom domains, you can configure custom DNS settings on the VNet to point to your own DNS servers, or use Azure Private DNS zones for seamless private endpoint resolution.

### Q7: What is the difference between TCP and UDP?
**A:** TCP (Transmission Control Protocol) is connection-oriented, ensuring reliable, ordered, and error-checked delivery of packets (used for web browsing, SSH, database connections). UDP (User Datagram Protocol) is connectionless and prioritizes speed over reliability, meaning packets might drop or arrive out of order (used for video streaming, VoIP, gaming).

### Q8: What is a VPN, and how does a Site-to-Site VPN differ from a Point-to-Site VPN?
**A:** A VPN (Virtual Private Network) creates a secure, encrypted tunnel over the public internet. A Site-to-Site VPN connects two distinct physical networks together (e.g., an on-premises data center router connecting to an Azure VPN Gateway). A Point-to-Site VPN connects an individual client computer securely to a network (e.g., a developer working from home connecting securely to an Azure VNet).

---

## Intermediate

### Q9: What is the difference between an Azure Load Balancer and an Azure Application Gateway?
**A:** Azure Load Balancer is a Layer 4 (TCP/UDP) load balancer that routes traffic purely based on IP and port, making it extremely fast but unaware of application content. Azure Application Gateway is a Layer 7 (HTTP/HTTPS) load balancer. It understands web traffic, can terminate SSL/TLS, route based on URL paths (e.g., `/images` to one backend, `/api` to another), and provides Web Application Firewall (WAF) capabilities.

### Q10: What is the difference between a Network Security Group (NSG) and Azure Firewall?
**A:** NSGs are free, basic Layer 4 stateful firewalls applied at the subnet or NIC level for micro-segmentation within a VNet. Azure Firewall is a managed, highly available, centralized network security appliance deployed in a Hub VNet. Azure Firewall provides advanced capabilities like Layer 7 FQDN filtering (e.g., block `*.youtube.com`), threat intelligence-based filtering, and centralized egress control, but it comes at a significant hourly cost.

### Q11: Explain Azure VNet Peering. What are its limitations?
**A:** VNet Peering connects two Azure VNets directly over the Microsoft backbone network, providing low-latency, high-bandwidth communication without going over the public internet. Key limitations include: it is non-transitive (if A peers to B, and B peers to C, A cannot reach C directly), the peered VNets cannot have overlapping IP address spaces, and global peering (across regions) incurs data transfer costs.

### Q12: What is the difference between a VPN Gateway and ExpressRoute?
**A:** VPN Gateway routes traffic over the public internet using an encrypted IPSec tunnel, offering up to 10 Gbps with variable latency and lower cost. ExpressRoute is a private, dedicated physical connection provided by an ISP directly into the Microsoft edge. It completely bypasses the public internet, offering speeds up to 100 Gbps, consistent ultra-low latency, and is preferred for enterprise-grade, mission-critical hybrid networking.

### Q13: Why would you use Azure Private Link (Private Endpoints)?
**A:** Azure Private Link allows you to access Azure PaaS services (like Storage Accounts, SQL DBs, or Key Vaults) using a private IP address from your VNet. This ensures traffic remains entirely on the Microsoft backbone and never traverses the public internet. It significantly enhances security, simplifies network architecture by removing the need for public IP firewall rules, and helps satisfy strict compliance requirements.

### Q14: Explain the concept of Network Address Translation (NAT) in Azure.
**A:** NAT enables resources with private IP addresses to communicate out to the public internet by translating their private IPs to a public IP. Azure NAT Gateway is the recommended solution for outbound internet connectivity. It provides a static, predictable public IP for an entire subnet's outbound traffic, preventing port exhaustion issues that can occur when relying on default outbound access or load balancer SNAT.

### Q15: What is Azure Front Door and how does it differ from Traffic Manager?
**A:** Azure Front Door is a global, Layer 7 load balancer and Content Delivery Network (CDN) that optimizes and secures web applications using Microsoft's global edge network. It performs SSL termination and path-based routing globally. Azure Traffic Manager is a DNS-based load balancer. It does not handle the actual data plane traffic; it merely returns the IP address of the closest or healthiest endpoint, leaving the client to connect directly.

### Q16: How do User Defined Routes (UDR) work in an Azure VNet?
**A:** Azure provides default system routes for VNets, but User Defined Routes (UDRs) allow you to override them. You attach a Route Table to a subnet to force specific traffic paths. A common use case is adding a UDR for `0.0.0.0/0` (all internet traffic) with the Next Hop set to `Virtual Appliance` (like an Azure Firewall). This forces all outbound traffic from the subnet to go through the firewall for inspection.

### Q17: What are Service Endpoints and how do they differ from Private Endpoints?
**A:** Service Endpoints provide secure, direct routing from a VNet to an Azure PaaS service over the Azure backbone, but the PaaS service still uses its public endpoint. Private Endpoints actually bring the PaaS service into your VNet by assigning it a private IP address from your subnet. Private Endpoints are generally preferred today as they allow on-premises connectivity via VPN/ExpressRoute and remove public routing entirely.

---

## Advanced

### Q18: What is BGP and how is it used in Azure?
**A:** BGP (Border Gateway Protocol) is the dynamic routing protocol of the internet. In Azure, BGP is heavily used in ExpressRoute and advanced VPN Gateway setups. Instead of manually configuring static routes on both sides, BGP allows your on-premises routers and Azure gateways to dynamically advertise and learn network prefixes. This ensures automatic failover and seamless routing updates when network topologies change.

### Q19: What is Azure DDoS Protection and when do you need it?
**A:** Azure provides basic DDoS protection automatically on all public IPs to protect the platform. The standard/premium tier provides adaptive, machine-learning-based traffic profiling, detailed metrics, mitigation reports, and a cost-protection SLA (crediting you for auto-scaled resources during an attack). You need the paid tier for mission-critical, public-facing applications (like financial services or gaming) that are high-value targets for volumetric attacks.

### Q20: How do you design a highly available Hub and Spoke network architecture in Azure?
**A:** I would deploy a Hub VNet containing shared services like Azure Firewall, VPN Gateway/ExpressRoute, and Bastion. Multiple Spoke VNets (housing different application workloads) would peer exclusively with the Hub. For high availability, I would deploy Azure Firewall across multiple Availability Zones. I would use UDRs in the spokes to force traffic through the Hub firewall, ensuring centralized security, visibility, and robust fault tolerance.

### Q21: Explain how Azure Virtual WAN simplifies large-scale networking.
**A:** Managing dozens of VNets, branch office VPNs, and ExpressRoute circuits with traditional Hub and Spoke peering becomes administratively complex. Azure Virtual WAN provides a unified, managed hub networking service. It automates routing and connectivity between branches, users (Point-to-Site), ExpressRoute, and VNets globally, acting as an intelligent network core that vastly simplifies global transit architectures.

### Q22: How do you troubleshoot asymmetric routing in a multi-region Azure setup?
**A:** Asymmetric routing occurs when a packet takes one path to a destination but the return packet takes a different path, often causing stateful firewalls to drop the connection. I would trace the traffic flow using Network Watcher, verify BGP advertisements, and check UDRs. The fix usually involves implementing Source NAT (SNAT) on the firewall or load balancer to ensure the return traffic correctly routes back to the appliance that initiated the session.

### Q23: How does TLS/SSL offloading work on an Application Gateway?
**A:** TLS offloading involves terminating the encrypted SSL/TLS connection at the Application Gateway instead of the backend servers. The client encrypts traffic to the App Gateway, which decrypts it, inspects it (e.g., using WAF), and then forwards it to the backend VM unencrypted (or re-encrypts it for end-to-end TLS). This offloads the CPU-intensive decryption process from the backend application servers and allows centralized certificate management.

### Q24: What is micro-segmentation, and how can it be achieved in Azure?
**A:** Micro-segmentation is a zero-trust security approach that tightly restricts network access between workloads, even within the same subnet. In Azure, this is achieved by applying highly specific Network Security Groups (NSGs) and Application Security Groups (ASGs). By grouping VMs logically with ASGs (e.g., "WebTier" and "DBTier") rather than by IP addresses, you can create granular NSG rules that easily scale as VMs are added or removed.

---

## Scenario-Based

### Q25: Scenario: In a Hub and Spoke network, how do you force all outbound internet traffic from a Spoke VM to go through the Hub Firewall?
**A:** I would create an Azure Route Table and add a User Defined Route (UDR). The route would specify a destination prefix of `0.0.0.0/0` (representing all external internet traffic). The Next Hop type would be set to `Virtual Appliance`, and the Next Hop IP address would be the private IP of the Azure Firewall located in the Hub VNet. Finally, I would associate this Route Table with the subnet in the Spoke VNet where the VM resides.

### Q26: Scenario: A VM in Subnet A cannot communicate with a VM in Subnet B. How do you troubleshoot?
**A:** I would start by using the **IP Flow Verify** tool in Azure Network Watcher to test communication from Subnet A to Subnet B on the specific port. This tool will immediately tell me if a specific NSG rule is blocking traffic. Next, I would verify that both VMs are powered on, check the OS-level firewall (like Windows Defender Firewall or iptables), and ensure the subnets have correct UDRs if custom routing is applied.

### Q27: Scenario: Your web application is experiencing a volumetric DDoS attack. How do you respond?
**A:** Assuming we have Azure DDoS Network Protection enabled, mitigation triggers automatically when traffic exceeds normal baseline thresholds. I would immediately review Azure Monitor metrics and DDoS mitigation reports. I would ensure our Application Gateway WAF is set to Prevention mode to block malicious application-layer requests. Concurrently, I would notify stakeholders and verify that our auto-scaling groups are responding correctly to the load spike.

### Q28: Scenario: You need to connect 50 branch offices to Azure securely and with minimal administrative overhead. What is your approach?
**A:** Configuring 50 individual Site-to-Site VPN connections manually is unmanageable. I would use **Azure Virtual WAN** with integrated VPN capabilities. Virtual WAN allows automated, large-scale branch connectivity and optimizes routing. I would also recommend using SD-WAN devices at the branch offices that integrate natively with Azure Virtual WAN, enabling zero-touch provisioning of the VPN tunnels back to the Azure Hub.

### Q29: Scenario: Your on-premises database must securely sync with an Azure SQL Database. The security team strictly forbids traffic over the public internet. How do you architect this?
**A:** I would utilize **Azure Private Link** and **ExpressRoute**. First, I create a Private Endpoint for the Azure SQL Database, assigning it a private IP within the VNet. Then, traffic from the on-premises database will route over the private ExpressRoute circuit, hitting the VNet, and connecting directly to the SQL private IP. This guarantees that all synchronization traffic stays entirely on private Microsoft and ISP backbones.

### Q30: Scenario: Developers report intermittent connection timeouts to an external API from an Azure VM behind a standard load balancer. What is the likely cause and fix?
**A:** This is likely caused by **SNAT port exhaustion**. When multiple VMs behind a load balancer make outbound connections to the internet, they share the load balancer's public IP and finite SNAT ports. Under high load, these ports run out, causing connection drops. The fix is to deploy an **Azure NAT Gateway** and attach it to the subnet, which handles outbound connections far more efficiently and provides up to 64,000 concurrent SNAT ports per IP.
