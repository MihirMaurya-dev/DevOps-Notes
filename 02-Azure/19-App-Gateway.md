---
category: Azure-Networking
tags: [azure, app-gateway, waf, layer7, architecture]
type: enterprise-architect-guide
status: active
---

# 🌍 Azure Application Gateway - Enterprise Architect Guide

## 1. Introduction
Azure Application Gateway (AppGW) is a highly scalable, regional Layer 7 web traffic load balancer. Unlike a standard Load Balancer (Layer 4) which only looks at IP addresses and ports, AppGW understands the HTTP/HTTPS protocol. It can make intelligent routing decisions based on the URL path, host headers, and can perform TLS/SSL termination.

## 2. Why This Service Exists
Modern web applications and microservices require advanced traffic management. For example, you might want `contoso.com/images` to be routed to a cheap VM storage tier, while `contoso.com/api` routes to an expensive, high-performance Kubernetes cluster. Additionally, web apps need protection from common internet attacks (like SQL injection). AppGW provides both URL-based routing and a built-in Web Application Firewall (WAF) to solve these problems.

## 3. Architecture
- **Scope:** Regional.
- **Layer:** Layer 7 (Application - HTTP/HTTPS/WebSocket).
- **Under the Hood:** AppGW operates as a reverse proxy. It terminates the client's connection, inspects the request, evaluates routing rules, and then creates a *new* TCP connection to the backend server. It requires a dedicated, empty subnet within your VNet to deploy its managed instances.

## 4. Core Components
- **Frontend IP:** Public IP, Private IP, or both.
- **Listeners:** Listen on a specific port (e.g., 443) and protocol for incoming requests. Evaluate SSL certificates.
- **Routing Rules:** Ties a Listener to a Backend Pool and dictates *how* to route (Basic routing vs Path-based routing).
- **Backend Pools:** The destinations (VMs, VMSS, AKS pods, App Services, or IPs).
- **HTTP Settings:** Defines the connection behavior to the backend (e.g., re-encrypt with TLS, stickiness/cookie affinity, custom health probes).
- **Web Application Firewall (WAF):** Evaluates HTTP requests against OWASP Core Rule Sets (CRS) to block malicious payloads.

## 5. Step-by-Step Request Flow
**Scenario:** A user accesses an e-commerce API (`https://shop.com/api/cart`).
1. Client establishes a TLS connection to the AppGW's Public IP on port 443.
2. AppGW terminates the TLS connection using the certificate bound to its **Listener**.
3. AppGW inspects the decrypted HTTP payload. The **WAF** scans it for SQL injection or Cross-Site Scripting (XSS).
4. If clean, AppGW evaluates the **Routing Rule**. It sees the `/api/*` path and maps it to the `AKS-Backend-Pool`.
5. AppGW checks the **HTTP Settings**. It re-encrypts the request (End-to-End TLS) and forwards it to an AKS pod.
6. The response returns through the AppGW back to the client.

## 6. Real-World Production Use Cases
1. **AKS Ingress Controller:** Using the Application Gateway Ingress Controller (AGIC) to expose Kubernetes microservices directly to the internet with enterprise WAF protection.
2. **SSL Offloading:** Centralizing SSL certificate management on the AppGW so backend VMs don't spend CPU cycles encrypting/decrypting traffic.
3. **Multi-Site Hosting:** Hosting multiple domains (e.g., `brand1.com` and `brand2.com`) on the same Application Gateway, routing to completely different backend server pools.

## 7. Architecture & Design Considerations
- **Dedicated Subnet:** AppGW v2 requires a dedicated subnet. A `/24` is recommended for production deployments with autoscaling. No other resources may reside in this subnet.
- **SKU Selection:** Always choose **WAF_v2**. The v1 SKUs are legacy and do not support autoscaling or zone redundancy. WAF_v2 provides faster provisioning and lower latency.
- **Autoscaling vs Manual:** v2 allows autoscaling. You define a minimum and maximum instance count. This ensures you can handle massive traffic spikes without paying for maximum capacity 24/7.

## 8. Microsoft Best Practices
- **End-to-End TLS:** In production, do not send unencrypted HTTP traffic from the AppGW to the backend. Terminate TLS at the AppGW for WAF inspection, but re-encrypt traffic to the backend to ensure Zero Trust network security.
- **Key Vault Integration:** Store AppGW SSL certificates in Azure Key Vault. AppGW uses a User-Assigned Managed Identity to auto-retrieve and auto-renew certificates without human intervention.

## 9. Security Best Practices
- **WAF Prevention Mode:** Deploy WAF initially in `Detection` mode to tune rules and avoid false positives. Once tuned, strictly enforce `Prevention` mode.
- **Disable Old TLS:** Configure the AppGW Listener to require TLS 1.2 as the minimum. Disable TLS 1.0 and 1.1 to comply with PCI-DSS and other standards.
- **NSG on AppGW Subnet:** Be extremely careful. AppGW v2 requires ports **65200–65535** open for inbound Azure infrastructure management traffic from the `GatewayManager` service tag. Misconfiguring the NSG will cause AppGW to enter a failed state.

## 10. Monitoring & Observability
- **Diagnostic Logs:** Send `ApplicationGatewayAccessLog`, `ApplicationGatewayPerformanceLog`, and `ApplicationGatewayFirewallLog` to a Log Analytics Workspace.
- **Metrics:** Alert on `Unhealthy Host Count` and `Failed Requests`.
- **WAF Tuning:** Use Log Analytics KQL queries on the `ApplicationGatewayFirewallLog` to identify which WAF rules are blocking legitimate traffic (false positives) so you can create custom exclusion rules.

## 11. Backup & Disaster Recovery
- **Regional:** AppGW is bound to one region.
- **DR Architecture:** Deploy an identical AppGW in a secondary region. Use **Azure Front Door** (for global HTTP/HTTPS) or **Traffic Manager** (for DNS-based failover) to route users globally, failing over to the secondary AppGW if the primary region goes down.
- **State:** Backup AppGW configuration entirely via Terraform/Bicep.

## 12. Cost Optimization Techniques
- AppGW v2 billing is based on a fixed hourly capacity unit rate PLUS Capacity Units (CU). A CU is a blend of compute, persistent connections, and throughput consumed.
- **Autoscale Limits:** Set a reasonable maximum autoscale limit so a DDoS attack does not cause the AppGW to scale infinitely and generate a massive bill.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Application Gateway?
   **A:** A regional Layer 7 (HTTP/HTTPS) web traffic load balancer with built-in WAF, URL routing, and SSL termination capabilities.
2. **Q:** What is Web Application Firewall (WAF)?
   **A:** A feature of AppGW that protects web apps from common exploits like SQL injection and cross-site scripting (XSS), based on OWASP Core Rule Sets.

### Intermediate
3. **Q:** What is URL-based routing?
   **A:** Routing traffic based on the URL path. E.g., `contoso.com/images` goes to an image server pool, while `contoso.com/api` goes to an API server pool.
4. **Q:** What is SSL Offloading (SSL Termination)?
   **A:** AppGW decrypts incoming HTTPS traffic so backend servers don't spend CPU resources doing decryption.
5. **Q:** What is Cookie-Based Affinity?
   **A:** Also known as sticky sessions; it uses a cookie to ensure a user's subsequent requests are routed to the same backend server.

### Advanced
6. **Q:** How does End-to-End TLS work in Application Gateway?
   **A:** AppGW decrypts the traffic at the listener to inspect it (WAF/routing), and then re-encrypts it before sending it to the backend servers, ensuring complete transit security from client to server.
7. **Q:** How is AppGW integrated with Azure Kubernetes Service (AKS)?
   **A:** Via the Application Gateway Ingress Controller (AGIC), which allows AKS to configure AppGW automatically based on Kubernetes Ingress resource definitions.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** The AppGW returns a `502 Bad Gateway` error to users.
  - **Resolution:** This means the AppGW cannot reach the backend.
    1. Check Backend Health in the portal to see which backend is unhealthy.
    2. Check if the NSG on the backend VM's subnet is blocking inbound traffic from the AppGW subnet CIDR.
    3. If using End-to-End TLS, ensure the custom health probe expects the correct host name and that the backend SSL certificate is trusted by AppGW.
- **Scenario:** WAF is blocking legitimate user file uploads.
  - **Resolution:** Query the `ApplicationGatewayFirewallLog` to find the specific WAF rule ID triggering the block. Create a WAF Exclusion for that specific request attribute (e.g., ignore inspection on a specific JSON body field or request header).

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create Dedicated Subnet
az network vnet subnet create -g rg-prod --vnet-name vnet-core-prod -n snet-appgw --address-prefixes 10.0.2.0/24

# Create Public IP
az network public-ip create -g rg-prod -n pip-appgw --sku Standard

# Create WAF v2 Application Gateway
az network application-gateway create \
  -g rg-prod \
  -n appgw-prod \
  --sku WAF_v2 \
  --public-ip-address pip-appgw \
  --vnet-name vnet-core-prod \
  --subnet snet-appgw \
  --min-capacity 2 --max-capacity 10
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_application_gateway" "network" {
  name                = "appgw-prod"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location

  sku {
    name = "WAF_v2"
    tier = "WAF_v2"
  }

  autoscale_configuration {
    min_capacity = 2
    max_capacity = 10
  }

  gateway_ip_configuration {
    name      = "my-gateway-ip-configuration"
    subnet_id = azurerm_subnet.appgw.id
  }

  frontend_port {
    name = "frontend-port-https"
    port = 443
  }

  frontend_ip_configuration {
    name                 = "frontend-ip"
    public_ip_address_id = azurerm_public_ip.pip.id
  }

  backend_address_pool {
    name = "backend-pool"
  }

  backend_http_settings {
    name                  = "https-settings"
    cookie_based_affinity = "Disabled"
    path                  = "/"
    port                  = 443
    protocol              = "Https"
    request_timeout       = 60
  }

  http_listener {
    name                           = "https-listener"
    frontend_ip_configuration_name = "frontend-ip"
    frontend_port_name             = "frontend-port-https"
    protocol                       = "Https"
    ssl_certificate_name           = "appgw-ssl-cert"
  }

  request_routing_rule {
    name                       = "rule1"
    rule_type                  = "Basic"
    http_listener_name         = "https-listener"
    backend_address_pool_name  = "backend-pool"
    backend_http_settings_name = "https-settings"
    priority                   = 100
  }

  waf_configuration {
    enabled          = true
    firewall_mode    = "Prevention"
    rule_set_type    = "OWASP"
    rule_set_version = "3.2"
  }
}
```

## 17. Production Readiness Checklist
- [ ] Is WAF enabled in Prevention mode (not Detection)?
- [ ] Are SSL certificates pulled dynamically from Azure Key Vault via Managed Identity?
- [ ] Is TLS 1.2 the minimum enforced version (TLS 1.0/1.1 disabled)?
- [ ] Is Autoscaling enabled with appropriate minimum and maximum capacity boundaries?
- [ ] Are End-to-End TLS and custom health probes configured for backend HTTPS?
- [ ] Is the NSG on the AppGW subnet allowing ports 65200–65535 from the `GatewayManager` service tag?
- [ ] Is diagnostic logging (Access, Performance, and WAF logs) enabled and routed to Log Analytics?