---
updated: 2026-07-26
tags: [architecture, landing-zone, zero-trust, networking, interview-prep]
source: generated
---

# Architecture Fundamentals Interview Questions

## Basics

1. **What is the fundamental difference between a Hub-and-Spoke and a Mesh network architecture?**
   In a Hub-and-Spoke architecture, all traffic routes through a central hub, making it easier to monitor, secure, and manage centralized services like firewalls or VPN gateways. In contrast, a Mesh architecture connects every node directly to every other node, providing high redundancy and lower latency between endpoints. While Hub-and-Spoke is cost-effective and easier to secure centrally, Mesh networks can become complex and expensive to scale as the number of nodes increases.

2. **Can you explain the concept of a DMZ (Demilitarized Zone)?**
   A DMZ is a physical or logical subnetwork that contains and exposes an organization's external-facing services to an untrusted network, typically the internet. Its primary purpose is to add an additional layer of security to an organization's local area network (LAN); an external network node can access only what is exposed in the DMZ, while the rest of the organization's network is firewalled. Common services placed in a DMZ include web servers, mail servers, and DNS servers.

3. **What is Network Segmentation and why is it important?**
   Network segmentation is the practice of dividing a computer network into smaller, isolated subnets. This improves security and performance by restricting communication between different parts of the network to only what is necessary. If a threat actor breaches one segment, segmentation prevents them from easily moving laterally to access sensitive data in other segments.

4. **Define the core principle of Zero Trust Architecture.**
   The core principle of Zero Trust is "never trust, always verify." It assumes that threats can exist both outside and inside the network, meaning no user or device is trusted by default, regardless of their location. Every access request must be fully authenticated, authorized, and encrypted before granting access to resources.

5. **What does Defence-in-Depth mean in network architecture?**
   Defence-in-Depth is a cybersecurity strategy that uses multiple layers of security controls throughout an information technology system. If one security control fails or is bypassed, another layer is in place to thwart the attack. This approach involves a combination of physical, technical, and administrative controls to protect network resources and data.

## Intermediate

6. **How does a Hub-and-Spoke topology simplify the deployment of security appliances compared to a Mesh topology?**
   In a Hub-and-Spoke topology, all traffic between spokes and the internet must pass through the central hub. This allows organizations to deploy a single set of expensive security appliances, such as Next-Generation Firewalls (NGFW) or Intrusion Detection Systems (IDS), in the hub rather than replicating them in every spoke. In a full mesh, traffic flows directly between nodes, meaning security controls would need to be distributed across all connections, significantly increasing cost and management complexity.

7. **How do you implement micro-segmentation in modern cloud environments?**
   Micro-segmentation involves creating secure zones in data centers and cloud deployments that allow you to isolate workloads from one another and secure them individually. In modern cloud environments, this is typically implemented using software-defined networking (SDN) and identity-based security policies rather than physical firewalls. For example, in Kubernetes, you use Network Policies to control traffic between pods, or in AWS, Security Groups and Network ACLs applied to specific ENIs.

8. **What are the key components required to build a Zero Trust architecture?**
   Building a Zero Trust architecture requires several key components: robust Identity and Access Management (IAM) with Multi-Factor Authentication (MFA), endpoint security and device posture checking, micro-segmentation, and continuous monitoring. A policy engine evaluates the context of every request (user identity, device health, location, time) before a policy administrator grants dynamic, least-privilege access to the specific resource.

9. **Explain how a DMZ interacts with internal and external firewalls.**
   A typical DMZ is created using two firewalls: an external firewall facing the internet and an internal firewall facing the private network. The external firewall allows traffic from the internet to access specific services in the DMZ (e.g., HTTP on port 80). The internal firewall is much stricter, typically only allowing traffic from the DMZ to the internal network if it is absolutely necessary (like a web server querying an internal database on a specific port), while denying all other inbound connections.

10. **How does Defence-in-Depth apply to data protection at rest and in transit?**
    For data at rest, Defence-in-Depth might involve file-level encryption, database encryption, full disk encryption, and strict access controls via IAM policies. For data in transit, it involves using secure protocols like TLS 1.3, enforcing HTTPS on load balancers, and establishing VPNs or IPsec tunnels for network-level encryption. By combining these layers, an attacker must bypass multiple encryption and authentication mechanisms to access readable data.

11. **Can you give an example of CLI commands to check network routing for a potential Hub-and-Spoke setup on Linux?**
    You can use tools like `traceroute` or `ip route` to verify routing paths.
    ```bash
    # View the routing table
    ip route show
    
    # Trace the route to a specific spoke IP to verify it goes through the hub
    traceroute 10.1.2.5
    ```
    If the architecture is Hub-and-Spoke, the traceroute to another spoke's subnet should show the hub's gateway IP as the first or second hop, rather than a direct connection.

## Advanced

12. **In a global cloud deployment, when would you choose a Transit Gateway (Hub-and-Spoke) over VPC Peering (Mesh)?**
    VPC Peering is a direct connection between two VPCs, creating a mesh if many VPCs need to communicate, which becomes complex to manage as the number of peering connections grows factorially. A Transit Gateway acts as a central hub, drastically simplifying routing management and allowing for centralized traffic inspection. You would choose a Transit Gateway when you have a large number of VPCs (e.g., >10), require centralized egress/ingress points, or need to integrate on-premises networks via Direct Connect or VPN at scale.

13. **How do you maintain a Zero Trust model when integrating legacy applications that do not support modern authentication?**
    Legacy applications can be integrated into a Zero Trust model using Identity-Aware Proxies (IAP) or reverse proxies. The proxy acts as the gateway, enforcing strong authentication (e.g., SAML, OIDC, MFA) and evaluating device posture before allowing the request to proceed. Once the proxy verifies the request, it can pass the traffic to the legacy application using headers, internal mutual TLS (mTLS), or even standard protocols that the legacy app understands, effectively shielding it from unauthenticated access.

14. **Describe the difference between macro-segmentation and micro-segmentation.**
    Macro-segmentation divides a network into broad, distinct zones based on high-level functions or departments, typically using traditional firewalls and VLANs (e.g., separating HR network from the Engineering network). Micro-segmentation goes much deeper, isolating individual workloads, applications, or even specific processes regardless of their physical or logical network location. Micro-segmentation relies on software-defined policies and identity, allowing granular control (e.g., Web Server A can talk to Database B on port 3306, but Web Server C cannot).

15. **How does implementing mTLS (Mutual TLS) contribute to a Zero Trust architecture?**
    mTLS ensures that both the client and the server authenticate each other using cryptographic certificates before establishing a connection. In a Zero Trust architecture, this means that network location is irrelevant; every service-to-service communication is verified and encrypted. This is heavily used in service meshes (like Istio) to provide identity-based segmentation and protect against man-in-the-middle attacks and lateral movement within the network.

16. **What are the challenges of managing routing in a full mesh architecture across multiple cloud regions?**
    Managing a full mesh across multiple regions involves significant complexity in configuring and maintaining routing tables, as the number of connections grows exponentially. It can lead to overlapping IP CIDR blocks if not meticulously planned. Furthermore, ensuring consistent security policies and monitoring traffic across all direct links is difficult without a centralized inspection point, increasing the risk of misconfigurations leading to security breaches.

17. **How does a reverse proxy placed in a DMZ enhance security for backend servers?**
    A reverse proxy in the DMZ terminates the incoming client connection, inspects the traffic (often performing SSL/TLS termination and WAF filtering), and then initiates a new, separate connection to the backend server. This hides the internal network's IP structure, prevents direct attacks on the backend servers (like DDoS or buffer overflows), and provides a centralized point for logging and access control enforcement.

## Scenario-Based

18. **Scenario: Your company is acquiring a startup and needs to integrate their AWS environment with yours. Their environment is currently a flat network. How do you approach this integration securely?**
    First, I would avoid directly peering their flat network with our internal networks to prevent potential lateral movement of existing threats. I would set up a Hub-and-Spoke architecture, connecting their environment as an isolated spoke to our central Transit Gateway. I would then deploy a Next-Generation Firewall in the hub to inspect all traffic between the acquired company and our corporate resources. Finally, I would initiate a project to segment their flat network into distinct tiers (e.g., web, app, db) using Security Groups and align them with our Zero Trust policies.

19. **Scenario: A developer wants to open a database port to the public internet for debugging purposes. Using Defence-in-Depth principles, how do you provide access securely without exposing the database?**
    Exposing a database port to the internet violates multiple security principles. Using Defence-in-Depth, I would first deny the request. Instead, I would provide access via a secure Bastion Host or an Identity-Aware Proxy. The developer would need to authenticate with MFA to access the proxy or bastion. Furthermore, the database would remain in a private subnet, and its firewall rules would only allow traffic from the specific Bastion/Proxy IP. Additionally, I would ensure database auditing is enabled to log the developer's activities.

20. **Scenario: You are designing the architecture for a new highly sensitive financial application. How do you implement Zero Trust and Network Segmentation for this application?**
    I would deploy the application in its own isolated VPC or network segment. I would use micro-segmentation to isolate the presentation, application, and data tiers, ensuring they only communicate over explicitly allowed ports and protocols using mTLS. Access to the application would be protected by an Identity Provider enforcing MFA and device compliance checks. Even database administrators would require just-in-time, time-bound access through a secure jump box to interact with the data tier.

21. **Scenario: Your organization is migrating from a traditional data center to a hybrid cloud model. How do you evolve the existing DMZ architecture?**
    In a hybrid model, the traditional perimeter-based DMZ must evolve into a distributed security model. While the on-premises DMZ might remain for legacy services, cloud-native services should utilize cloud-specific constructs. I would use Web Application Firewalls (WAF), API Gateways, and Cloud Load Balancers at the edge to inspect and filter inbound internet traffic. For connectivity between on-premises and cloud, I would establish secure IPsec VPNs or dedicated links, treating the cloud environment as a separate, governed segment rather than an implicit extension of the corporate LAN.

22. **Scenario: An alert indicates that a web server in your DMZ has been compromised. How does your architecture limit the blast radius?**
    If the architecture is well-designed with Defence-in-Depth and strict segmentation, the blast radius is highly constrained. The internal firewall prevents the compromised web server from initiating arbitrary connections to the internal network. The web server should only have the minimum necessary permissions (least privilege) to access internal resources, such as a specific database on a specific port. Additionally, egress filtering on the external firewall would block the server from communicating with known malicious command-and-control IP addresses, slowing down data exfiltration.
