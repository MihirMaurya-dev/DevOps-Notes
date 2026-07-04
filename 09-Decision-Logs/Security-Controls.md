---
tags: [decision-log, security, zero-trust, compliance]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Decision Log: Baseline Security Controls

## Context
We need to establish a non-negotiable security baseline for all resources deployed within the Azure Landing Zone to align with Zero Trust principles and meet CIS (Center for Internet Security) Azure Foundations Benchmarks. Hardening newly deployed Azure resources is critical to prevent misconfigurations that lead to data breaches.

## Controls Implemented

### 1. Resource Locks on Production
- **Implementation:** Azure Policy (`DeployIfNotExists`) applied at the Production Management Group to automatically apply `CanNotDelete` locks to all Resource Groups.
- **Compliance Mapping:** CIS 1.1.2.
- **Cost Implication:** Free.

### 2. Defender for Cloud Standard Tier
- **Implementation:** Enabled via Azure Policy at the tenant root. Covers VMs (Defender for Servers) and PaaS (Defender for App Service, Storage, SQL).
- **Compliance Mapping:** CIS 2.1 (Defender CSPM).
- **Cost Implication:** Significant ($15/server/month). Budget approved for production environments.

### 3. NSG Flow Logs and Traffic Analytics
- **Implementation:** Configured via Terraform on Network Watcher. All NSG traffic is logged to the central Log Analytics workspace.
- **Compliance Mapping:** CIS 5.2.9.
- **Cost Implication:** Storage costs for Log Analytics data ingestion.

### 4. Diagnostic Settings to Log Analytics
- **Implementation:** Extensive Azure Policy initiatives that automatically configure Diagnostic Settings to forward audit logs, metrics, and firewall logs to the central workspace.
- **Compliance Mapping:** CIS 5.1 (Ensure diagnostic setting captures appropriate categories).
- **Cost Implication:** Data ingestion costs. Mitigation: Filter out verbose/debug logs at the source where possible.

### 5. Key Vault Soft Delete and Purge Protection
- **Implementation:** Enforced via Terraform (`soft_delete_retention_days = 90`, `purge_protection_enabled = true`). Azure Policy denies creation of Key Vaults without these settings.
- **Compliance Mapping:** CIS 8.1, 8.2.
- **Cost Implication:** Free. Prevents malicious insider deletion of encryption keys.

### 6. Just-in-Time (JIT) VM Access
- **Implementation:** Configured via Defender for Cloud. Removes standing SSH/RDP rules from NSGs. Admins must request access, which temporarily opens the port for a maximum of 3 hours.
- **Compliance Mapping:** CIS 5.2.1, Zero Trust Principle of Least Privilege.
- **Cost Implication:** Included in Defender for Servers Plan 2.

### 7. Private Endpoints for PaaS
- **Implementation:** Deployed via Terraform. Public network access is disabled (`public_network_access_enabled = false`) on Storage Accounts, SQL DBs, and Key Vaults.
- **Compliance Mapping:** CIS 3.1.
- **Cost Implication:** ~$7/month per Private Endpoint + minor data processing charges.

## Monitoring and Alerting Strategy
- Microsoft Sentinel (SIEM) is connected to the central Log Analytics workspace.
- High-severity alerts from Defender for Cloud automatically trigger a Logic App to page the on-call engineer via PagerDuty.
- Scheduled KQL queries run to detect anomalous outbound traffic patterns (potential data exfiltration).

## Outstanding Gaps and Planned Remediation
- **Gap:** Outbound internet access from standard VMs currently bypasses the Azure Firewall if UDRs are misconfigured.
- **Remediation Plan:** Deploy Azure Virtual WAN with Secured Virtual Hub routing intent to enforce centralized egress filtering automatically.
