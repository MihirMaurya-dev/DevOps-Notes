---
tags: [interview, prep, security, devsecops, questions]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Security Interview Questions

A collection of common interview questions regarding Cloud Security and DevSecOps.

---

## Q1: How do you secure credentials and secrets in a CI/CD pipeline?
**A:** First, I would ensure that no secrets are ever hardcoded in the source code. In the pipeline, I would integrate a secrets management tool like **Azure Key Vault**. During the pipeline execution, I would use **Workload Identity Federation (OIDC)** to authenticate the pipeline runner to Azure without using a long-lived Client Secret. The pipeline would then securely fetch the necessary secrets from the Key Vault dynamically, inject them as masked environment variables, and use them for the deployment.

---

## Q2: What is the Principle of Least Privilege? Give an example.
**A:** The Principle of Least Privilege states that a user or system should only be given the bare minimum access permissions necessary to perform its required function, and nothing more.

**Example:** If a Web Application only needs to read data from a specific Azure Storage Account, I would assign its Managed Identity the "Storage Blob Data Reader" role scoped *only* to that specific Storage Account, rather than granting it "Contributor" access to the entire Resource Group.

---

## Q3: What is Microsoft Defender for Cloud and how does it help?
**A:** Microsoft Defender for Cloud is a unified Cloud Security Posture Management (CSPM) and Cloud Workload Protection Platform (CWPP). It helps by:
1. Providing a **Secure Score** that evaluates my infrastructure against security best practices (e.g., flagging VMs that have public IPs or lack encryption).
2. Providing **Active Threat Protection** by analyzing logs and network traffic to detect anomalous activity, such as brute-force attacks on SSH or malicious SQL injection attempts on databases.

---

## Q4: How do you prevent lateral movement by an attacker inside an Azure VNet?
**A:** I would implement network micro-segmentation using **Network Security Groups (NSGs)**. Instead of having one flat VNet where all VMs can talk to each other, I would place different tiers of the application (Web, App, DB) in different subnets. I would apply NSGs to those subnets with strict rules — for example, the DB subnet only allows inbound traffic on port 1433 from the specific IP range of the App subnet, and drops all other traffic.

---

## Q5: What is the difference between Encryption at Rest and Encryption in Transit?
**A:** 
- **Encryption in Transit** protects data as it moves across the network (e.g., from a user's browser to the load balancer). This is achieved using TLS/SSL (HTTPS).
- **Encryption at Rest** protects data while it is stored on a physical disk (e.g., inside an Azure Storage Account or an Azure SQL database). This ensures that if someone physically stole the hard drive from the Microsoft datacenter, the data would be unreadable without the decryption key.

---

## Q6: Explain the difference between NSG and Azure Firewall and when to use each
**A:**

| Feature | NSG | Azure Firewall |
|---|---|---|
| **OSI Layer** | Layer 4 (IP, Port, Protocol) | Layer 4 + Layer 7 (FQDN, URL, TLS inspection) |
| **Deployment scope** | Subnet or NIC level | Centralized hub VNet (hub-spoke topology) |
| **FQDN-based rules** | No | Yes — allow/block by domain name |
| **Threat Intelligence** | No | Yes — Microsoft threat feed integration |
| **Egress filtering** | Basic (IP/port only) | Full FQDN and URL-based egress filtering |
| **Cost** | Free | ~$1.25/hr + ~$0.016/GB processed |
| **Logging** | NSG Flow Logs (via Network Watcher) | Firewall Diagnostic Logs to Log Analytics |

**When to use NSG:**
- Controlling traffic *between* subnets within a VNet (east-west / lateral movement prevention).
- Restricting which ports are open on individual VMs or subnet tiers.
- Quick, zero-cost traffic filtering.

**When to use Azure Firewall:**
- Controlling *all* outbound (north-south) internet traffic from a VNet.
- Enforcing FQDN-based allowlists (e.g., allow only `*.microsoft.com` and `*.ubuntu.com`).
- Centralized logging and policy management across multiple VNets in a hub-spoke topology.

> [!note] Production best practice
> Use **both**: NSGs for subnet-level micro-segmentation and Azure Firewall (in the hub VNet) for centralized egress control and threat intelligence. Route tables (UDR) force all subnet traffic through the firewall.

---

## Q7: What is Microsoft Sentinel and how does it work?
**A:** Microsoft Sentinel is a cloud-native **SIEM (Security Information and Event Management)** and **SOAR (Security Orchestration, Automation, and Response)** solution built on top of Azure Log Analytics.

**How it works:**
1. **Collect**: Ingest security data from across your environment — Azure, Microsoft 365, on-premises, and third-party sources — via Data Connectors.
2. **Detect**: Use built-in and custom **Analytics Rules** (KQL-based queries) to detect suspicious patterns in the ingested logs. Also applies ML-based fusion to correlate low-fidelity signals into high-confidence incidents.
3. **Investigate**: When an alert fires, it creates an **Incident** with an investigation graph showing entities (users, IPs, hosts) and their relationships.
4. **Respond**: **Playbooks** (Azure Logic Apps) can automatically respond to incidents — e.g., blocking an IP in an NSG or disabling a compromised Entra ID account.

```kql
// Example KQL analytics rule: Detect multiple failed logins from same IP
SigninLogs
| where ResultType != 0                          // Failed sign-ins
| summarize FailureCount = count() by IPAddress, bin(TimeGenerated, 5m)
| where FailureCount > 10
| project TimeGenerated, IPAddress, FailureCount
```

> [!tip]
> Sentinel's key advantage over traditional SIEM tools is **no infrastructure to manage** and pricing is based on data ingested (GB/day), making it cost-effective for cloud-native organizations.

---

## Q8: How do you implement Just-in-Time VM Access?
**A:** Just-in-Time (JIT) VM Access is a feature of **Microsoft Defender for Cloud** that eliminates standing network access to management ports (SSH/22, RDP/3389) on VMs.

**How it works:**
1. JIT locks down management ports by creating a **Deny-all** NSG rule for ports 22 and 3389.
2. When an admin needs access, they **request it** through the Azure Portal, CLI, or API — specifying their source IP and a time window (max 3 hours by default).
3. Defender for Cloud temporarily **opens the NSG rule** only for that specific IP and time window.
4. After the time window expires, the Deny rule is automatically re-applied.

```bash
# Request JIT access via Azure CLI
az security jit-policy initiate \
  --resource-group rg-prod \
  --vm-name vm-web-01 \
  --ports '[{"number":22,"protocol":"TCP","allowedSourceAddressPrefix":"203.0.113.50","maxDuration":"PT3H"}]'
```

> [!important]
> JIT VM access directly addresses the threat of internet-exposed management ports, which are the primary vector for brute-force and ransomware attacks. It should be enabled on **all** internet-facing VMs.

---

## Q9: What are the network security layers in a well-architected AKS cluster?
**A:** A production-grade AKS cluster uses multiple concentric security layers:

```
[Internet]
    |
[Azure Front Door / Application Gateway + WAF]   <-- Layer 7 edge security
    |
[Azure Firewall]                                  <-- Centralized egress filtering
    |
[AKS VNet / Subnet NSG]                          <-- Subnet-level allow/deny rules
    |
[Kubernetes Network Policy]                       <-- Pod-to-pod traffic control
    |
[Service Mesh (Istio/Linkerd)]                    <-- mTLS, pod-level identity
    |
[Pod Security Admission / OPA Gatekeeper]        <-- Policy enforcement
```

Key controls:

| Layer | Technology | Purpose |
|---|---|---|
| Edge | Front Door WAF / App Gateway WAF | Block OWASP Top 10, DDoS |
| Network | Private cluster (no public API server) | API server only reachable from VNet |
| Egress | Azure Firewall + UDR | Restrict outbound internet from pods |
| East-West | Kubernetes Network Policy (Calico/Azure) | Deny pod-to-pod traffic by default |
| Identity | Workload Identity (OIDC) | Pods authenticate to Azure without secrets |
| Runtime | Defender for Containers | Threat detection, vulnerability scanning |

> [!warning]
> A private AKS cluster is the **baseline minimum** for production. Combine it with a private container registry (ACR with private endpoint), private DNS zones, and restricted egress via Azure Firewall.

---

## Q10: Explain Workload Identity Federation (OIDC) and why it replaces client secrets
**A:**

**The problem with client secrets:**
Client secrets (and service principal passwords) are long-lived credentials that must be:
- Generated and stored securely.
- Rotated before expiry (typically 1-2 years).
- Distributed to all consumers (pipelines, apps) — creating secret sprawl.
- Potentially leaked via logs, code repos, or misconfigured storage.

**How Workload Identity Federation works (OIDC):**
Instead of a static secret, the workload (pipeline runner, pod, etc.) presents a **short-lived OIDC token** issued by its own identity provider (GitHub Actions, Azure AKS OIDC issuer). Azure AD is pre-configured to **trust** that issuer and, upon receiving a valid token, issues a short-lived Azure access token.

```
[GitHub Actions Runner]
    | issues short-lived OIDC JWT (valid ~5min)
    |
[Entra ID]
    | validates JWT against GitHub's OIDC endpoint
    | issues Azure access token (no secret ever exchanged)
    |
[Azure Resources (Key Vault, AKS, etc.)]
```

```yaml
# GitHub Actions: Workload Identity Federation (no secrets needed)
- name: Azure Login via OIDC
  uses: azure/login@v2
  with:
    client-id: ${{ vars.AZURE_CLIENT_ID }}
    tenant-id: ${{ vars.AZURE_TENANT_ID }}
    subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}
    # No client-secret! OIDC token handles auth
```

> [!important]
> Workload Identity Federation is the **zero-secrets** approach to CI/CD authentication. There is no secret to leak, no secret to rotate, and no secret to store. It is the recommended method for GitHub Actions, Azure DevOps, AKS pods (via Azure Workload Identity), and Terraform Cloud.

---

## Related Notes
- [[Azure]] — Azure platform, RBAC, Managed Identity
- [[CI-CD]] — Securing CI/CD pipelines
- [[Networking]] — NSG, Azure Firewall, private endpoints
