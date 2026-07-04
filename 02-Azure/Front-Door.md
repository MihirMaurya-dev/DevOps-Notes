---
category: Azure-Networking
tags: [azure, front-door, global, cdn, waf, architecture]
type: enterprise-architect-guide
status: active
---

# 🚪 Azure Front Door - Enterprise Architect Guide

## 1. Introduction
Azure Front Door is a global Layer 7 load balancer, Web Application Firewall (WAF), and Content Delivery Network (CDN) all rolled into one. While Application Gateway handles traffic within a single region, Front Door sits at the absolute edge of Microsoft's global network, routing users from anywhere in the world to your fastest and healthiest backend region.

## 2. Why This Service Exists
If you have a global web application hosted in both New York and London, a user in the UK connecting directly to New York suffers terrible latency across the Atlantic. Furthermore, a massive DDoS attack on your region could take down your VNet. Front Door exists to terminate the user's connection at the closest local Microsoft Point of Presence (PoP) (e.g., London), cache static content locally, and route dynamic traffic over Microsoft's high-speed private WAN, providing massive performance and security benefits.

## 3. Architecture
- **Scope:** Global.
- **Layer:** Layer 7 (Application - HTTP/HTTPS).
- **Under the Hood:** It uses **Anycast** routing. Unlike DNS routing (Traffic Manager), Front Door advertises the exact same IP address worldwide. Border Gateway Protocol (BGP) naturally routes the user's packets to the physically closest edge node. It terminates the TCP and TLS connection at the edge, drastically reducing the round-trip time (RTT) for the TLS handshake.

## 4. Core Components
- **Domains:** Custom domains (e.g., `www.contoso.com`) and Azure-managed TLS certificates.
- **Origin Groups:** The logical grouping of your backend resources (e.g., App Services in East US and West Europe).
- **Origins:** The actual backend endpoints within an Origin Group.
- **Routes:** Rules that map a domain and a URL path pattern (e.g., `/images/*`) to an Origin Group.
- **Rule Engine:** Powerful edge-computing engine to modify HTTP headers, perform URL redirects, or change caching behavior on the fly.
- **WAF Policy:** Global Web Application Firewall to block attacks at the edge before they reach your Azure regions.

## 5. Step-by-Step Request Flow
**Scenario:** A user in Sydney requests a dynamic API payload from a backend hosted in East US.
1. The user's DNS resolves to Front Door's global Anycast IP.
2. The user's traffic is routed to the Sydney Edge Node (PoP) via BGP's shortest path.
3. The TLS handshake is completed immediately in Sydney (saving hundreds of milliseconds vs. connecting to East US directly).
4. The Sydney node checks if the payload is cached. It is a dynamic API call, so it is a Cache Miss.
5. The WAF inspects the payload in Sydney and approves it.
6. The Sydney node forwards the request over Microsoft's private backbone to the East US backend.
7. The East US backend responds. Front Door streams the response back to the user in Sydney.

## 6. Real-World Production Use Cases
1. **Global Active-Active Architectures:** Deploying instances of a web app in US, Europe, and Asia, using Front Door to route users to their local instance, and automatically failing over if one region goes down.
2. **Global CDN:** Caching large images, CSS, and JS files for a media site at 100+ edge locations globally, drastically reducing the load on the backend web servers.
3. **Zero-Trust Edge Security:** Using Front Door Premium to connect to internal, private VNets via Azure Private Link, meaning the backend servers have absolutely zero public IP exposure.

## 7. Architecture & Design Considerations
- **Standard vs Premium SKU:**
  - **Standard** is optimized for content delivery (CDN + WAF custom rules).
  - **Premium** includes Microsoft-managed WAF rule sets, advanced security analytics, and critically, **Private Link** support for connecting to private (non-public) backends.
- **Traffic Manager vs Front Door:** Use Traffic Manager for non-HTTP traffic (UDP/TCP) or when you want the client to connect directly to a regional endpoint. Use Front Door for HTTP/HTTPS web applications requiring global acceleration, caching, and SSL offloading at the edge.

## 8. Microsoft Best Practices
- **Lock Down the Backend:** If you are not using Private Link, your backends (App Service, Application Gateway) still have public IPs. You MUST restrict their NSGs or access restrictions to only accept traffic from the `AzureFrontDoor.Backend` service tag AND validate the `X-Azure-FDID` HTTP header to ensure traffic originates from *your specific* Front Door profile — not any Front Door instance.
- **Use Managed Certificates:** Let Azure manage your TLS certificates. Front Door will automatically generate, rotate, and deploy certificates for your custom domains at no extra cost.

## 9. Security Best Practices
- **WAF at the Edge:** Always deploy WAF policies on Front Door. Blocking attacks at the edge saves backend compute costs and prevents volumetric Layer 7 attacks from overwhelming your regional infrastructure.
- **Private Link (Premium):** Use Front Door Premium to create a Private Endpoint to your backend Internal Load Balancer, App Service, or Application Gateway. Traffic remains entirely on the Microsoft backbone, providing ultimate security.

## 10. Monitoring & Observability
- **Log Analytics:** Route `FrontDoorAccessLog` and `FrontDoorWebApplicationFirewallLog` to a Log Analytics Workspace for query and alerting.
- **Built-in Reports:** The Front Door portal provides excellent out-of-the-box reports on Cache Hit Ratio, Latency by Geography, Origin Health, and Top WAF Rules triggered.

## 11. Backup & Disaster Recovery
- Front Door is inherently a DR tool. It continuously monitors the health of your Origin Groups via health probes. If the East US region suffers an outage, Front Door automatically detects the failed health probes and routes all traffic to the West Europe origin seamlessly.
- Front Door configuration (routes, domains, WAF policies) must be maintained via Terraform/Bicep for version control and instant recreation.

## 12. Cost Optimization Techniques
- **Caching:** Maximize cache hit ratios. Serving data from the edge cache is dramatically cheaper than pulling it from your origin, and it reduces compute costs on your origin servers.
- **Data Transfer Costs:** Front Door charges for outbound data transfer from the edge to the client. Be aware that massive video or file streaming workloads will incur high bandwidth costs; evaluate Azure CDN or Blob Storage static hosting for large media files.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Front Door?
   **A:** A global, Layer 7 load balancer, CDN, and WAF for modern web applications that terminates connections at the nearest Microsoft edge PoP.
2. **Q:** Azure Front Door vs Application Gateway?
   **A:** Front Door is Global and includes a CDN with Anycast routing. App Gateway is Regional and operates entirely within a specific VNet.

### Intermediate
3. **Q:** What routing mechanism does Front Door use?
   **A:** Anycast routing. The same IP address is advertised globally from all PoPs; BGP routes users to the physically closest Microsoft edge node for lowest latency.
4. **Q:** Can Front Door act as a Web Application Firewall?
   **A:** Yes, WAF policies can be attached to Front Door to block malicious traffic globally at the edge before it ever reaches your region.
5. **Q:** How does caching work in Front Door?
   **A:** It caches static assets (images, CSS, JS) at edge PoP locations near users, dramatically reducing load times and backend server strain.

### Advanced
6. **Q:** Can Front Door route traffic to private backend resources that are not exposed to the internet?
   **A:** Yes, Front Door Premium supports connecting to backend services privately using Azure Private Link, meaning the backend requires no public IP.
7. **Q:** How do you prevent users from bypassing Front Door and hitting your backend App Service directly?
   **A:** Configure the App Service to only accept traffic containing the specific `X-Azure-FDID` header matching your Front Door profile ID, combined with an IP restriction to the `AzureFrontDoor.Backend` service tag. Alternatively, use Private Link (Premium SKU).

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** The backend web app returns a `503 Service Unavailable` through Front Door.
  - **Resolution:** Front Door's health probes are failing for all origins in the group. Check if the backend application is online. Check if the backend firewall/NSG allows inbound traffic from the `AzureFrontDoor.Backend` IP service tag. Verify the probe path (e.g., `/healthz`) is returning HTTP 200 OK.
- **Scenario:** Users are seeing stale/old content on the website.
  - **Resolution:** The edge nodes have cached the old content. Navigate to the Front Door portal and execute a **Cache Purge** operation on the specific URL path (e.g., `/css/styles.css` or `/*`) to force edge nodes to fetch the latest version from the origin.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create a Front Door Profile (Standard SKU)
az afd profile create -g rg-global-prod --profile-name fd-global-prod --sku Standard_AzureFrontDoor

# Create an Endpoint
az afd endpoint create -g rg-global-prod --endpoint-name web-endpoint --profile-name fd-global-prod

# Create an Origin Group with health probing
az afd origin-group create -g rg-global-prod --origin-group-name og-web --profile-name fd-global-prod \
  --probe-request-type GET --probe-path /healthz --probe-protocol Https --probe-interval-in-seconds 30

# Add an Origin (Backend)
az afd origin create -g rg-global-prod --host-name myapp-eastus.azurewebsites.net \
  --origin-group-name og-web --origin-name origin-eastus --profile-name fd-global-prod \
  --origin-host-header myapp-eastus.azurewebsites.net --priority 1 --weight 1000
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_cdn_frontdoor_profile" "fd" {
  name                = "fd-global-prod"
  resource_group_name = azurerm_resource_group.rg.name
  sku_name            = "Standard_AzureFrontDoor"
}

resource "azurerm_cdn_frontdoor_endpoint" "endpoint" {
  name                     = "web-endpoint"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.fd.id
}

resource "azurerm_cdn_frontdoor_origin_group" "og" {
  name                     = "og-web"
  cdn_frontdoor_profile_id = azurerm_cdn_frontdoor_profile.fd.id

  load_balancing {
    additional_latency_in_milliseconds = 50
    sample_size                        = 4
    successful_samples_required        = 3
  }

  health_probe {
    path                = "/healthz"
    protocol            = "Https"
    request_type        = "GET"
    interval_in_seconds = 30
  }
}

resource "azurerm_cdn_frontdoor_origin" "origin" {
  name                           = "origin-eastus"
  cdn_frontdoor_origin_group_id  = azurerm_cdn_frontdoor_origin_group.og.id
  enabled                        = true
  host_name                      = "myapp-eastus.azurewebsites.net"
  origin_host_header             = "myapp-eastus.azurewebsites.net"
  certificate_name_check_enabled = true
  priority                       = 1
  weight                         = 1000
}

resource "azurerm_cdn_frontdoor_route" "route" {
  name                          = "default-route"
  cdn_frontdoor_endpoint_id     = azurerm_cdn_frontdoor_endpoint.endpoint.id
  cdn_frontdoor_origin_group_id = azurerm_cdn_frontdoor_origin_group.og.id
  cdn_frontdoor_origin_ids      = [azurerm_cdn_frontdoor_origin.origin.id]
  supported_protocols           = ["Http", "Https"]
  patterns_to_match             = ["/*"]
  forwarding_protocol           = "HttpsOnly"
  https_redirect_enabled        = true
}
```

## 17. Production Readiness Checklist
- [ ] Is WAF attached to the Front Door profile in Prevention mode?
- [ ] Are custom domains configured with Azure Managed TLS Certificates?
- [ ] Are backends locked down to only accept traffic from this specific Front Door profile (X-Azure-FDID header + AzureFrontDoor.Backend service tag)?
- [ ] Is caching enabled and tuned for static asset paths (`/images/*`, `/css/*`, `/js/*`)?
- [ ] Are health probes targeting a meaningful application health endpoint (e.g., `/healthz`) with HTTPS and an appropriate interval?
- [ ] Is the Front Door configuration fully managed via Terraform/Bicep?