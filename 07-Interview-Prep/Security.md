---
tags: [interview, prep, security, devsecops, questions]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-07-26
---

# Security Interview Questions

A comprehensive collection of 26 common interview questions regarding Cloud Security and DevSecOps.

---

## Basics

### Q1: What is the Principle of Least Privilege? Give an example.
**A:** The Principle of Least Privilege states that a user or system should only be given the bare minimum access permissions necessary to perform its required function, and nothing more. By strictly limiting permissions, you significantly reduce the blast radius if an identity is compromised. **Example:** If a Web Application only needs to read data from a specific Azure Storage Account, I would assign its Managed Identity the "Storage Blob Data Reader" role scoped *only* to that specific Storage Account, rather than granting it "Contributor" access to the entire Resource Group.

### Q2: What is the difference between Encryption at Rest and Encryption in Transit?
**A:** Encryption in Transit protects data as it moves across the network, ensuring that man-in-the-middle attacks cannot read intercepted traffic. This is typically achieved using TLS/SSL for protocols like HTTPS. Encryption at Rest protects data while it is stored on a physical disk, such as inside an Azure Storage Account or an Azure SQL database. This ensures that if someone physically stole the hard drive from the datacenter, the data would remain unreadable without the decryption key.

### Q3: What is multifactor authentication (MFA) and why is it important?
**A:** Multifactor authentication (MFA) is a security mechanism that requires users to provide two or more verification factors to gain access to a resource. It typically combines something you know (a password), something you have (a smartphone app or hardware token), and something you are (biometrics). MFA is critical because passwords alone are easily compromised via phishing or credential stuffing, and adding a second factor blocks the vast majority of automated account takeover attacks.

### Q4: What are Network Security Groups (NSGs) in Azure?
**A:** Network Security Groups (NSGs) act as virtual firewalls in Azure that filter network traffic to and from Azure resources. They contain a list of security rules that allow or deny inbound or outbound network traffic based on source and destination IP address, port, and protocol. By applying NSGs at the subnet or network interface level, administrators can easily enforce basic network isolation and access controls.

### Q5: What is Role-Based Access Control (RBAC)?
**A:** Role-Based Access Control (RBAC) is a method of restricting access based on the roles of individual users. Instead of assigning permissions to individuals directly, permissions are assigned to roles, and users are added to those roles. In Azure, RBAC is built into every resource — you assign roles like "Reader", "Contributor", or "Key Vault Secrets User" scoped to a specific subscription, resource group, or resource.
```cli
# Assign a role in Azure
az role assignment create --assignee user@domain.com --role "Reader" --scope /subscriptions/00000000-0000-0000-0000-000000000000
```

### Q6: What is a DDoS attack and how do you mitigate it in Azure?
**A:** A Distributed Denial of Service (DDoS) attack floods a target server or network with traffic to make it unavailable. In Azure, you mitigate it using **Azure DDoS Protection Standard** which automatically detects and drops malicious traffic at the network edge. Deploying an **Azure Application Gateway with WAF** and **Azure Front Door** further absorbs and filters traffic spikes before they reach your backend.

### Q7: What is a Web Application Firewall (WAF)?
**A:** A Web Application Firewall (WAF) is a security solution designed to protect web applications by filtering and monitoring HTTP traffic between a web application and the Internet. It specifically guards against common web exploits and vulnerabilities, such as those listed in the OWASP Top 10 (e.g., SQL injection, cross-site scripting). In Azure, a WAF is typically deployed as a component of Azure Front Door or Application Gateway.

### Q8: Explain the difference between Authentication and Authorization.
**A:** Authentication is the process of verifying who a user or system is, usually via credentials like passwords, biometrics, or security tokens. Authorization happens after authentication and determines what resources the authenticated user is allowed to access and what actions they can perform. In simple terms, authentication answers "Are you who you say you are?" while authorization answers "What are you allowed to do?".

---

## Intermediate

### Q9: How do you secure credentials and secrets in a CI/CD pipeline?
**A:** First, I ensure that no secrets are ever hardcoded in the source code or pipeline definitions. Instead, I integrate a secrets management tool like Azure Key Vault or HashiCorp Vault. During pipeline execution, I use Workload Identity Federation to authenticate the runner without utilizing long-lived client secrets. The pipeline then dynamically fetches the necessary secrets, injects them as masked environment variables into memory, and immediately discards them when the job completes.

### Q10: What is Microsoft Defender for Cloud and how does it help?
**A:** Microsoft Defender for Cloud is a unified Cloud Security Posture Management (CSPM) and Cloud Workload Protection Platform (CWPP) solution. It continuously assesses your infrastructure to provide a Secure Score, highlighting misconfigurations like VMs with public IPs or missing encryption. Furthermore, it offers Active Threat Protection by analyzing network traffic and logs to detect anomalous activities, such as brute-force attacks or malware deployments.

### Q11: How do you prevent lateral movement by an attacker inside an Azure VNet?
**A:** To prevent lateral movement, I implement network micro-segmentation using Network Security Groups (NSGs). Instead of a flat VNet, I separate application tiers (e.g., Web, App, DB) into distinct subnets and apply strict NSG rules to govern traffic between them. For instance, the database subnet would only accept traffic on port 1433 originating strictly from the App subnet's IP range, dropping all other unexpected internal traffic.

### Q12: Explain the difference between NSG and Azure Firewall and when to use each.
**A:** NSGs operate at Layer 4 (IP, Port, Protocol) and are used for basic subnet or NIC-level traffic filtering, making them ideal for east-west traffic control within a VNet. Azure Firewall operates at Layers 4 through 7, offering advanced features like FQDN-based rules, TLS inspection, and threat intelligence integration. I use NSGs for free, zero-cost micro-segmentation, and deploy Azure Firewall in a hub VNet to centrally inspect and govern north-south outbound internet traffic.

### Q13: What is Just-in-Time (JIT) VM Access and how do you implement it?
**A:** Just-in-Time (JIT) VM Access is a feature that eliminates standing network access to management ports like SSH (22) and RDP (3389) to prevent brute-force attacks. It works by keeping a "Deny-all" NSG rule active by default on these ports. When an administrator needs access, they request it via the portal or CLI, and the system temporarily opens the port for their specific IP address for a limited duration (e.g., 2 hours).
```bash
az security jit-policy initiate --resource-group myRG --vm-name myVM --ports '[{"number":22,"protocol":"TCP","allowedSourceAddressPrefix":"203.0.113.50","maxDuration":"PT2H"}]'
```

### Q14: What is DevSecOps and how do you integrate security into the CI/CD pipeline?
**A:** DevSecOps is the philosophy of integrating security practices early and continually throughout the software development lifecycle, rather than treating it as a final hurdle. I integrate it into CI/CD pipelines by embedding automated security gates at every stage. This includes running Static Application Security Testing (SAST) on source code, Software Composition Analysis (SCA) for vulnerable dependencies, and Dynamic Application Security Testing (DAST) on deployed staging environments.

### Q15: What is infrastructure as code (IaC) security scanning?
**A:** IaC security scanning involves analyzing code used to provision infrastructure (like Terraform, Bicep, or ARM templates) to identify misconfigurations before deployment. Tools like Checkov, tfsec, or Microsoft Defender for DevOps scan the templates against security best practices and compliance frameworks. This ensures issues like open security groups, unencrypted storage, or missing logging are caught in the PR phase rather than after they are deployed to the cloud.

### Q16: Explain zero-trust architecture.
**A:** Zero-trust architecture operates on the principle of "never trust, always verify," assuming that threats exist both outside and inside the corporate network. It requires strict identity verification, device health checks, and continuous authorization for every user and device trying to access resources, regardless of their network location. Zero-trust relies heavily on strong identity management, micro-segmentation, and rich telemetry to dynamically grant or revoke access based on risk.

---

## Advanced

### Q17: What is Microsoft Sentinel and how does it work?
**A:** Microsoft Sentinel is a cloud-native Security Information and Event Management (SIEM) and Security Orchestration, Automation, and Response (SOAR) solution built on Azure Log Analytics. It works by ingesting vast amounts of security telemetry across your entire enterprise via data connectors. It then applies built-in AI and custom KQL analytics rules to detect complex threats, creating incidents that security teams can investigate or automatically remediate using Logic App playbooks.
```kql
// Detect multiple failed logins from same IP
SigninLogs
| where ResultType != 0
| summarize FailureCount = count() by IPAddress
| where FailureCount > 10
```

### Q18: What are the network security layers in a well-architected AKS cluster?
**A:** A production-grade AKS cluster uses multiple concentric security layers starting from the edge with a WAF (Front Door or App Gateway) to block layer 7 attacks. At the network level, it uses a private API server to prevent public exposure, while outbound traffic is routed through Azure Firewall for egress filtering. Internally, it implements Kubernetes Network Policies to restrict pod-to-pod east-west traffic, often supplemented by a service mesh like Istio for mTLS and granular pod identity.

### Q19: Explain Workload Identity Federation (OIDC) and why it replaces client secrets.
**A:** Client secrets are long-lived credentials that suffer from sprawl, leakage risks, and operational overhead during rotation. Workload Identity Federation solves this by using OpenID Connect (OIDC) to establish a trust relationship between an external identity provider (like GitHub) and Azure Entra ID. The workload requests a short-lived OIDC token from its provider, which Entra ID validates to instantly issue a temporary Azure access token, completely eliminating the need to store or rotate static secrets.

### Q20: How do you secure container images before deploying them to production?
**A:** I secure container images by incorporating vulnerability scanning directly into the CI/CD pipeline using tools like Trivy or Defender for Containers. I enforce policies that fail the build if high or critical CVEs are found in the base image or dependencies. Additionally, I use minimal base images (like distroless) to reduce the attack surface, and sign the images using tools like Cosign to ensure only trusted, unaltered images are admitted to the cluster by OPA Gatekeeper.

### Q21: What is mutual TLS (mTLS) and why is it used in a service mesh?
**A:** Mutual TLS (mTLS) is an extension of standard TLS where both the client and the server cryptographically authenticate each other's certificates during the handshake. In a microservices architecture, a service mesh uses mTLS to encrypt all service-to-service communication transparently. This ensures data confidentiality in transit and guarantees that a service is definitively communicating with its intended counterpart, effectively thwarting spoofing and internal man-in-the-middle attacks.

### Q22: Explain the concept of confidential computing in the cloud.
**A:** Confidential computing protects data in use by isolating computations in a hardware-based Trusted Execution Environment (TEE) or secure enclave. While traditional encryption secures data at rest and in transit, confidential computing ensures data remains encrypted even while being processed in memory. This provides strong guarantees against insider threats, hypervisor compromises, or even cloud provider operators, making it ideal for highly sensitive workloads like financial modeling or healthcare data processing.

---

## Scenario-Based

### Q23: An attacker compromised a web server. How do you respond and prevent them from reaching the database?
**A:** My immediate response is to isolate the compromised web server by modifying its NSG to block all inbound and outbound traffic, and capturing a forensic snapshot of its disk. To prevent database access, I ensure micro-segmentation is in place so the DB subnet only accepts connections from authorized app tiers, not the web tier directly. Finally, I would rotate any credentials or managed identity tokens the web server had access to, and investigate SIEM logs to identify the intrusion vector.

### Q24: Your team accidentally pushed a hardcoded cloud credential to a public GitHub repository. What steps do you take immediately?
**A:** First, I treat the credential as actively compromised and immediately revoke it in the cloud provider's IAM portal. Second, I rotate the secret and update the application or pipeline to use a secure secrets manager instead. Third, I rewrite the Git repository history using a tool like BFG Repo-Cleaner to remove the secret from all commits, and I implement pre-commit hooks (like detect-secrets) to prevent future hardcoded credentials from being pushed.

### Q25: A developer needs temporary administrative access to production for debugging. How do you grant this securely?
**A:** I would never provide permanent standing admin access. Instead, I use Privileged Identity Management (PIM) to allow the developer to temporarily elevate their role for a strictly time-bound window (e.g., 2 hours). This request can be configured to require managerial approval and mandatory MFA verification upon activation. All actions performed during this elevated session are thoroughly audited and logged to ensure full accountability.

### Q26: You are designing a public-facing e-commerce application. How do you architect its network security to withstand OWASP Top 10 attacks and DDoS?
**A:** I would deploy the application behind Azure Front Door with a tightly configured Web Application Firewall (WAF) to inspect incoming HTTP/S traffic for OWASP vulnerabilities like SQLi and XSS. I would enable Azure DDoS Protection Standard on the VNet to absorb volumetric attacks. Behind the scenes, the backend APIs and databases would be placed in isolated subnets with no public IP addresses, accessible only via Private Endpoints, ensuring all traffic originates solely through the validated Front Door path.

---

## Related Notes
- [[Azure]] — Azure platform, RBAC, Managed Identity
- [[CI-CD]] — Securing CI/CD pipelines
- [[Networking]] — NSG, Azure Firewall, private endpoints
