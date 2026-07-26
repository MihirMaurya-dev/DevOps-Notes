---
updated: 2026-07-26
tags: [azure, landing-zone, interview-questions, devops, cloud, networking, security]
source: generated
---

# Azure Landing Zone Interview Questions

## Basics

### 1. What is an Azure Landing Zone?
An Azure Landing Zone is an environment for hosting workloads, pre-provisioned through code. It provides foundational capabilities like networking, identity and access management, security, and governance out of the box. The goal is to enable application migration and greenfield development at enterprise scale without worrying about the underlying plumbing.

### 2. What is the Cloud Adoption Framework (CAF) in Azure?
The Microsoft Cloud Adoption Framework (CAF) for Azure is a collection of documentation, implementation guidance, best practices, and tools designed to help organizations align their business and technical strategies. It guides companies through the lifecycle of cloud adoption, including strategy, planning, readiness, adoption, and governance. Landing Zones are a core technical implementation of the "Ready" phase in CAF.

### 3. What are the key design areas of an Azure Landing Zone?
There are eight key design areas in an Azure Landing Zone architecture. These include billing and Active Directory tenant, identity and access management, network topology and connectivity, resource organization, governance and compliance, baseline disciplines, business continuity and disaster recovery (BCDR), and deployment options. These design areas ensure that the environment is secure, scalable, and manageable.

### 4. What is the purpose of Management Groups in Azure?
Management Groups provide a level of scope above subscriptions, allowing you to organize subscriptions into a hierarchy for unified policy and access management. For example, you can apply an Azure Policy or Role-Based Access Control (RBAC) role at a Management Group level, and it will inherit down to all associated subscriptions. This hierarchical structure is essential for applying consistent governance across a large landing zone environment.

### 5. How does a Hub and Spoke network topology work in a Landing Zone?
In a Hub and Spoke topology, a central "hub" Virtual Network (VNet) acts as a central point of connectivity to on-premises networks and the internet. The "spoke" VNets peer with the hub and can be used to isolate workloads. This design allows for centralized services like firewalls, VPN gateways, and DNS in the hub, reducing costs and administrative overhead while keeping spoke workloads secure and segmented.

### 6. What is the difference between an Enterprise-Scale Landing Zone and a start-small approach?
The Enterprise-Scale architecture is designed for large organizations that need complex governance, security, and networking from day one. It heavily utilizes Management Groups, centralized policies, and Hub-Spoke or Virtual WAN networking. The start-small approach is simpler, often starting within a single subscription and expanding organically as the organization grows and its cloud maturity increases.

### 7. What role does Azure Policy play in a Landing Zone?
Azure Policy is a service used to create, assign, and manage policies that enforce different rules and effects over your resources. In a Landing Zone, policies ensure that resources stay compliant with corporate standards and service level agreements, often automatically deploying diagnostic settings or denying non-compliant resources (like unencrypted storage). It acts as the primary governance engine for the environment.
```az cli
az policy assignment create --name "Allowed Locations" --policy "e56962a6-4747-49cd-b67b-bf8b01975c4c" --params "{'listOfAllowedLocations': {'value': ['westeurope', 'northeurope']}}"
```

### 8. How are Subscriptions used as a unit of management in Azure?
Subscriptions act as the primary unit of billing, security boundary, and scale in Azure. In a modern Landing Zone architecture, organizations use multiple subscriptions to separate environments (e.g., dev, test, prod) or workloads (e.g., HR app, Finance app) to prevent hitting resource limits and to isolate blast radiuses. This strategy is known as subscription democratization or subscription vending.

## Intermediate

### 9. How do you implement network segmentation in an Azure Landing Zone?
Network segmentation is typically achieved using a combination of Virtual Networks, Subnets, and Network Security Groups (NSGs). In a Landing Zone, you segment at a macro level using separate spoke VNets for different workloads or environments. At a micro level, you use subnets within those VNets and apply strict NSG rules and Application Security Groups (ASGs) to control east-west and north-south traffic.

### 10. Can you explain the difference between Azure RBAC and Azure AD roles?
Azure AD roles are used to manage Azure AD resources, such as creating users, assigning licenses, or managing enterprise applications. Azure RBAC (Role-Based Access Control) is used to manage access to Azure resources like virtual machines, storage accounts, and virtual networks. In a Landing Zone, Azure RBAC is heavily utilized to grant developers access to their specific resource groups or subscriptions without giving them administrative rights to the tenant.

### 11. How do you enforce compliance across all subscriptions using Azure Policy?
You enforce compliance by assigning Azure Policies or Policy Initiatives at the Management Group level. By structuring your Management Groups correctly (e.g., separating "Online" workloads from "Corp" workloads), you can tailor policies to specific environments. Using effects like `Deny` prevents non-compliant deployments, while `DeployIfNotExists` can automatically remediate issues, such as setting up Microsoft Defender for Cloud on new subscriptions.

### 12. What is the purpose of the Connectivity subscription in a Landing Zone architecture?
The Connectivity subscription is a dedicated, centralized subscription used to host core networking resources. This typically includes the Hub Virtual Network, VPN Gateways, ExpressRoute circuits, Azure Firewall, and central Private DNS zones. Isolating these resources into their own subscription ensures that only the networking team has access to modify critical routing and perimeter security configurations.

### 13. How would you design DNS resolution between on-premises and Azure in a Hub-Spoke topology?
To enable hybrid DNS resolution, you typically deploy Azure DNS Private Resolver or custom DNS forwarder VMs in the Hub VNet. On-premises DNS servers are configured with a conditional forwarder pointing to the inbound endpoint of the Azure DNS resolver. Conversely, the Azure DNS resolver has an outbound endpoint and rules to forward queries for on-premises domains back to the on-premises DNS servers, ensuring seamless name resolution across both environments.

### 14. What are the benefits of using Infrastructure as Code (IaC) like Bicep or Terraform for deploying a Landing Zone?
IaC allows you to define your Landing Zone infrastructure in declarative code, ensuring consistent, repeatable, and automated deployments. It eliminates configuration drift and allows infrastructure changes to be version-controlled, peer-reviewed, and tested via CI/CD pipelines. This approach is critical for scaling Landing Zones, as it enables safe and rapid provisioning of new subscriptions, policies, and networking components.

### 15. How do you handle centralized logging and auditing across multiple subscriptions?
Centralized logging is handled by deploying a central Azure Log Analytics Workspace, often in a dedicated Management subscription. You then use Azure Policy (with `DeployIfNotExists` effect) to automatically configure Diagnostic Settings on all supported resources across all subscriptions to send their logs to this central workspace. This provides a single pane of glass for security auditing, monitoring, and alerting via Azure Monitor and Microsoft Sentinel.

### 16. Explain the concept of subscription vending in Azure.
Subscription vending is the automated process of creating and configuring new Azure subscriptions for workload teams. Instead of a manual ticketing process, developers can request a subscription via a portal or pipeline, and IaC provisions a new subscription, links it to the correct Management Group, sets up VNet peering, configures RBAC, and applies baseline policies. This accelerates development while ensuring governance is baked in from the start.

## Advanced

### 17. How do you design for high availability and disaster recovery in a multi-region Landing Zone?
Multi-region Landing Zones require deploying multiple Hubs across paired Azure regions (e.g., East US and West US). Traffic is load-balanced globally using Azure Front Door or Traffic Manager. Networking between regions can be handled via Azure Virtual WAN or Global VNet Peering. Disaster recovery is managed by replicating critical state using services like Azure Site Recovery, geo-redundant storage, and Cosmos DB global distribution, combined with automated failover processes.

### 18. What are the security considerations for cross-tenant Landing Zone architectures?
Cross-tenant scenarios often occur after acquisitions or in managed service provider models. Security considerations include managing identity via Azure AD B2B collaboration, securing network traffic using private links or VPNs, and establishing trust boundaries. You must carefully manage RBAC using Azure Lighthouse to provide delegated access, ensuring that admins from the managing tenant only have least-privilege access to the target tenant's resources.

### 19. How do you implement Zero Trust principles within an Azure Landing Zone?
Zero Trust in a Landing Zone involves "never trust, always verify" across identity, devices, networks, and data. This is implemented by enforcing Multi-Factor Authentication (MFA) and Conditional Access policies via Azure AD. On the network side, it involves strict micro-segmentation, forcing traffic through Layer 7 firewalls, and using Azure Private Link to ensure PaaS services are not exposed to the public internet. Furthermore, encryption is enforced both in transit and at rest.

### 20. Explain the integration of Azure Firewall and Azure Virtual WAN in a large-scale enterprise Landing Zone.
Azure Virtual WAN (vWAN) provides a unified routing architecture, simplifying connectivity between branches, remote users, and Azure VNets. When integrated with Azure Firewall within the vWAN Hub (known as a Secured Virtual Hub), it allows centralized inspection and filtering of all traffic (east-west and north-south). This simplifies routing complexity, as the vWAN hub automatically propagates routes to all connected spokes and on-premises gateways.

### 21. How do you manage policy exceptions and exemptions at scale without compromising security?
Policy exemptions should be tracked, time-bound, and strictly controlled via an approval process. In Azure, you can create Policy Exemptions at the resource or resource group level for specific policies. Best practice is to manage these exemptions as code, deploying them via pipelines so they are version-controlled and peer-reviewed. Additionally, continuous monitoring should alert security teams of active exemptions to ensure they are remediated before expiry.

### 22. How do you design identity and access management for hybrid environments using Azure AD Connect?
In a hybrid setup, Azure AD Connect synchronizes identities from on-premises Active Directory to Azure AD. Design considerations include choosing the right authentication method (Password Hash Sync, Pass-through Authentication, or ADFS) based on security and compliance requirements. You must also design High Availability for the sync engine (staging mode) and configure Seamless SSO to provide a frictionless login experience for domain-joined corporate devices.

### 23. Describe the process of migrating existing Azure workloads into a newly built Enterprise-Scale Landing Zone.
Migrating existing workloads involves moving resources from legacy subscriptions into the new Landing Zone hierarchy. This requires careful planning to minimize downtime. The process includes mapping existing resources to the new Management Group structure, assessing compliance impact against new policies, and redesigning networking to connect to the new Hub. Azure Resource Mover can be used to move resources across subscriptions and regions, while testing is critical to ensure RBAC and routing continue to function.

### 24. How do you handle IP address management (IPAM) effectively in a large Azure Hub and Spoke environment?
Effective IPAM prevents address overlapping, which breaks VNet peering and routing. In large environments, organizations use third-party IPAM tools (like Infoblox) or custom solutions integrated into their subscription vending pipelines. When a new spoke VNet is requested, the pipeline dynamically queries the IPAM solution to check out an available CIDR block. This automation ensures contiguous routing spaces and simplifies BGP route propagation to on-premises networks.

## Scenario-Based

### 25. Scenario: A company wants to prevent any developer from creating public IP addresses in their spoke subscriptions. How would you achieve this?
I would implement this using Azure Policy. I would assign the built-in policy "Not allowed resource types" at the Management Group level covering all spoke subscriptions. I would configure the policy parameter to deny the resource type `Microsoft.Network/publicIPAddresses`. This ensures that any ARM template, Bicep file, or portal action attempting to create a Public IP will be explicitly blocked at the management plane level before provisioning occurs.

### 26. Scenario: You have a hub network and three spoke networks. Spoke A needs to communicate with Spoke B, but not Spoke C. How do you configure the routing?
First, ensure that VNet peering between the spokes and the hub has "Allow forwarded traffic" enabled. In the Hub, deploy an Azure Firewall or NVA. In Spoke A and Spoke B, attach Route Tables with a User Defined Route (UDR) pointing `0.0.0.0/0` (or specific address spaces) to the private IP of the Firewall. Finally, configure network rules on the Azure Firewall to explicitly allow traffic from Spoke A's CIDR to Spoke B's CIDR, while denying traffic to Spoke C.

### 27. Scenario: Your organization has acquired another company and needs to integrate their Azure environment. What is your approach using Management Groups and Policies?
I would start by creating a new, separate Management Group hierarchy under our root for the acquired company to avoid breaking their existing workloads with our strict policies. I would gradually audit their environment using our policies in "AuditOnly" mode to identify gaps. Over time, we would remediate their resources, align their RBAC models, and eventually merge their subscriptions into our standard "Corp" or "Online" Management Groups to achieve unified governance.

### 28. Scenario: An audit reveals that several storage accounts lack encryption with Customer-Managed Keys (CMK). How do you enforce this going forward and remediate existing ones?
I would deploy an Azure Policy with a `Deny` effect to block the creation of new storage accounts that do not use CMK. For remediation, I would create a separate policy with a `DeployIfNotExists` or `Modify` effect and a remediation task to update the existing storage accounts. Alternatively, if complex logic is required, I could write a script (PowerShell/CLI) to iterate through the non-compliant resources identified by Policy and apply the CMK configuration programmatically.

### 29. Scenario: You are tasked with providing isolated sandbox environments for developers that automatically get deleted after 30 days. How do you design this?
I would create a "Sandbox" Management Group with loose policies (to encourage experimentation) but strict spending limits (using Azure Cost Management budgets). Using a subscription vending pipeline, developers can request a sandbox subscription. I would tag the subscription with a `CreationDate` or `ExpiryDate`. An automated runbook or Azure Function would run daily, query the tags, and automatically delete resource groups or cancel the subscription if the 30-day limit is reached.

### 30. Scenario: A legacy application moved to Azure requires a static IP and cannot support modern authentication. How do you secure it within the Landing Zone?
For networking, I would place the application in a dedicated subnet and assign an internal static IP. I would route all inbound and outbound traffic through the Azure Firewall in the Hub using UDRs for deep packet inspection. Since it lacks modern auth, I would place it behind Azure Application Gateway or Entra ID Application Proxy to offload authentication, requiring users to authenticate with Azure AD (MFA) before their traffic ever reaches the legacy application backend.

### 31. Scenario: You need to ensure that all resources are deployed only in the West Europe and North Europe regions. How do you implement this restriction?
This is a classic governance requirement solved by Azure Policy. I would assign the built-in policy named "Allowed locations" at the highest applicable Management Group level. During assignment, I would pass an array containing `westeurope` and `northeurope` to the `listOfAllowedLocations` parameter. This will explicitly deny any resource deployment outside of these two regions, ensuring data sovereignty and compliance.

### 32. Scenario: Your central IT team manages the hub, but workload teams need full control over their spoke virtual networks. How do you assign permissions effectively?
This requires a delegated administration model using Azure RBAC. The central IT team receives `Network Contributor` access on the Hub subscription/resource group. For the workload teams, I would assign them `Contributor` rights specifically scoped to their spoke resource groups or subscriptions. To allow peering, I would grant the central IT team a custom role with `Microsoft.Network/virtualNetworks/peer/action` on the spoke VNets, and grant the spoke teams the same permission on the hub VNet, enabling peering without granting full administrative access to the networks.
