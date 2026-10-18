---
tags: [interview, azure, rbac, security, architecture]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Azure Core: High-Quality Interview Questions

These questions test your understanding of Azure basics, Networking, Compute, Containers, Security, and Monitoring. Structured from Basics to Scenario-Based.

## 🟢 Part 1: Basics

### 1. What is Microsoft Azure?
Azure is Microsoft's public cloud computing platform. It provides computing, analytics, storage, and networking services. Users can pick and choose these services to develop and scale new applications or run existing applications.
```bash
az account show
```

### 2. What is an Azure Region?
A region is a geographical area on the planet containing at least one, but potentially multiple, datacenters. These datacenters are networked together with a low-latency network. You deploy resources into specific regions based on compliance and user proximity.
```bash
az account list-locations -o table
```

### 3. What is an Availability Zone (AZ)?
Availability Zones are unique physical locations within an Azure region. Each zone is made up of one or more datacenters equipped with independent power, cooling, and networking. This provides high availability and fault tolerance.

### 4. What is a Resource Group?
A Resource Group is a logical container that holds related resources for an Azure solution. You can manage, deploy, and delete resources as a group. It is heavily used for organizing resources and applying RBAC.
```bash
az group create --name myRG --location eastus
```

### 5. Can a resource group contain resources from different regions?
Yes, a resource group can contain resources located in different regions. The location of the resource group itself only determines where the metadata about the resources is stored.

### 6. What is an Azure Virtual Network (VNet)?
A VNet is the fundamental building block for your private network in Azure. It enables many types of Azure resources to securely communicate with each other, the internet, and on-premises networks.
```bash
az network vnet create --name myVNet --resource-group myRG --address-prefixes 10.0.0.0/16
```

### 7. What is a Subnet?
A subnet is a range of IP addresses within a VNet. You can divide a VNet into multiple subnets for organization and security. Resources are deployed into subnets, not directly into VNets.
```bash
az network vnet subnet create --name mySubnet --vnet-name myVNet --resource-group myRG --address-prefixes 10.0.1.0/24
```

### 8. What is a Network Security Group (NSG)?
An NSG is a virtual firewall that filters inbound and outbound network traffic to and from Azure resources in an Azure VNet. It contains security rules that allow or deny traffic based on source/destination IP, port, and protocol.
```bash
az network nsg create --resource-group myRG --name myNSG
```

### 9. What is an Azure Virtual Machine (VM)?
An Azure VM provides on-demand, scalable computing resources. It falls under Infrastructure as a Service (IaaS), giving you full control over the operating system and installed software.
```bash
az vm create --resource-group myRG --name myVM --image Ubuntu2204 --admin-username azureuser --generate-ssh-keys
```

### 10. What is an Availability Set?
An Availability Set is a logical grouping capability for isolating VM resources from each other when they are deployed. Azure ensures that the VMs placed within an Availability Set run across multiple physical servers, compute racks, storage units, and network switches.

### 11. What is Azure Kubernetes Service (AKS)?
AKS is a managed Kubernetes service that simplifies deploying a managed Kubernetes cluster in Azure. Azure handles the control plane, while you only manage and pay for the agent nodes.
```bash
az aks create --resource-group myRG --name myAKSCluster --node-count 1 --enable-addons monitoring --generate-ssh-keys
```

### 12. What is Azure Key Vault?
Azure Key Vault is a cloud service for securely storing and accessing secrets. A secret is anything that you want to tightly control access to, such as API keys, passwords, certificates, or cryptographic keys.
```bash
az keyvault create --name myKeyVault --resource-group myRG --location eastus
```

### 13. What is RBAC in Azure?
Role-Based Access Control (RBAC) is an authorization system built on Azure Resource Manager. It provides fine-grained access management of Azure resources. You assign roles to users, groups, or service principals at different scopes.
```bash
az role assignment create --assignee user@domain.com --role Contributor --scope /subscriptions/00000000-0000-0000-0000-000000000000
```

### 14. What is a Managed Identity?
A Managed Identity is a feature in Microsoft Entra ID that provides Azure services with an automatically managed identity. You can use this identity to authenticate to services that support Azure AD authentication, such as Key Vault, without needing credentials in your code.

### 15. What is a Private Endpoint?
A Private Endpoint is a network interface that uses a private IP address from your virtual network. This network interface connects you privately and securely to a service powered by Azure Private Link, bringing the service into your VNet.

### 16. What is Azure Resource Manager (ARM)?
ARM is the deployment and management service for Azure. It provides a management layer that enables you to create, update, and delete resources in your Azure account.

### 17. What is an ARM Template?
An ARM template is a JavaScript Object Notation (JSON) file that defines the infrastructure and configuration for your project. The template uses declarative syntax to define the resources you want to deploy.

## 🟡 Part 2: Advanced

### 18. What is the difference between Azure Load Balancer and Application Gateway?
Azure Load Balancer operates at Layer 4 (TCP/UDP) and is used for network-level load balancing. Application Gateway operates at Layer 7 (HTTP/HTTPS) and provides features like URL routing, cookie-based session affinity, and Web Application Firewall (WAF).

### 19. How does VNet Peering work?
VNet peering connects two Azure virtual networks. Once peered, the networks appear as one for connectivity purposes. The traffic between VMs in peered networks uses the Microsoft backbone infrastructure and never traverses the public internet.
```bash
az network vnet peering create --name myVNet1ToVNet2 --resource-group myRG --vnet-name VNet1 --remote-vnet VNet2 --allow-vnet-access
```

### 20. What is an Application Security Group (ASG)?
ASGs enable you to configure network security as a natural extension of an application's structure. You can group VMs and define network security policies based on those groups, rather than maintaining explicit IP addresses in NSG rules.

### 21. How does Azure Monitor differ from Log Analytics?
Azure Monitor is the overarching service that collects, analyzes, and acts on telemetry data from your cloud and on-premises environments. Log Analytics is a specific tool within Azure Monitor used to write queries (using KQL) and analyze the collected log data.
```kusto
// KQL Example to find failed Azure AD logins
SigninLogs | where ResultType != 0
```

### 22. What is Microsoft Entra ID (formerly Azure AD)?
Microsoft Entra ID is a cloud-based identity and access management service. It helps your employees access external resources (like Microsoft 365 or SaaS apps) and internal resources (like apps on your corporate network or in Azure).

### 23. What is the difference between System-Assigned and User-Assigned Managed Identity?
A System-Assigned identity is tied to the lifecycle of a specific Azure resource; if the resource is deleted, the identity is deleted. A User-Assigned identity is created as a standalone Azure resource and can be shared across multiple resources, possessing an independent lifecycle.

### 24. How do you scale an AKS cluster?
You can scale an AKS cluster manually or use the Cluster Autoscaler to automatically adjust the number of agent nodes based on resource demands. For pod-level scaling, you use the Horizontal Pod Autoscaler (HPA) within Kubernetes.
```bash
az aks scale --resource-group myRG --name myAKSCluster --node-count 3
```

### 25. What is Azure Policy?
Azure Policy is a service used to create, assign, and manage policies that enforce rules over your resources. This ensures your resources stay compliant with your corporate standards and SLAs.
```bash
az policy assignment create --name "Allowed Locations" --policy "e56962a6-4747-49cd-b67b-bf8b01975c4c" --params "{'listOfAllowedLocations': {'value': ['eastus', 'westus']}}"
```

### 26. How do you secure Key Vault access?
You secure Key Vault using either Azure RBAC or Key Vault Access Policies. The modern best practice is to use Azure RBAC, which provides centralized management of access control. You also secure network access using firewalls or Private Endpoints.

### 27. Explain the difference between Service Endpoint and Private Endpoint.
A Service Endpoint provides a direct, secure connection to Azure PaaS services over the Azure backbone, but the PaaS service still uses a public IP address. A Private Endpoint gives the PaaS service a private IP from your VNet, completely removing the public IP from the equation.

### 28. What is the difference between VM Scale Sets (VMSS) and Availability Sets?
Availability Sets protect your applications from hardware failures by distributing VMs across fault domains. VM Scale Sets provide identical VMs that can automatically increase or decrease in number based on demand or a defined schedule.

### 29. How do NSG rules get evaluated?
NSG rules are evaluated by priority using a number between 100 and 4096. Lower numbers have higher priority and are processed first. Once a match is found, no further rules are evaluated.

### 30. What is a Route Table in Azure?
A Route Table contains a set of rules (routes) that determine where network traffic from your subnet is directed. You use it to override Azure's default routing, for instance, forcing traffic through a network virtual appliance.
```bash
az network route-table create --resource-group myRG --name myRouteTable
```

### 31. What is Azure Bastion?
Azure Bastion is a fully managed PaaS service that provides secure and seamless RDP/SSH connectivity to your VMs directly from the Azure portal over TLS. It eliminates the need to expose public IP addresses on your VMs.

### 32. Explain RBAC Scope inheritance.
RBAC applies hierarchically. Access granted at a higher scope (like a Management Group or Subscription) is inherited by all child scopes (Resource Groups and Resources). The best practice is to assign roles at the lowest possible scope to follow the principle of least privilege.

### 33. What is Bicep?
Bicep is a Domain-Specific Language (DSL) that uses declarative syntax to deploy Azure resources. It provides concise syntax and reliable type safety, acting as a transparent abstraction over ARM templates.
```bicep
resource storageAccount 'Microsoft.Storage/storageAccounts@2021-02-01' = {
  name: 'mystorageaccount'
  location: 'eastus'
  sku: {
    name: 'Standard_LRS'
  }
  kind: 'StorageV2'
}
```

### 34. What is the Azure CLI?
The Azure Command-Line Interface is a set of cross-platform commands for managing Azure resources. You can run it on Windows, macOS, and Linux to automate tasks via scripts.

## 🔴 Part 3: Scenario-Based

### 35. Your VM cannot reach the internet. What do you check?
First, check the NSG rules applied to the VM's Network Interface and Subnet to ensure outbound port 80/443 is allowed. Next, check if a custom Route Table is forcing traffic to a firewall that might be dropping it. Finally, ensure the VM has a Public IP or is behind a NAT Gateway/Load Balancer.

### 36. A developer needs access to restart VMs but not delete them. How do you configure this?
You should create a Custom RBAC Role in Azure. You will specify the exact action `Microsoft.Compute/virtualMachines/restart/action` in the `Actions` array and leave the delete action out. Then, assign this custom role to the developer at the Resource Group scope.
```bash
az role definition create --role-definition my-custom-role.json
```

### 37. Your Web App needs to access an Azure SQL Database securely without storing passwords. How?
Enable a System-Assigned Managed Identity on the Azure Web App. In the Azure SQL Database, create a database user mapped to the Managed Identity and grant it the necessary SQL roles (e.g., `db_datareader`). The app can now authenticate securely using Entra ID tokens.

### 38. Your VNet-A is peered to VNet-B, and VNet-B is peered to VNet-C. Can resources in VNet-A communicate with VNet-C?
No. VNet Peering in Azure is non-transitive. To enable communication from VNet-A to VNet-C, you must either create a direct peer between A and C, or configure VNet-B to act as a transit network with a firewall or network virtual appliance (NVA) and UDRs.

### 39. How do you securely access an Azure Storage Account from a VNet without going over the public internet?
Create a Private Endpoint for the Storage Account inside the VNet. This assigns a private IP address to the storage account. You must also configure Private DNS Zones so that your VMs can resolve the storage account's URL to its new private IP instead of its public IP.

### 40. Your AKS pods cannot resolve external DNS names. What could be the issue?
This is typically an issue with CoreDNS pods inside the cluster or the VNet's custom DNS settings. Check if the CoreDNS pods are running (`kubectl get pods -n kube-system -l k8s-app=kube-dns`). Also, verify if the VNet has custom DNS servers set that cannot reach the internet, or if an NSG is blocking outbound port 53.

### 41. You need to route HTTP traffic to different backend pools based on the URL path. Which load balancer do you choose?
You should use Azure Application Gateway. It operates at Layer 7 and supports URL Path-Based Routing. For example, you can route `/images/*` to a pool of VMs optimized for image processing, and `/video/*` to a pool optimized for video streaming.

### 42. You want to ensure no one can accidentally delete a critical Resource Group. What do you use?
Apply a Resource Lock of type "CannotDelete" on the Resource Group. This prevents anyone, even the Subscription Owner, from deleting the resource group or its contents until the lock is explicitly removed.
```bash
az lock create --name PreventDelete --lock-type CanNotDelete --resource-group myCriticalRG
```

### 43. An engineer accidentally gave Contributor rights to everyone on the subscription. How do you prevent this in the future?
Implement Microsoft Entra Privileged Identity Management (PIM). Instead of giving standing access, users must request "Just-In-Time" access to the Contributor role. You can mandate approval workflows, MFA requirements, and maximum access duration limits (e.g., 2 hours).

### 44. You need to migrate on-premise VMware VMs to Azure. Which tool do you use?
Use Azure Migrate. It provides a centralized hub to assess and migrate on-premises servers, infrastructure, applications, and data to Azure. It includes server assessment and migration tools.

### 45. How do you track who deleted a Virtual Machine last week?
You check the Azure Activity Log. It provides insight into subscription-level events, tracking operations on resources (who, what, and when). You can filter the log by the 'Delete Virtual Machine' operation to find the exact user and time.
```bash
az monitor activity-log list --offset 7d
```

### 46. Your web app is experiencing volumetric DDoS attacks. How do you protect it?
Azure automatically provides Basic DDoS protection. However, you should upgrade to Azure DDoS Network Protection for advanced mitigation and dedicated support. Additionally, place an Azure Application Gateway with a Web Application Firewall (WAF) in front of the web app to block malicious Layer 7 traffic.

### 47. You need to connect your on-premise network to Azure securely over the internet. What are the options?
For internet-based connections, use an Azure VPN Gateway (Site-to-Site VPN). If you need a private, dedicated connection that bypasses the public internet entirely, use Azure ExpressRoute.

### 48. You have a database password in Key Vault that expires soon. How do you automate its rotation?
You can use Azure Event Grid to detect the "Secret Near Expiry" event from Key Vault. This event can trigger an Azure Function that connects to the database, generates a new password, updates the database, and saves the new password back into the Key Vault.

### 49. You need a highly available database across multiple Azure regions. What do you use?
Use Azure Cosmos DB for a globally distributed, multi-model NoSQL database. If you require a relational SQL database, use Azure SQL Database with Active Geo-Replication or Auto-failover groups to replicate data to secondary regions.

### 50. Your deployment failed with an error stating you exceeded the core quota. How do you fix this?
Azure enforces default limits (quotas) on resources like VM CPU cores per region to prevent accidental large expenditures. You must go to the "Quotas" blade in the Azure Portal or use the Help + Support section to submit a ticket requesting a quota increase for that specific VM family in your region.
