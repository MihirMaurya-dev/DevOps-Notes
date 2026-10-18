---
category: Azure-Resilience
tags: [azure, backup, recovery, vault, architecture]
type: enterprise-architect-guide
status: active
---

# 💾 Azure Backup - Enterprise Architect Guide

## 1. Introduction
Azure Backup is a simple, secure, and cost-effective cloud-based backup-as-a-service (BaaS) solution. It protects your data from corruption, accidental deletion, and ransomware, allowing you to restore data across Azure VMs, SQL databases, Azure Files, and even on-premises servers.

## 2. Why This Service Exists
Historically, backing up data meant managing complex tape drives, off-site storage facilities, and heavy backup infrastructure servers (like Commvault or Veeam). Azure Backup abstracts all this complexity. It provides infinite, scalable storage to retain data for up to 99 years, with built-in ransomware protection and zero infrastructure to manage.

## 3. Architecture
- **Scope:** Regional (Data resides in a specific Vault, but can be geo-replicated).
- **Layer:** Platform as a Service (PaaS) Storage.
- **Under the Hood:** Azure Backup uses block-level, incremental snapshots. After an initial full backup, only the delta changes (modified blocks) are transferred, drastically reducing network bandwidth and storage costs.

## 4. Core Components
- **Recovery Services Vault (RSV):** The storage entity housing backups for older/traditional workloads (VMs, SQL in VMs, Azure Files, On-prem servers).
- **Backup Vault:** The newer storage entity designed for modern PaaS/IaaS workloads (PostgreSQL, Managed Disks, Azure Blobs).
- **Backup Policy:** Defines the schedule (e.g., daily at 2 AM) and retention logic (e.g., keep daily for 30 days, monthly for 12 months).
- **MARS Agent (Microsoft Azure Recovery Services):** A lightweight agent installed on on-premises Windows machines to back up files/folders directly to Azure.

## 5. Step-by-Step Request Flow
**Scenario:** A scheduled daily backup of an Azure VM.
1. The **Backup Policy** triggers at 2:00 AM.
2. Azure Backup communicates with the **VM Backup Extension** installed on the guest OS.
3. The extension triggers a VSS (Volume Shadow Copy Service) snapshot in Windows (or fsfreeze in Linux) to ensure **application consistency** (flushing memory to disk).
4. An underlying Managed Disk snapshot is created instantly.
5. The snapshot data is transferred in the background to the **Recovery Services Vault**.
6. Once the transfer is complete, the snapshot is deleted, and the Vault retains the recovery point.

## 6. Real-World Production Use Cases
1. **Ransomware Recovery:** A company's file servers are encrypted by ransomware. The admin uses Azure Backup to restore the VMs to the exact state they were in 24 hours prior.
2. **Database Point-in-Time Restore:** Backing up Azure SQL or SQL on IaaS, allowing DBAs to restore the database to a specific minute in time (e.g., 2:14 PM, right before a developer dropped a critical table).
3. **Long-Term Compliance:** Retaining financial data backups for 7-10 years to satisfy SEC or HIPAA regulatory requirements.

## 7. Architecture & Design Considerations
- **LRS vs GRS:** By default, Vaults are Geo-Redundant (GRS), meaning backups are replicated to a secondary region. If your architecture doesn't require cross-region disaster recovery for backups, switch it to Locally Redundant (LRS) *before* protecting any items to save 50% on storage costs.
- **Cross-Region Restore (CRR):** If GRS is enabled, you can enable CRR, allowing you to restore the VM in the secondary region even if the primary region is completely offline.

## 8. Microsoft Best Practices
- **Use Application-Consistent Backups:** Ensure VM backups are application-consistent (VSS integrated) rather than crash-consistent, so databases inside the VMs recover cleanly without corruption.
- **Separate Vaults per Environment:** Do not mix Production backups and Dev/Test backups in the same vault. Apply strict RBAC to the Production vault.

## 9. Security Best Practices
- **Multi-User Authorization (MUA):** Enable MUA via Azure Resource Guard. This requires a second, highly privileged administrator to approve any destructive actions (like deleting a backup policy or modifying retention), preventing rogue admins or hackers from wiping backups.
- **Soft Delete:** Enabled by default. If a hacker deletes a backup item, it is retained in a soft-delete state for 14 days, giving you time to recover it.
- **Immutable Vaults:** Configure the vault to be Immutable, meaning recovery points cannot be deleted or altered by *anyone* before their retention period expires.

## 10. Monitoring & Observability
- **Backup Reports:** Configure Azure Backup Reports to send data to a Log Analytics workspace. This provides PowerBI-like dashboards showing backup failures, storage consumption trends, and cost analytics.
- **Alerts:** Set up Azure Monitor alerts for "Backup Job Failed" to ensure IT operations is immediately notified if a critical server stops backing up.

## 11. Backup & Disaster Recovery
- Azure Backup *is* the backup solution.
- For DR, combine Azure Backup (for data retention) with **Azure Site Recovery (ASR)** (for rapid failover). Backup gives you RPOs of 24 hours (usually), while ASR gives RPOs of seconds.

## 12. Cost Optimization Techniques
- **Selective Disk Backup:** If a VM has a massive 2TB data disk that just holds temporary tempdb or cache files, exclude that specific disk from the backup policy to save massive storage costs.
- **Archive Tier:** Move long-term retention points (e.g., yearly backups kept for 10 years) to the Vault-Archive tier, which is significantly cheaper than the Standard tier.

## 13. Common Interview Questions

### Beginner
1. **Q:** What is Azure Backup?
   **A:** A service that backs up and restores data across the Azure cloud and on-premises, protecting against data loss and ransomware.
2. **Q:** What is a Recovery Services Vault?
   **A:** A storage entity in Azure used to house backup data for VMs, SQL in VMs, and Azure Files.

### Intermediate
3. **Q:** What is the difference between a Recovery Services Vault and a Backup Vault?
   **A:** Recovery Services Vaults are for older/traditional workloads (VMs, Files). Backup Vaults are for newer PaaS/IaaS workloads (Managed Disks, PostgreSQL, Blobs).
4. **Q:** How does Azure Backup protect against ransomware?
   **A:** By using Soft Delete (retains deleted backups for 14 days) and Multi-User Authorization (requires a second admin to approve destructive actions).
5. **Q:** What are LRS and GRS in terms of Backup vaults?
   **A:** LRS (Locally Redundant Storage) keeps 3 copies of backup data in one datacenter. GRS (Geo-Redundant) replicates backup data to a secondary region.

### Advanced
6. **Q:** Can you restore an Azure VM backup to a different region?
   **A:** Yes, if Cross-Region Restore (CRR) is enabled on a GRS vault, you can restore VMs to the paired secondary region.
7. **Q:** What is the Microsoft Azure Recovery Services (MARS) agent?
   **A:** A lightweight agent installed on on-premises Windows servers to back up files, folders, and system state directly to an Azure Recovery Services Vault.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** VM Backup fails with `Extension failed to install or update`.
  - **Resolution:** Check the VM's Guest OS. Ensure the Azure VM Agent is running and up-to-date. Ensure the VM has outbound internet access to Azure Storage (if restricted by NSGs) so the extension can communicate.
- **Scenario:** Backup completes, but is listed as "Crash Consistent" instead of "Application Consistent".
  - **Resolution:** This means VSS failed inside the guest OS. Log into the Windows VM, run `vssadmin list writers`, and look for writers in a "Failed" state. Restart the corresponding services (e.g., SQL VSS Writer).

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
# Create Recovery Services Vault (LRS to save cost for dev)
az backup vault create --resource-group rg-backup-prod --name rsv-prod --location eastus --backup-storage-redundancy LocallyRedundant

# Enable backup for a VM using the DefaultPolicy
az backup protection enable-for-vm \
    --resource-group rg-compute-prod \
    --vault-name rsv-prod \
    --vm vm-app-01 \
    --policy-name DefaultPolicy
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_recovery_services_vault" "vault" {
  name                = "rsv-prod"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "Standard"
  storage_mode_type   = "GeoRedundant"
  
  # Enable Cross Region Restore
  cross_region_restore_enabled = true
}

resource "azurerm_backup_policy_vm" "daily" {
  name                = "policy-daily-30d"
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name

  timezone = "UTC"

  backup {
    frequency = "Daily"
    time      = "02:00"
  }

  retention_daily {
    count = 30
  }

  retention_monthly {
    count    = 12
    weekdays = ["Sunday"]
    weeks    = ["First"]
  }
}

resource "azurerm_backup_protected_vm" "vm_backup" {
  resource_group_name = azurerm_resource_group.rg.name
  recovery_vault_name = azurerm_recovery_services_vault.vault.name
  source_vm_id        = azurerm_linux_virtual_machine.vm.id
  backup_policy_id    = azurerm_backup_policy_vm.daily.id
}
```

## 17. Production Readiness Checklist
- [ ] Is Soft Delete enabled and configured?
- [ ] Are Immutable Vaults or Multi-User Authorization (MUA) implemented to protect against ransomware?
- [ ] Are non-critical disks excluded from the backup policy to save costs?
- [ ] Is Cross-Region Restore (CRR) enabled for mission-critical VMs?
- [ ] Are Backup Reports configured and streaming to a Log Analytics Workspace?
- [ ] Have you successfully performed a test restore drill in the last 6 months?