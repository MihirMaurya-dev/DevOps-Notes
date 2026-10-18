---
tags: [terraform, azure, kubernetes, azurerm_kubernetes_cluster]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# ☸️ Terraform Resource: azurerm_kubernetes_cluster

> "AKS is a giant cruise ship for your Docker containers. Microsoft drives the ship, you just tell them how many passenger cabins you need."

---

## 📖 Before You Read

Before diving into this Terraform resource, make sure you understand:
- What **Docker Containers** are — they are lightweight, standalone packages of software.
- What **Kubernetes** is — it's the conductor of the orchestra that manages thousands of containers.
- What a **Virtual Machine** is — see [[VM]] (because Kubernetes uses VMs under the hood!).

---

## 1. 🤔 What is `azurerm_kubernetes_cluster`?

### 🤔 What is it?

**Azure Kubernetes Service (AKS)** is Microsoft's managed Kubernetes platform. Normally, setting up a Kubernetes cluster from scratch is incredibly difficult (you have to build the control plane, manage the databases, and network the worker nodes). AKS does all the hard work for you.

In Terraform, the `azurerm_kubernetes_cluster` resource tells Microsoft to build that cluster and hand you the keys.

> 🚢 **Real-World Analogy:**
> Imagine managing a shipping company. In the old days (Virtual Machines), you bought individual trucks and drove them yourself. 
> 
> Kubernetes is a massive cargo ship. You just drop your shipping containers (Docker containers) onto the deck, and the ship's Captain (the Kubernetes Control Plane) figures out how to balance the weight and steer to the destination. 
> 
> `azurerm_kubernetes_cluster` is you paying Microsoft to provide the ship and the Captain. You only have to pay for the fuel (the worker nodes)!

---

## 2. 🧠 Why do we need it?

If your company has a microservices architecture (meaning your app is broken into 50 different small Docker containers), deploying them to 50 different Virtual Machines manually is a nightmare.

Kubernetes automatically restarts containers if they crash, scales them up if traffic spikes, and routes network traffic between them. 

Using Terraform to deploy AKS ensures that your cluster is integrated with your existing VNet, uses the correct Managed Identity, and has Azure Active Directory (Entra ID) security enabled from Day 1.

---

## 3. ⚙️ How does it work?

A basic AKS cluster requires a few core components in Terraform:
1. `name`: The cluster name.
2. `dns_prefix`: A unique prefix used to generate the cluster's public API address.
3. `default_node_pool`: The actual Virtual Machines (worker nodes) that will run your containers. You must specify how many VMs you want (`node_count`) and how big they are (`vm_size`).
4. `identity`: How the cluster authenticates to Azure. Modern clusters use `SystemAssigned` Managed Identities instead of messy Service Principals.

---

## 4. 💡 Real Example (Line-by-Line)

Here is a basic, beginner-friendly implementation of an AKS cluster.

### `variables.tf` (The Inputs)
```hcl
variable "cluster_name" {
  type        = string
  description = "The name of the AKS cluster."
  default     = "aks-myapp-prod-eus"
}

variable "resource_group_name" {
  type    = string
  default = "rg-containers-prod"
}

variable "location" {
  type    = string
  default = "eastus"
}

variable "dns_prefix" {
  type        = string
  description = "DNS prefix used for the Kubernetes API server."
  default     = "aks-myapp-prod"
}
```

### `main.tf` (The Actual Resource)
```hcl
# ---- THE RESOURCE BLOCK ----
resource "azurerm_kubernetes_cluster" "main" {
  name                = var.cluster_name
  location            = var.location
  resource_group_name = var.resource_group_name
  dns_prefix          = var.dns_prefix

  # 🖥️ The Node Pool: The actual computers that run your containers
  default_node_pool {
    name       = "systempool"    # Name of the pool
    node_count = 2               # Start with 2 Virtual Machines
    vm_size    = "Standard_D2_v2" # 2 CPUs, 7GB RAM per machine
  }

  # 🪪 Identity: Let Azure create a Managed Identity for the cluster automatically
  identity {
    type = "SystemAssigned"
  }

  tags = {
    Environment = "Production"
  }
}
```

### `outputs.tf` (The Results)
```hcl
output "kubernetes_cluster_id" {
  description = "The Azure Resource ID of the cluster."
  value       = azurerm_kubernetes_cluster.main.id
}

output "kube_config" {
  description = "The secret config file needed to connect to the cluster from your laptop!"
  value       = azurerm_kubernetes_cluster.main.kube_config_raw
  sensitive   = true # Do NOT print this to the screen!
}
```

---

## 5. ⚠️ Common Mistakes Beginners Make

1. **Using Too Small of a VM:** Beginners often pick `Standard_B2s` (a very cheap VM) for their `default_node_pool` to save money. Kubernetes itself takes up a lot of RAM just to run. If the VM is too small, your containers will constantly crash with `OOMKilled` (Out Of Memory) errors. Always use at least `Standard_D2_v2` or higher.
2. **Hardcoding Node Counts:** In enterprise setups, you shouldn't use a static `node_count = 2`. You should enable `enable_auto_scaling = true` and set a `min_count` and `max_count`. This lets the cluster automatically buy more VMs if traffic spikes!
3. **Putting Everything in the Default Pool:** Best practice is to use the `default_node_pool` ONLY for core Kubernetes system services. You should create a completely separate Terraform resource (`azurerm_kubernetes_cluster_node_pool`) called a "User Pool" where your actual application containers run.

---

## 6. 🎯 Key Takeaway

The `azurerm_kubernetes_cluster` resource provisions a fully functional Kubernetes environment without you having to build the control plane. You define the cluster, configure the virtual machines in the `default_node_pool`, and Azure handles the rest. Always protect the `kube_config_raw` output, as it is the master key to your cluster!

---

## 7. ❓ Beginner FAQ

**Q1: How do I actually deploy my Docker containers after Terraform builds the cluster?**
> Terraform's job is just to build the "empty ship" (the cluster infrastructure). Once it is built, you use a different tool, like `kubectl` or `Helm`, inside your CI/CD pipeline to deploy your actual application code into the cluster.

**Q2: Does the cluster connect to my VNet?**
> Yes! In advanced configurations, you can use the `network_profile` block in Terraform to plug the AKS cluster directly into an existing `azurerm_subnet`. This ensures your containers can securely talk to your databases.

**Q3: What is the `kube_config` output?**
> It is a chunk of text that contains the web address of the cluster and the certificates needed to log in. You save this text as a file on your laptop (usually at `~/.kube/config`), which allows the `kubectl` command-line tool to talk to the cluster.
