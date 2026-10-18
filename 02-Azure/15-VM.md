---
category: Azure-Compute
tags: [azure, compute, vm, iaas, architecture]
type: enterprise-architect-guide
status: active
---

# 💻 Azure Virtual Machines (VM) - Enterprise Architect Guide

## 1. Introduction
Azure Virtual Machines (VM) are scalable, on-demand compute resources provided by Microsoft Azure. They are the backbone of Infrastructure as a Service (IaaS), giving you complete control over the operating system, network configuration, and installed software without the need to manage the underlying physical hardware.

## 2. Why This Service Exists
Before the cloud, organizations had to purchase, rack, power, and cool physical servers—a process that took months and required massive capital expenditure (CapEx). Azure VMs exist to provide instant, scalable infrastructure (OpEx). They are essential for "lift-and-shift" migrations of legacy applications that cannot be modernized into PaaS or containerized environments.

## 3. Architecture
- **Scope:** Regional service (bound to a specific Azure Region and Availability Zone).
- **Layer:** IaaS (Infrastructure as a Service).
- **Under the Hood:** Azure VMs run on massive physical clusters running Hyper-V. Azure abstracts the physical layer, providing you an isolated guest OS. They are heavily interdependent on other Azure resources: **Virtual Networks (VNets)** for connectivity and **Managed Disks** for storage.

## 4. Core Components
- **VM Size (SKU):** Determines the amount of vCPU, RAM, and temporary storage (e.g., D-Series for General Purpose, E-Series for Memory Optimized).
- **OS Disk:** Contains the operating system (Windows/Linux) and boot volume (usually C: or `/`). This is a **persistent** Managed Disk — data survives reboots and deallocations.
- **Data Disk(s):** Separate attached Managed Disks for persistent application data or databases.
- **Network Interface (NIC):** Provides the VM with a private IP address from the VNet and connects it to a subnet.
- **Temporary Disk:** A volatile, physically attached disk (usually D: on Windows or `/dev/sdb1` on Linux) used for page files/swap. **Data is lost upon deallocation.**

## 5. Step-by-Step Request Flow
**Scenario:** An external user accesses an Nginx web server running on an Azure VM.
1. The user's request hits an **Azure Application Gateway** or **Load Balancer** via a Public IP.
2. The Load Balancer forwards the traffic to the VM's **Private IP Address** located on its Network Interface (NIC).
3. The traffic hits the **Network Security Group (NSG)** attached to the VM's subnet/NIC. The NSG evaluates the rule (e.g., Allow Inbound Port 80/443).
4. If allowed, the request hits the Guest OS TCP stack and is processed by the Nginx web service.
5. The VM processes the request (potentially querying a database on another VM) and returns the HTTP response back through the NIC and Load Balancer.

## 6. Real-World Production Use Cases
1. **Lift-and-Shift Migrations:** Moving on-premises legacy applications that require specific registry edits or absolute OS control.
2. **Database Hosting (IaaS):** Hosting SQL Server, Oracle, or proprietary databases that require strict configuration not supported by Azure SQL (PaaS).
3. **Domain Controllers:** Hosting Microsoft Entra Domain Services / Active Directory Domain Controllers in the cloud for hybrid identity management.

## 7. Architecture & Design Considerations
- **Availability Sets vs Zones:** Always architect for failure. Use Availability Zones to distribute VMs across physical datacenters. If Zones are not supported in the region, use Availability Sets to distribute across hardware racks (Fault Domains).
- **SKU Selection:** Do not overprovision. Use B-Series for burstable dev/test, D-Series for web servers, and E-Series for databases.
- **Managed Disks vs Unmanaged:** Always use Managed Disks. They provide 99.999% reliability and simplify storage management.

## 8. Microsoft Best Practices
- **Never Store Persistent Data on the Temporary Drive:** The Temporary drive is volatile. If the VM moves to a different physical host during maintenance, the data is wiped.
- **Use Premium SSDs for Production Workloads:** Standard HDDs/SSDs should only be used for Dev/Test or low-IOPS workloads.
- **Avoid Public IPs:** Never assign Public IPs directly to a VM's NIC in production. Use an Azure Load Balancer, App Gateway, or Azure Firewall for ingress, and NAT Gateway for egress.

## 9. Security Best Practices
- **Just-In-Time (JIT) Access:** Enable JIT in Microsoft Defender for Cloud to keep RDP (3389) and SSH (22) closed by default, opening them only upon approved request.
- **Azure Bastion:** Use Bastion to access VMs over TLS from the Azure Portal, removing the need for public-facing management ports entirely.
- **Encryption:** Use Azure Disk Encryption (ADE) to encrypt the OS and Data disks at rest using BitLocker (Windows) or DM-Crypt (Linux) with keys stored in Azure Key Vault.
- **Identity:** Disable password authentication for Linux VMs and use SSH keys. Use **System-Assigned Managed Identities** for the VM to authenticate to other Azure services securely.

## 10. Monitoring & Observability
- **Azure Monitor Agent (AMA):** Install the AMA extension to collect guest OS metrics (Memory, Logical Disk space) and logs (Windows Event Logs, Syslog) and send them to a Log Analytics Workspace.
- **Boot Diagnostics:** Always enable this. It captures serial console logs and a screenshot of the boot screen, which is critical for troubleshooting a VM that won't start.
- **Alerting:** Set up alerts for `CPU > 90%`, `Available Memory < 1GB`, or `Disk Queue Length` spikes.

## 11. Backup & Disaster Recovery
- **Azure Backup:** Use an Azure Recovery Services Vault to take daily, application-consistent snapshots of the VM. Configure retention policies (e.g., 30 days daily, 12 months monthly).
- **Disaster Recovery (ASR):** Use Azure Site Recovery to continuously replicate the VM's disk state to a secondary paired region for rapid failover (low RTO/RPO) during a massive outage.

## 12. Cost Optimization Techniques
- **Reserved Instances (RIs):** Commit to a 1-year or 3-year term for predictable production workloads to save up to 72% on compute costs.
- **Azure Hybrid Benefit (AHB):** Bring your existing on-premises Windows Server and SQL Server licenses with Software Assurance to Azure to dramatically reduce OS licensing costs.
- **Auto-Shutdown:** For Dev/Test environments, use the built-in auto-shutdown feature to power off VMs at night. (Note: The VM must be in a 'Deallocated' state to stop compute billing; simply shutting it down from within the OS still incurs charges).
- **Spot Instances:** Use Spot VMs for stateless, interruptible batch processing jobs at a massive discount (up to 90%).

## 13. Common Interview Questions

### Beginner
1. **Q:** What is an Azure Virtual Machine?
   **A:** Infrastructure as a Service (IaaS) providing an on-demand, scalable computing server in the cloud.
2. **Q:** What is the difference between a Data Disk and an OS Disk?
   **A:** The OS disk is a **persistent** Managed Disk containing the operating system — data survives reboots and deallocations. Data disks are separate persistent Managed Disks attached for application data storage. Neither should be confused with the **Temporary Disk**, which is ephemeral and lost on deallocation.

### Intermediate
3. **Q:** What is an Availability Set?
   **A:** A logical grouping that ensures your VMs are spread across different hardware racks (Fault Domains and Update Domains) within a single data center to prevent a single hardware failure from taking them all down.
4. **Q:** What are Fault Domains vs Update Domains?
   **A:** Fault Domains share a common power source and network switch (protect against hardware failure). Update domains are logical groups that get rebooted together during planned Azure maintenance.
5. **Q:** How do you stop a VM from being billed for compute costs?
   **A:** You must stop it from the Azure Portal (Deallocated state). Shutting down the OS from inside the VM leaves it in a "Stopped" state and you still pay for compute.

### Advanced
6. **Q:** What are Availability Zones?
   **A:** Physically separate data centers within an Azure region, each with independent power, cooling, and networking. Distributing VMs across zones protects against entire data center failures (99.99% SLA).
7. **Q:** How would you securely connect to a Linux VM without exposing port 22 to the internet?
   **A:** Deploy Azure Bastion, which provides secure SSH access via the browser over TLS, or use JIT VM access in Defender for Cloud to open the port temporarily only to your IP.

## 14. Real-Time Troubleshooting Scenarios
- **Scenario:** The VM is running in the portal, but you cannot RDP or SSH into it.
  - **Resolution:** 
    1. Check the NSG rules applied to the NIC and the Subnet. 
    2. Check if the VM Guest Agent is running.
    3. Check **Boot Diagnostics** to ensure the OS hasn't blue-screened or entered a boot loop.
    4. Reset the NIC or reapply the networking configuration via the portal.
- **Scenario:** High CPU alerts are firing, but the Guest OS task manager shows normal CPU usage.
  - **Resolution:** If the VM is a **B-Series** (Burstable), check the "CPU Credits Consumed" and "CPU Credits Remaining" metrics. The VM has likely exhausted its credits and Azure is throttling it at the hypervisor level. Upgrade the SKU or reduce the load.

## 15. Hands-on Implementation
**Azure CLI Example:**
```bash
az vm create \
  --resource-group rg-compute-prod \
  --name vm-app-01 \
  --image Ubuntu2204 \
  --size Standard_D2s_v3 \
  --vnet-name vnet-core-prod \
  --subnet snet-app \
  --admin-username azureuser \
  --generate-ssh-keys \
  --public-ip-address "" # explicitly avoids creating a public IP
```

## 16. Terraform Implementation (IaC)
```hcl
resource "azurerm_network_interface" "nic" {
  name                = "nic-vm-app-01"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.app.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "vm" {
  name                = "vm-app-01"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  size                = "Standard_D2s_v3"
  admin_username      = "adminuser"
  network_interface_ids = [
    azurerm_network_interface.nic.id,
  ]

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Premium_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "0001-com-ubuntu-server-jammy"
    sku       = "22_04-lts"
    version   = "latest"
  }
}
```

## 17. Production Readiness Checklist
- [ ] Is the VM placed in an Availability Zone (if supported by the region)?
- [ ] Is the VM backed up by a Recovery Services Vault?
- [ ] Are Premium Managed Disks being used for production workloads?
- [ ] Is Boot Diagnostics enabled?
- [ ] Is the Azure Monitor Agent (AMA) installed?
- [ ] Are there NO Public IPs directly attached to the VM?
- [ ] Is disk encryption enabled (ADE)?
- [ ] Has an Auto-shutdown policy been evaluated (for dev/test)?