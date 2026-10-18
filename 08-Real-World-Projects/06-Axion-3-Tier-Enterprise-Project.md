---
tags: [real-world-project, azure, terraform, 3-tier, axion, ci-cd, devopsinsiders]
source: devopsinsiders/batch-18
created: 2026-09-30
updated: 2026-10-18
level: advanced
---

# 🚀 Project 06: Axion 3-Tier Enterprise Infrastructure & CI/CD Platform

---

## 📖 Before You Read

- Review 3-Tier Architecture Theory → [[01-3-Tier-Architecture]]
- Review Azure Key Vault Deep Dive → [[09-Key-Vault]]
- Review Azure DevOps YAML Multi-Stage Pipelines → [[05-Terraform-Pipeline]], [[09-Pipeline-Parallelism-and-Optimization]]
- Review Terraform Modular Architecture → [[10-Modules]]

---

## 🌟 Executive Summary

The **Axion 3-Tier Enterprise Project** is the flagship end-to-end cloud infrastructure implementation developed in **DevOps Insiders Batch 18**. It represents a real-world, enterprise-scale web application infrastructure built entirely from scratch using **Modular Terraform (IaC)**, deployed on **Microsoft Azure**, and automated through **Azure DevOps Multi-Stage YAML Pipelines**.

```
Axion 3-Tier Enterprise Architecture:
                                  ┌────────────────────────┐
                                  │      Public Users      │
                                  └───────────┬────────────┘
                                              │ HTTPS (443)
                                              ▼
                                  ┌────────────────────────┐
                                  │     Public IP / LB     │
                                  └───────────┬────────────┘
                                              │
    Azure VNet: vnet-axion-preprod (10.0.0.0/16)
┌─────────────────────────────────────────────┼─────────────────────────────────────────────┐
│                                             ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Tier 1: Frontend Subnet (10.0.1.0/24)                                               │  │
│  │  ┌─────────────────────────┐     ┌─────────────────────────┐                        │  │
│  │  │ VM: vm-frontend-01      │     │ VM: vm-frontend-02      │                        │  │
│  │  │ (React + NGINX)         │     │ (React + NGINX)         │                        │  │
│  │  └───────────┬─────────────┘     └───────────┬─────────────┘                        │  │
│  └──────────────┼───────────────────────────────┼──────────────────────────────────────┘  │
│                 │ Internal HTTP (Port 8000/5000)│                                         │
│                 ▼                               ▼                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Tier 2: Backend Subnet (10.0.2.0/24)                                                │  │
│  │  ┌─────────────────────────┐     ┌─────────────────────────┐                        │  │
│  │  │ VM: vm-backend-01       │     │ VM: vm-backend-02       │                        │  │
│  │  │ (Python FastAPI / Java) │     │ (Python FastAPI / Java) │                        │  │
│  │  └───────────┬─────────────┘     └───────────┬─────────────┘                        │  │
│  └──────────────┼───────────────────────────────┼──────────────────────────────────────┘  │
│                 │ PostgreSQL Wire Protocol (Port 5432)                                    │
│                 ▼                                                                         │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Tier 3: Database Subnet (10.0.3.0/24)                                               │  │
│  │  ┌───────────────────────────────────────────────────────────────────────────────┐  │  │
│  │  │ Azure Database for PostgreSQL Flexible Server (PaaS with VNet Integration)    │  │  │
│  │  │ (Automated Backups, High Availability, Zone-Redundant Storage)               │  │  │
│  │  └───────────────────────────────────────────────────────────────────────────────┘  │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
│                                                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────────────────┐  │
│  │ Management & Security Subnets                                                       │  │
│  │  ┌─────────────────────────┐     ┌─────────────────────────┐                        │  │
│  │  │ AzureBastionSubnet      │     │ private-endpoint-subnet │                        │  │
│  │  │ (Secure RDP/SSH Gateway)│     │ (Azure Key Vault)       │                        │  │
│  │  └─────────────────────────┘     └─────────────────────────┘                        │  │
│  └─────────────────────────────────────────────────────────────────────────────────────┘  │
└───────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🎯 Architecture Pillars

### 1. Presentation Tier (Frontend)
- **Workload:** React single-page application built for high responsiveness.
- **Compute:** Ubuntu 22.04 LTS Virtual Machines running NGINX as a reverse proxy.
- **Network Ingress:** Accessible externally via Public IP / Azure Load Balancer on ports 80/443.

### 2. Application Tier (Backend)
- **Workload:** Python FastAPI and Java microservices processing business logic, authentication, and API endpoints.
- **Compute:** Virtual Machines configured with System-Assigned Managed Identity.
- **Network Isolation:** Positioned inside `backend-subnet`. Inbound traffic is strictly restricted to traffic originating from `frontend-subnet`. Internet access is blocked.

### 3. Data Tier (Database)
- **Workload:** Relational database storage.
- **Deployment Model:** **Azure Database for PostgreSQL Flexible Server** (PaaS) integrated directly into a delegated `database-subnet`.
- **Security:** Zero public internet access. Port 5432 is accessible strictly from `backend-subnet`. Data encrypted at rest and in transit (SSL/TLS 1.3).

### 4. Governance & Management Tier
- **Azure Bastion:** Deployed into `AzureBastionSubnet` to allow engineers to securely SSH into VMs via the Azure Portal without attaching public IPs to backend or frontend VMs.
- **Azure Key Vault:** Dedicated private Key Vault for storing administrative credentials, database master passwords, and API secrets.

---

## 🧱 Terraform Modular Architecture

The Axion infrastructure is engineered with a **Child/Parent module pattern**, ensuring complete separation of environment definitions from reusable cloud resource code.

```
Codebase Hierarchy:
Axion-Crash-Course-Infra-Code/
├── environments/
│   ├── preprod/
│   │   ├── main.tf                 # Calls reusable child modules
│   │   ├── provider.tf             # AzureRM provider & remote backend
│   │   ├── variables.tf            # Environment variable declarations
│   │   └── terraform.tfvars        # Preprod values (maps of objects)
│   └── prod/
│       ├── main.tf
│       ├── provider.tf
│       ├── variables.tf
│       └── terraform.tfvars        # Prod-specific high-availability values
└── modules/
    ├── azurerm_resource_group/
    ├── azurerm_virtual_network/
    ├── azurerm_subnet/
    ├── azurerm_public_ip/
    ├── azurerm_virtual_machine/
    └── azurerm_postgres_flexible_server/
```

### Parent Module Implementation (`environments/preprod/main.tf`)

```hcl
module "rg" {
  source = "../../modules/azurerm_resource_group"
  rgs    = var.rgs
}

module "vnet" {
  depends_on = [module.rg]
  source     = "../../modules/azurerm_virtual_network"
  vnets      = var.vnets
}

module "subnet" {
  depends_on = [module.vnet]
  source     = "../../modules/azurerm_subnet"
  subnets    = var.subnets
}

module "pips" {
  depends_on = [module.rg]
  source     = "../../modules/azurerm_public_ip"
  public_ips = var.public_ips
}

module "vms" {
  depends_on       = [module.subnet, module.pips]
  source           = "../../modules/azurerm_virtual_machine"
  virtual_machines = var.virtual_machines
}

module "postgressql" {
  depends_on         = [module.rg, module.subnet]
  source             = "../../modules/azurerm_postgres_flexible_server"
  postgresql_servers = var.postgresql_servers
}
```

### PostgreSQL PaaS Child Module (`modules/azurerm_postgres_flexible_server/main.tf`)

```hcl
resource "azurerm_postgresql_flexible_server" "postgres" {
  for_each               = var.postgresql_servers
  name                   = each.value.name
  resource_group_name    = each.value.resource_group_name
  location               = each.value.location
  version                = each.value.version
  delegated_subnet_id    = each.value.delegated_subnet_id
  private_dns_zone_id    = each.value.private_dns_zone_id
  administrator_login    = each.value.administrator_login
  administrator_password = each.value.administrator_password
  zone                   = each.value.zone

  storage_mb             = each.value.storage_mb
  sku_name               = each.value.sku_name
  backup_retention_days  = 7

  tags                   = each.value.tags
}
```

---

## 🔄 Azure DevOps Multi-Stage CI/CD Pipeline

The Axion platform is deployed using an automated multi-stage pipeline (`azure-pipeline.yml`) executed on a self-hosted agent pool (`vistara-agents`):

```
CI/CD Pipeline Flow:
┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐     ┌──────────────────────┐
│ Stage 1: Init & Val  │ ──► │ Stage 2: Plan        │ ──► │ Stage 3: Approval    │ ──► │ Stage 4: Apply       │
│ • terraform init     │     │ • terraform plan     │     │ • Server pool gate   │     │ • terraform apply    │
│ • terraform validate │     │ • publish plan art   │     │ • Manual review      │     │ • on 'main' branch   │
└──────────────────────┘     └──────────────────────┘     └──────────────────────┘     └──────────────────────┘
```

### Complete Pipeline Definition (`azure-pipeline.yml`)

```yaml
pool: vistara-agents

trigger:
  - main
  - feature/*

stages:

  # Stage 1: Init and Validate
  - stage: TerraformInitAndValidate
    displayName: 'Init and Validate'
    jobs: 
      - job: InitAndValidate
        displayName: 'Init and Validate'
        steps:
          - task: TerraformTask@5
            displayName: 'Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'
              backendServiceArm: 'corp-prod-01-sc'
              backendAzureRmStorageAccountName: 'distoragetf786'
              backendAzureRmContainerName: 'tfstate'
              backendAzureRmKey: 'preprod.terraform.tfstate'

          - task: TerraformTask@5
            displayName: 'Terraform Validate'
            inputs:
              provider: 'azurerm'
              command: 'validate'
              workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'

  # Stage 2: Plan
  - stage: TerraformPlan
    displayName: 'Plan'
    condition: succeeded()
    dependsOn: TerraformInitAndValidate
    jobs: 
      - job: TerraformPlan
        displayName: 'Plan'
        steps:
          - task: TerraformTask@5
            displayName: 'Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'
              backendServiceArm: 'corp-prod-01-sc'
              backendAzureRmStorageAccountName: 'distoragetf786'
              backendAzureRmContainerName: 'tfstate'
              backendAzureRmKey: 'preprod.terraform.tfstate'

          - task: TerraformTask@5
            displayName: 'Terraform Plan'
            inputs:
              provider: 'azurerm'
              command: 'plan'
              workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'
              environmentServiceNameAzureRM: 'corp-prod-01-sc'

  # Stage 3: Manual Approval Gate
  - stage: ManualApproval
    displayName: 'Manual Approval Before Apply'
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    dependsOn: TerraformPlan
    jobs:
      - job: Approval
        displayName: 'Waiting for Approval'
        pool: server          # Server pool avoids locking build agent
        steps:
          - task: ManualValidation@1
            displayName: 'Approve Terraform Apply'
            inputs:
              notifyUsers: ''
              instructions: 'Terraform Plan complete hai. Apply karne ke liye approval dein.'
              onTimeout: 'reject'

  # Stage 4: Apply
  - stage: TerraformApply
    displayName: 'Apply'
    condition: and(succeeded(), eq(variables['Build.SourceBranch'], 'refs/heads/main'))
    dependsOn: ManualApproval
    jobs: 
      - job: TerraformApply
        displayName: 'Apply'
        steps:
          - task: TerraformTask@5
            displayName: 'Terraform Init'
            inputs:
              provider: 'azurerm'
              command: 'init'
              workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'
              backendServiceArm: 'corp-prod-01-sc'
              backendAzureRmStorageAccountName: 'distoragetf786'
              backendAzureRmContainerName: 'tfstate'
              backendAzureRmKey: 'preprod.terraform.tfstate'

          - task: TerraformTask@5
            displayName: 'Terraform Apply'
            inputs:
              provider: 'azurerm'
              command: 'apply'
              workingDirectory: '$(System.DefaultWorkingDirectory)/environments/preprod'
              environmentServiceNameAzureRM: 'corp-prod-01-sc'
```

---

## 🏆 Business Value & Operational Metrics

| Metric | Before Axion Automation | After Axion Platform |
|--------|-------------------------|----------------------|
| **Environment Provisioning Time** | 3 - 4 Days (Manual Portal clicks) | **12 Minutes** (Terraform apply) |
| **Configuration Drift** | High (Uncontrolled manual changes) | **Zero** (All infra declared in Git) |
| **Security Compliance** | Vulnerable (Hardcoded credentials) | **100% Secure** (Key Vault + Managed Identity) |
| **Blast Radius** | Entire Environment | **Subnet Level** (NSG Tiered Isolation) |
| **Deployment Risk** | High (No pre-approval review) | **Low** (Automated plan review + Manual Gate) |

---

## 🔗 Related Notes

- [[01-3-Tier-Architecture]] — 3-Tier Enterprise Architecture Design
- [[09-Key-Vault]] — Azure Key Vault Enterprise Deep Dive
- [[09-Pipeline-Parallelism-and-Optimization]] — Pipeline Parallelism and Optimization
- [[10-Parameterized-Pipelines-and-Templates]] — Reusable Templates and Parameters
- [[05-Interview-Strategy-and-Introductions]] — How to present this project in interviews
