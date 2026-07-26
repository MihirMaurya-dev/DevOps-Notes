---
tags: [architecture, 3-tier, azure, networking, nsg, appgateway]
source: devopsinsiders/batch-18
created: 2026-07-26
updated: 2026-07-26
---

# 🏛️ 3-Tier Application Architecture on Azure

A 3-tier architecture splits an application into three **logically and physically separate layers**, each in its own subnet with strict network controls. It is the most widely used pattern for hosting enterprise web applications on Azure.

---

## 1. What Is 3-Tier Architecture?

```
Internet
    │
    ▼
┌─────────────────────────────────────────┐
│  PRESENTATION TIER  (Web / Frontend)    │  ← Public-facing, load-balanced
│  Azure Application Gateway + WAF        │
│  VMs / App Service / AKS (Ingress)      │
└────────────────┬────────────────────────┘
                 │ (Private traffic only)
    ▼
┌─────────────────────────────────────────┐
│  APPLICATION TIER  (App / Backend)      │  ← Business logic, private subnet
│  VMs / Azure Functions / AKS Pods       │
│  Internal Load Balancer                 │
└────────────────┬────────────────────────┘
                 │ (Private traffic only)
    ▼
┌─────────────────────────────────────────┐
│  DATA TIER  (Database / Storage)        │  ← Strictest security, no internet
│  Azure SQL / CosmosDB / PostgreSQL      │
│  Azure Storage / Redis Cache            │
└─────────────────────────────────────────┘
```

| Tier | Purpose | Azure Services |
|------|---------|---------------|
| **Presentation** | User interface — serves HTML/API responses | App Gateway + WAF, App Service, AKS |
| **Application** | Business logic — processes requests | VMs, Azure Functions, AKS, API Management |
| **Data** | Data storage — stores and retrieves data | Azure SQL, CosmosDB, PostgreSQL, Redis |

---

## 2. Azure Network Design

Each tier lives in its own **subnet** inside a single **VNet**:

```
VNet: 10.0.0.0/16
│
├── web-subnet      10.0.1.0/24    (Presentation — App Gateway + Web VMs)
├── app-subnet      10.0.2.0/24    (Application — Backend VMs)
└── db-subnet       10.0.3.0/24    (Data — Azure SQL / DB VMs)
```

**NSG Rules per tier:**

| Tier | Allow Inbound From | Deny |
|------|--------------------|------|
| Web Subnet | Internet (port 443) | All other |
| App Subnet | Web Subnet only (port 8080) | Internet, DB Subnet |
| DB Subnet | App Subnet only (port 1433/5432) | Internet, Web Subnet |

---

## 3. Terraform Implementation

```hcl
# ─── VNet & Subnets ───────────────────────────────────────────────────────────
resource "azurerm_virtual_network" "vnet" {
  name                = "vnet-app-prod"
  address_space       = ["10.0.0.0/16"]
  location            = var.location
  resource_group_name = var.rg_name
}

resource "azurerm_subnet" "subnets" {
  for_each = {
    web = "10.0.1.0/24"
    app = "10.0.2.0/24"
    db  = "10.0.3.0/24"
  }
  name                 = "${each.key}-subnet"
  resource_group_name  = var.rg_name
  virtual_network_name = azurerm_virtual_network.vnet.name
  address_prefixes     = [each.value]
}

# ─── NSG: Web Tier ────────────────────────────────────────────────────────────
resource "azurerm_network_security_group" "web_nsg" {
  name                = "nsg-web"
  location            = var.location
  resource_group_name = var.rg_name

  security_rule {
    name                       = "allow-https-inbound"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
    source_port_range          = "*"
    destination_port_range     = "443"
  }
}

# ─── NSG: App Tier ────────────────────────────────────────────────────────────
resource "azurerm_network_security_group" "app_nsg" {
  name                = "nsg-app"
  location            = var.location
  resource_group_name = var.rg_name

  security_rule {
    name                       = "allow-from-web-tier"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_address_prefix      = "10.0.1.0/24"   # Web subnet only
    destination_address_prefix = "*"
    source_port_range          = "*"
    destination_port_range     = "8080"
  }

  security_rule {
    name                       = "deny-internet-inbound"
    priority                   = 4096
    direction                  = "Inbound"
    access                     = "Deny"
    protocol                   = "*"
    source_address_prefix      = "Internet"
    destination_address_prefix = "*"
    source_port_range          = "*"
    destination_port_range     = "*"
  }
}

# ─── NSG: DB Tier ─────────────────────────────────────────────────────────────
resource "azurerm_network_security_group" "db_nsg" {
  name                = "nsg-db"
  location            = var.location
  resource_group_name = var.rg_name

  security_rule {
    name                       = "allow-from-app-tier"
    priority                   = 100
    direction                  = "Inbound"
    access                     = "Allow"
    protocol                   = "Tcp"
    source_address_prefix      = "10.0.2.0/24"   # App subnet only
    destination_address_prefix = "*"
    source_port_range          = "*"
    destination_port_range     = "1433"           # SQL Server port
  }
}

# ─── Associate NSGs with Subnets ──────────────────────────────────────────────
resource "azurerm_subnet_network_security_group_association" "web" {
  subnet_id                 = azurerm_subnet.subnets["web"].id
  network_security_group_id = azurerm_network_security_group.web_nsg.id
}

resource "azurerm_subnet_network_security_group_association" "app" {
  subnet_id                 = azurerm_subnet.subnets["app"].id
  network_security_group_id = azurerm_network_security_group.app_nsg.id
}

resource "azurerm_subnet_network_security_group_association" "db" {
  subnet_id                 = azurerm_subnet.subnets["db"].id
  network_security_group_id = azurerm_network_security_group.db_nsg.id
}
```

---

## 4. Production-Grade Enhancements

| Enhancement | Why | Azure Service |
|------------|-----|--------------|
| **WAF on App Gateway** | Block OWASP Top 10 at the edge | App Gateway v2 + WAF policy |
| **Private Endpoints for DB** | Disable public DB access entirely | Azure Private Link |
| **Azure Bastion** | Secure SSH/RDP without public IPs on VMs | Azure Bastion |
| **Key Vault for DB credentials** | No hardcoded connection strings | Azure Key Vault + Managed Identity |
| **Internal Load Balancer** | Distribute traffic to app tier VMs | Azure Internal LB (Standard SKU) |
| **Azure Monitor + Alerts** | End-to-end observability per tier | Azure Monitor, Log Analytics |

---

## 5. CI/CD Deployment Strategy

```yaml
# GitHub Actions — 3-Tier Terraform Deploy
name: Deploy 3-Tier App

on:
  push:
    branches: [main]

jobs:
  deploy-network:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Terraform Plan & Apply — VNet + Subnets + NSGs
        run: |
          terraform init
          terraform apply -auto-approve -target=azurerm_virtual_network.vnet \
                          -target=azurerm_subnet.subnets \
                          -target=azurerm_network_security_group.web_nsg \
                          -target=azurerm_network_security_group.app_nsg \
                          -target=azurerm_network_security_group.db_nsg

  deploy-app:
    needs: deploy-network
    runs-on: ubuntu-latest
    steps:
      - name: Deploy App Tier (after network is ready)
        run: terraform apply -auto-approve
```

> [!tip]
> Use `-target` in CI only for ordered deployments. In day-to-day Terraform runs, avoid `-target` as it hides dependency issues.

---

## 6. Security Checklist

- [ ] No VM in any tier has a Public IP directly (use App Gateway / Bastion)
- [ ] DB tier NSG explicitly denies traffic from everywhere except App subnet
- [ ] Azure SQL / PostgreSQL has public network access **disabled** (Private Endpoint only)
- [ ] App Gateway WAF enabled in **Prevention** mode (not just Detection)
- [ ] Managed Identity used by App VMs to fetch DB credentials from Key Vault
- [ ] DDoS Standard Plan enabled on VNet (for production workloads)
- [ ] Network Watcher Flow Logs enabled on all NSGs
