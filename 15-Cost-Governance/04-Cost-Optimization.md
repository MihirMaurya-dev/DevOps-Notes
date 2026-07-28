---
tags: [devops, azure, cost-governance, cost-optimization, finops]
source: devopsinsiders/batch-18
created: 2026-07-28
updated: 2026-07-28
---

# Azure Cost Optimization Strategies

## Basics
**Cost Optimization** (or FinOps) is the continuous process of maximizing the business value of your cloud spend by identifying mismanaged resources, eliminating waste, and utilizing pricing discounts.

## Why it matters
Cloud resources are billed on a pay-as-you-go model. Without governance, idle resources (like unattached disks or running Dev environments on weekends) will silently drain the IT budget. Proactive optimization can easily reduce cloud bills by 30-50%.

## How it works

### Key Strategies
1. **Azure Budgets & Alerts**: Set a financial limit and get emailed when costs reach 80%, 90%, and 100% of the budget.
2. **Pricing Models**:
   - *Pay-as-you-go*: Most expensive, highly flexible.
   - *Reserved Instances (RIs)*: Commit to 1 or 3 years for up to 72% discount on VMs and DBs.
   - *Spot VMs*: Use spare Azure capacity for up to 90% discount. Can be evicted at any time. Ideal for batch processing.
3. **Right-sizing**: Azure Advisor analyzes CPU/RAM usage and recommends scaling down oversized VMs.
4. **Auto-Shutdown**: Turn off non-prod VMs outside of business hours (e.g., 7 PM to 7 AM).
5. **Storage Tiering**: Move old data from Hot to Cool or Archive tiers.
6. **Azure Hybrid Benefit**: Bring your existing on-premises Windows Server or SQL Server licenses to Azure to waive software costs.

## Azure implementation (with code/CLI)

### Terraform: Auto-shutdown for Dev VMs
```hcl
resource "azurerm_dev_test_global_vm_shutdown_schedule" "shutdown" {
  virtual_machine_id = azurerm_linux_virtual_machine.dev_vm.id
  location           = azurerm_linux_virtual_machine.dev_vm.location
  enabled            = true

  daily_recurrence_time = "1900"
  timezone              = "India Standard Time"

  notification_settings {
    enabled = false
  }
}
```

### AKS Cost Optimization
1. **Cluster Autoscaler**: Scales node pools down to 0 or 1 when pods are not demanding resources.
2. **Spot Node Pools**:
```bash
az aks nodepool add \
    --resource-group myRG \
    --cluster-name myAKS \
    --name spotpool \
    --priority Spot \
    --eviction-policy Delete \
    --spot-max-price -1 \
    --enable-cluster-autoscaler \
    --min-count 1 --max-count 5
```

## Production best practices
- **Find Orphaned Resources**: Regularly search for and delete unattached Managed Disks and Public IPs, as they incur charges even when not attached to a VM.
- **AKS Vertical Pod Autoscaler (VPA)**: Developers often request too much CPU/RAM for their pods. Use VPA to automatically adjust pod requests based on actual usage.
- **Budget per Resource Group**: Set up dedicated budgets per team/project (Resource Group) rather than one massive budget for the whole subscription.

## CI/CD integration
You can use **Infracost** in your CI/CD pipelines to calculate the estimated cost of Terraform changes *before* they are deployed.

```yaml
# GitHub Actions example
- name: Run Infracost
  run: infracost breakdown --path ./terraform --format json --out-file infracost.json
- name: Post PR Comment
  run: infracost comment github --path infracost.json --repo $GITHUB_REPOSITORY --pull-request ${{ github.event.pull_request.number }} --behavior update
```
*This leaves a comment on the PR: "This change will increase your Azure bill by $150/month."*

## Interview Q&A

1. **How do you reduce the cost of a Dev/QA Kubernetes cluster?**
   *Answer*: I would implement Cluster Autoscaler to scale down nodes, use Azure Spot VMs for the worker nodes, and shut down the entire cluster or scale node pools to zero outside of business hours.

2. **What is Azure Hybrid Benefit?**
   *Answer*: It is a licensing benefit that lets you bring your on-premises Windows Server and SQL Server licenses with active Software Assurance to Azure. It significantly reduces the hourly cost of those VMs.

3. **How do you prevent a developer's Terraform script from accidentally spinning up an expensive GPU VM?**
   *Answer*: I would use Azure Policy to restrict the allowed VM sizes (SKUs) in the Dev/QA resource groups.
