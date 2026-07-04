---
category: Azure-Networking
tags: [azure, load-balancer, lb, layer4, architecture]
type: enterprise-architect-guide
status: active
---

# ⚖️ Azure Load Balancer - Enterprise Architect Guide

## 1. Introduction
Azure Load Balancer is a high-performance, ultra-low-latency Layer 4 (TCP/UDP) load balancing service. It distributes incoming network traffic across a group of backend resources (like VMs or VM Scale Sets). It can be configured as a **Public** Load Balancer (internet-facing) or an **Internal** Load Balancer (private VNet traffic).

## 2. Why This Service Exists
Single servers are single points of failure. To achieve high availability and handle large volumes of traffic, you need multiple servers acting as one. Historically, this required expensive physical appliances (like F5 or A10). Azure Load Balancer exists as a cloud-native, Software-Defined Networking (SDN) abstraction to provide this capability out-of-the-box without managing underlying appliances.

## 3. Architecture
- **Scope:** Regional.
- **Layer:** Layer 4 (Transport - TCP/UDP). It does not understand HTTP/HTTPS or URLs.
- **Under the Hood:** It is not a traditional proxy. It uses a hash-based distribution algorithm (Source IP, Source Port, Destination IP, Destination Port, Protocol) and operates using **Direct Server Return (DSR)** for floating IP scenarios, meaning backend servers can respond directly to the client without the return traffic bottlenecking through the load balancer.

## 4. Core Components
- **Frontend IP Configuration:** The IP address (Public or Private) that clients connect to.
- **Backend Pool:** The group of VMs or VMSS instances that serve the traffic.
- **Health Probes:** Automated checks (pinging a specific port) to determine if a backend instance is healthy. Unhealthy instances stop receiving traffic.
- **Load Balancing Rules:** The mapping rule linking a Frontend IP/Port to a Backend Pool/Port.
- **Inbound NAT Rules:** Used to port-forward traffic to a specific, single VM (e.g., mapping public port 50001 to port 3389 on VM-1 for RDP access).

## 5. Step-by-Step Request Flow
**Scenario:** A client connects to a SQL Server cluster behind an Internal Load Balancer.
1. Client initiates a TCP connection to the LB's Frontend IP on port 1433.
2. The LB evaluates the 5-tuple hash to determine which backend VM should receive the connection.
3. The LB checks the Health Probe status. It selects VM-2 (which is healthy).
4. The LB forwards the packet to VM-2's private IP (without altering the payload).
5. VM-2 processes the SQL query and sends the response back to the client.

## 6. Real-World Production Use Cases
1. **High Availability Databases:** Internal Load Balancers are standard for routing traffic to SQL Server Always On Availability Groups inside a VNet.
2. **Outbound Internet Access (SNAT):** Using a Public Load Balancer to provide a shared outbound Public IP for a pool of backend VMs that only have private IPs.
3. **Massive UDP Workloads:** Gaming servers or IoT ingestion endpoints where Layer 7 inspection is unnecessary and ultra-low latency is required.

## 7. Architecture & Design Considerations
- **SKU Selection:** **Always choose the Standard SKU.** The Basic SKU is deprecated, lacks Availability Zone support, has no SLA by itself, and is closed to inbound traffic by default unless an NSG allows it.
- **Availability Zones:** A Standard Public IP and Standard LB can be Zone-Redundant, surviving a datacenter failure within the region.
- **Floating IP (DSR):** Required for SQL Always On Availability Groups. The backend VM's listener is configured with the LB's frontend IP, allowing the database to process traffic without IP mismatch errors.

## 8. Microsoft Best Practices
- **Do not use Load Balancer for SNAT in large deployments:** While it can provide outbound internet access (Source NAT), heavy traffic causes SNAT port exhaustion. Use **Azure NAT Gateway** for outbound traffic instead.
- **Tune Health Probes:** Don't set probe intervals too aggressively (e.g., every 5 seconds) for heavy applications, as the probe itself can cause CPU load. The default 15-second interval is a safe starting point.

## 9. Security Best Practices
- **NSG Enforcement:** Standard Load Balancer drops all traffic by default unless an explicit Network Security Group (NSG) rule is applied to the backend subnet/NIC allowing the traffic.
- **Internal First:** Always use an Internal Load Balancer unless external public access is strictly required.

## 10. Monitoring & Observability
- **Metrics:** Monitor `Data Path Availability` (is the LB functioning?) and `Health Probe Status` (are the backends alive?).
- **SNAT Connections:** Monitor `SNAT Connection Count` to ensure you are not hitting port exhaustion limits (65,536 ephemeral ports per public IP by default).

## 11. Backup & Disaster Recovery
- **Regional Limitation:** The LB is bound to a single region.
- **Disaster Recovery:** Deploy a secondary Load Balancer in your paired DR region. Place an **Azure Traffic Manager** globally in front of both Load Balancers to route traffic to the DR region if the primary region goes offline.

## 12. Cost Optimization Techniques
- Standard Load Balancer is billed based on a fixed hourly rate plus the volume of data processed (per GB).
- To save costs on massive data transfers within Azure, ensure cross-zone traffic is minimized where possible, though LB data processing fees are generally very low.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Load Balancer?
   **A:** A Layer 4 (TCP/UDP) load balancer that distributes incoming traffic among healthy instances.
2. **Q:** Internal vs Public Load Balancer?
   **A:** Public has a public IP (internet facing). Internal has a private IP (for traffic inside the VNet).

### Intermediate
3. **Q:** What are Load Balancer Health Probes?
   **A:** Health checks sent by the LB to a specific port on the backend VMs. If a VM fails the probe, the LB stops sending traffic to it.
4. **Q:** What is a Load Balancing Rule?
   **A:** It maps a frontend IP and port (e.g., Public IP port 80) to a backend pool and port, defining how traffic is distributed.
5. **Q:** What is SNAT (Source Network Address Translation) in Azure Load Balancer?
   **A:** It translates the private IPs of backend VMs to the public IP of the load balancer when the VMs initiate outbound internet connections.

### Advanced
6. **Q:** Why might you experience port exhaustion on a Standard Load Balancer, and how do you fix it?
   **A:** If many VMs make high volumes of outbound connections, the SNAT ports (65,536 per public IP) run out. Fix it by deploying an Azure NAT Gateway for dedicated, scalable outbound connectivity.
7. **Q:** How does the Standard SKU differ from the Basic SKU Load Balancer?
   **A:** Standard is secure by default (requires NSGs), supports Availability Zones, has a larger backend pool limit (1,000 vs 300 instances), provides rich metrics in Azure Monitor, and the Basic SKU is deprecated.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** Backend VMs are running, but the Load Balancer is not routing traffic to them.
  - **Resolution:**
    1. Check the Health Probe metrics. If the probe is failing, verify the application service (e.g., IIS/Nginx) is running and listening on the correct port.
    2. Check the Guest OS firewall (Windows Defender Firewall / iptables). It must allow traffic from the Azure Health Probe IP (`168.63.129.16`).
    3. Check the Azure NSG applied to the backend subnet/NIC. It must allow inbound traffic on the designated application port.
- **Scenario:** Outbound internet connections from backend VMs are failing intermittently under heavy load.
  - **Resolution:** You are experiencing SNAT port exhaustion. Deploy an Azure NAT Gateway to the backend subnet to handle massive outbound concurrent connections without port exhaustion.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create Public IP
az network public-ip create --resource-group rg-prod --name pip-lb --sku Standard

# Create Standard Load Balancer
az network lb create \
    --resource-group rg-prod \
    --name lb-prod \
    --sku Standard \
    --public-ip-address pip-lb \
    --frontend-ip-name frontend \
    --backend-pool-name backend

# Create Health Probe
az network lb probe create -g rg-prod --lb-name lb-prod -n probe-tcp-80 --protocol tcp --port 80

# Create LB Rule
az network lb rule create -g rg-prod --lb-name lb-prod -n rule-80 \
    --protocol tcp --frontend-port 80 --backend-port 80 \
    --frontend-ip-name frontend --backend-pool-name backend --probe-name probe-tcp-80
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_public_ip" "pip" {
  name                = "pip-lb"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  allocation_method   = "Static"
  sku                 = "Standard"
}

resource "azurerm_lb" "lb" {
  name                = "lb-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.pip.id
  }
}

resource "azurerm_lb_backend_address_pool" "pool" {
  loadbalancer_id = azurerm_lb.lb.id
  name            = "BackEndAddressPool"
}

resource "azurerm_lb_probe" "probe" {
  loadbalancer_id = azurerm_lb.lb.id
  name            = "http-probe"
  port            = 80
}

resource "azurerm_lb_rule" "rule" {
  loadbalancer_id                = azurerm_lb.lb.id
  name                           = "LBRule"
  protocol                       = "Tcp"
  frontend_port                  = 80
  backend_port                   = 80
  frontend_ip_configuration_name = "PublicIPAddress"
  backend_address_pool_ids       = [azurerm_lb_backend_address_pool.pool.id]
  probe_id                       = azurerm_lb_probe.probe.id
}
```

## 17. Production Readiness Checklist
- [ ] Is the Standard SKU selected (Basic SKU is deprecated)?
- [ ] Are health probes testing the actual application port (not just ICMP/TCP ping)?
- [ ] Is a NAT Gateway configured for outbound traffic to prevent SNAT port exhaustion?
- [ ] Does the NSG explicitly allow traffic from the Azure Health Probe IP (`168.63.129.16`)?
- [ ] Are backend VMs distributed across Availability Zones for zone-redundant HA?