---
category: Azure-Disaster-Recovery
tags: [azure, asr, dr, failover, architecture]
type: enterprise-architect-guide
status: active
---

# 🌩️ Azure Site Recovery (ASR) - Enterprise Architect Guide

## 1. Introduction
Azure Site Recovery (ASR) is Microsoft's Disaster Recovery as a Service (DRaaS) solution. It ensures business continuity by keeping business apps and workloads running during major regional outages. ASR continuously replicates workloads (Azure VMs, on-premises VMs, and physical servers) from a primary location to a secondary location.

## 2. Why This Service Exists
Backups (Azure Backup) are for data recovery, but they take hours to restore and you lose up to 24 hours of data. If an entire Azure region (e.g., East US) goes down due to a natural disaster, enterprises cannot wait 12 hours to restore from backup. ASR exists to provide near-zero RPO (Recovery Point Objective) and extremely low RTO (Recovery Time Objective), allowing an entire datacenter to fail over to a new region in minutes.

## 3. Architecture
- **Scope:** Cross-Region (or On-Premises to Region).
- **Layer:** IaaS (Compute & Storage Replication).
- **Under the Hood:** ASR does not wait for a daily schedule. It uses a **Mobility Service Extension** installed on the OS to capture block-level disk writes in memory, intercepting them and asynchronously replicating them to a Cache Storage Account in the target region, which then applies them to Replica Managed Disks.

## 4. Core Components
- **Recovery Services Vault:** The management entity orchestrating the replication.
- **Mobility Service Agent:** The agent installed on the source VM that captures disk writes.
- **Cache Storage Account:** A staging storage account in the source/target region to buffer replication data.
- **Replication Policy:** Defines the RPO thresholds and how long to keep app-consistent snapshots (e.g., keep 24 hours of recovery points).
- **Recovery Plan:** An orchestration runbook defining the exact sequence in which VMs should boot up during a failover.

## 5. Step-by-Step Request Flow
**Scenario:** Continuous replication of a VM from East US to West US.
1. The VM in East US writes data to its local Managed Disk.
2. The **Mobility Service Agent** intercepts the block change before it commits to disk.
3. The agent compresses and encrypts the delta changes and sends them over the Azure backbone to a **Cache Storage Account** in West US.
4. The ASR service processes the cache and applies the changes to the **Replica Managed Disk** in West US.
5. In the event of a disaster, the admin clicks "Failover". ASR takes the Replica Managed Disk, attaches it to a newly spun-up compute VM in West US, and connects it to the West US VNet.

## 6. Real-World Production Use Cases
1. **Azure-to-Azure DR:** Replicating a massive ERP system (SAP/SQL) from North Europe to West Europe to meet regulatory requirements for regional resilience.
2. **On-Premises to Azure DR:** Retiring an expensive, physical secondary datacenter and using Azure as the DR site for VMware or Hyper-V workloads.
3. **Cloud Migration:** Using ASR not for disaster recovery, but to lift-and-shift on-premises servers into Azure permanently. Once replicated, you trigger a "failover" and never failback.

## 7. Architecture & Design Considerations
- **Network Mapping:** When a VM fails over, it needs a network. You must pre-create a target VNet in the secondary region and map the source VNet to the target VNet in ASR so the VM gets an IP address immediately upon boot.
- **IP Address Retention:** If your application requires hardcoded IPs, ensure the target VNet has the exact same CIDR block as the primary, and ASR will retain the private IPs upon failover. (Note: The primary VNet must be completely offline to avoid IP conflicts).

## 8. Microsoft Best Practices
- **Do not use ASR for everything:** ASR is for IaaS (Virtual Machines). Do NOT use ASR to replicate Azure SQL Databases, Cosmos DB, or App Services. Those PaaS services have built-in geo-replication mechanisms that are cheaper and more native.
- **Test Failovers Regularly:** Use ASR's "Test Failover" feature every 6 months. It creates a clone of the VMs in an isolated test VNet, allowing you to verify DR readiness without impacting production.

## 9. Security Best Practices
- **Encryption:** Data in transit between regions is encrypted by default. Ensure the target Replica Disks are configured with Azure Disk Encryption (ADE) or Customer-Managed Keys (CMK) at rest.
- **RBAC:** Strictly limit who has the `Site Recovery Contributor` role. An accidental failover click can disrupt production heavily.

## 10. Monitoring & Observability
- **RPO Monitoring:** Monitor the ASR dashboard for **RPO (Recovery Point Objective)**. If the RPO creeps up from 2 minutes to 45 minutes, it means the replication is lagging (often due to massive disk churn or network limits).
- **Log Analytics:** Route ASR diagnostic logs to Log Analytics to track replication health and failover job statuses.

## 11. Backup & Disaster Recovery
- **Failover:** Moving production to the secondary region.
- **Reprotect:** Once failed over, you must "Reprotect" the VMs, which reverses the replication direction (from Secondary back to Primary).
- **Failback:** Failing the workload back to the primary region once the outage is resolved.

## 12. Cost Optimization Techniques
- ASR charges a flat monthly licensing fee per protected instance (~$25/month), plus the cost of the storage consumed by the Replica Disks in the target region.
- **Compute is Free during replication:** You do NOT pay for VM compute costs in the secondary region while replicating. You only pay for the VM compute *after* a failover is triggered and the VM actually spins up.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is the main difference between Backup and Disaster Recovery?
   **A:** Backup is for recovering lost/corrupted data. DR (Site Recovery) is for keeping applications running with minimal downtime during major regional outages.
2. **Q:** Explain RTO and RPO.
   **A:** RTO (Recovery Time Objective): Max acceptable downtime. RPO (Recovery Point Objective): Max acceptable data loss (time measured).

### Intermediate
3. **Q:** What is Azure Site Recovery (ASR)?
   **A:** Azure's DRaaS (Disaster Recovery as a Service) that replicates workloads from a primary region to a secondary region for fast failover.
4. **Q:** How does ASR replicate data without impacting VM performance?
   **A:** It uses an extension to capture block-level changes in memory/disk and asynchronously sends them to a cache storage account in the target region.
5. **Q:** What is a Recovery Plan in ASR?
   **A:** A customizable runbook that defines the exact boot order of VMs during a failover (e.g., start DBs first, then App servers, then Web servers).

### Advanced
6. **Q:** Do you need ASR to protect Azure SQL Databases?
   **A:** No, Azure SQL Database is PaaS and has built-in Auto-Failover Groups and Geo-Replication. ASR is generally for IaaS VMs.
7. **Q:** How do you test a DR failover without causing downtime?
   **A:** ASR provides a "Test Failover" feature, which clones the VMs in the secondary region and connects them to an isolated test VNet, leaving production untouched.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** Replication is falling behind; RPO is expanding to several hours.
  - **Resolution:** Check the disk churn rate (data change rate) on the source VM. Standard ASR handles up to 10-20 MB/s per disk. If the VM is running a heavy database rebuild, it will outpace the replication limit. Upgrade to High Churn ASR if necessary.
- **Scenario:** Test Failover succeeds, but the application doesn't work.
  - **Resolution:** The VMs booted, but in the wrong order. The Web Server booted before the Database server was ready. Fix this by creating a **Recovery Plan** with multiple groups (Group 1: DBs, Group 2: Apps), adding manual wait actions if necessary.

## 15. Hands-on Implementation
**Azure CLI Example (High-Level Steps):**
```bash
# Ensure you have a Recovery Services Vault in the TARGET region
# Enable Replication
az site-recovery protected-item enable-replication \
  --resource-group rg-dr-westus \
  --vault-name rsv-dr-westus \
  --fabric-name PrimaryFabric \
  --protection-container PrimaryContainer \
  --protected-item vm-app-01 \
  --policy-name 24HourRetentionPolicy
```

## 16. Terraform Implementation (IaC)
```hcl
# Note: ASR setup in Terraform is complex and requires Fabric, Containers, and Mappings.
# This is a simplified snippet of the replication enabling.

resource "azurerm_site_recovery_replicated_vm" "vm_replication" {
  name                                      = "vm-app-01-replication"
  resource_group_name                       = azurerm_resource_group.dr_rg.name
  recovery_vault_name                       = azurerm_recovery_services_vault.dr_vault.name
  source_recovery_fabric_name               = azurerm_site_recovery_fabric.primary.name
  source_vm_id                              = azurerm_linux_virtual_machine.primary.id
  recovery_replication_policy_id            = azurerm_site_recovery_replication_policy.policy.id
  source_recovery_protection_container_name = azurerm_site_recovery_protection_container.primary.name
  
  target_resource_group_id                = azurerm_resource_group.dr_rg.id
  target_recovery_fabric_id               = azurerm_site_recovery_fabric.secondary.id
  target_recovery_protection_container_id = azurerm_site_recovery_protection_container.secondary.id
  
  managed_disk {
    # Reference the OS disk ID from the VM's os_disk block, not source_image_reference
    disk_id                    = azurerm_linux_virtual_machine.primary.os_disk[0].managed_disk_id
    staging_storage_account_id = azurerm_storage_account.cache.id
    target_resource_group_id   = azurerm_resource_group.dr_rg.id
    target_disk_type           = "Premium_LRS"
    target_replica_disk_type   = "Premium_LRS"
  }
}
```

## 17. Production Readiness Checklist
- [ ] Are PaaS services utilizing their native Geo-Replication instead of ASR?
- [ ] Is Network Mapping completely configured between the Primary and Secondary VNets?
- [ ] Is a Recovery Plan created to orchestrate the exact boot sequence of the VMs?
- [ ] Are Public IPs in the secondary region pre-staged and attached to Traffic Manager?
- [ ] Was a "Test Failover" successfully executed in an isolated VNet in the last quarter?