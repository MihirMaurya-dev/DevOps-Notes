---
tags: [azure, kubernetes, containers]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# ☸️ Azure Kubernetes Service (AKS) — The Beginner's Complete Guide

---

## 📖 Before You Read

This topic builds on some foundational concepts. Before diving in, make sure you understand:
- What a **container** is — think of it like a shipping container for your app: a self-contained box with everything your app needs to run (code, libraries, settings), isolated from everything else
- What **Docker** is — the most popular tool for creating and running containers
- What [[01-Azure|Azure]] is — Microsoft's cloud platform
- What a **Virtual Machine (VM)** is — a virtual computer running in the cloud

If you know those, you're ready. If not, go learn Docker basics first — Kubernetes won't make sense without that foundation!

---

## 🤔 What is Kubernetes? — Plain English + Real-World Analogy

Before understanding **AKS**, let's understand **Kubernetes** first.

Imagine you run a **huge shipping port**. Thousands of shipping containers arrive every day. You need someone to:
- Decide which dock each container goes to
- Monitor if a container falls into the water (and replace it)
- Scale up and get more docks when ships arrive in large numbers
- Scale down and free up docks when the port is quiet
- Route the right trucks to pick up the right containers

Managing all this manually would be chaos. You'd hire a **Port Operations Manager** — someone (or a system) that coordinates everything automatically.

**Kubernetes** (often abbreviated as **K8s** — the 8 replaces the 8 letters between K and s) is that Port Operations Manager — but for your containerized applications (apps running in Docker containers). It automatically:
- Decides which server runs which container
- Restarts containers if they crash
- Adds more containers when traffic increases
- Removes containers when traffic drops
- Routes incoming traffic to the right containers

> 🧠 **In simple words:** Kubernetes is an orchestration system (a coordinator) that automatically manages many containers running across many servers. It keeps your apps running, scales them up and down, and heals them when they break.

---

## 🌟 What is AKS — Azure Kubernetes Service?

**AKS** stands for **Azure Kubernetes Service**. It is Microsoft Azure's **managed Kubernetes offering**.

"Managed" is the key word here. Let's understand what that means:

### 🏗️ Standard Kubernetes (Self-Managed) — You Do Everything

If you set up Kubernetes yourself (on your own servers or VMs), you're responsible for TWO parts:

#### 1. 🧠 The Control Plane (Master Nodes)
This is the "brain" of Kubernetes — the management layer that makes all the decisions:
- **API Server:** The front door — every `kubectl` command (instructions you send to Kubernetes) goes through here. `kubectl` is the Command Line Interface (CLI — a black terminal window where you type commands) for Kubernetes.
- **Scheduler:** Decides which worker node (server) should run each new container
- **etcd:** A database that stores the entire state of your cluster (which containers are running, what their settings are, etc.)
- **Controller Manager:** Constantly checks "what should be running" vs "what is actually running" and fixes differences

You manage all of this yourself — installing, upgrading, securing, backing up. Very complex!

#### 2. 💪 The Data Plane (Worker Nodes)
These are the actual servers where your application containers run. Each worker node has:
- **Kubelet:** An agent that receives instructions from the control plane and manages containers on that node
- **Container Runtime:** The software that actually runs containers (like Docker or containerd)
- **kube-proxy:** Handles network routing on the node

### ☁️ AKS — Microsoft Manages the Control Plane for Free!

In **AKS**, Microsoft takes over the entire **Control Plane** — you don't manage it, you don't pay for it, and you don't worry about it. Microsoft handles:
- ✅ Control plane installation and configuration
- ✅ Upgrading control plane components
- ✅ Backing up etcd
- ✅ Patching security vulnerabilities in the control plane

**You only manage and pay for the Worker Nodes** (the servers running your actual application containers).

```
Standard Kubernetes:   YOU manage Control Plane + Worker Nodes (complex, expensive)
AKS:                   Microsoft manages Control Plane (free) + YOU manage Worker Nodes (simpler!)
```

Think of it like renting an apartment vs owning a building:
- **Own the building (self-managed K8s):** You handle plumbing, electrical, roof — everything
- **Rent an apartment (AKS):** The landlord (Microsoft) handles the building maintenance; you just live in your unit and pay rent (worker node costs)

---

## ⚙️ Key AKS Features — Explained in Plain English

### 🔄 Automated Upgrades and Patching

Kubernetes releases new versions regularly with bug fixes, security patches, and new features. With self-managed Kubernetes, upgrading is complex and risky. AKS simplifies this:
- **Node OS Patching:** Azure automatically applies security updates to the operating system (OS — the software like Linux that runs on your servers) of your worker nodes
- **Kubernetes Version Upgrades:** You can upgrade your cluster's Kubernetes version with a single command or through the portal

```bash
# Upgrade AKS cluster Kubernetes version with one command!
# az = Azure CLI (Command Line Interface)
# aks upgrade = the upgrade command
# --name = your cluster name
# --kubernetes-version = the new version you want

az aks upgrade \
  --resource-group my-resource-group \
  --name my-aks-cluster \
  --kubernetes-version 1.29.0
```

---

### 📈 Scaling — Handling More or Less Traffic Automatically

#### Cluster Autoscaler — Adding/Removing Servers

Imagine your online store normally has 5 servers (worker nodes). On Black Friday, traffic spikes 10x. The **Cluster Autoscaler** automatically adds more worker nodes to handle the extra load, then removes them when traffic goes back to normal — saving you money!

```hcl
# Terraform example: Enabling the Cluster Autoscaler on AKS

resource "azurerm_kubernetes_cluster" "example" {
  name                = "my-aks-cluster"
  location            = "East US"
  resource_group_name = "my-rg"
  dns_prefix          = "myakscluster"    # Used in the cluster's URL

  default_node_pool {
    name       = "systempool"
    node_count = 2            # Start with 2 nodes
    vm_size    = "Standard_D2s_v3"  # The size/spec of each server

    enable_auto_scaling = true   # ← Enable Cluster Autoscaler!
    min_count           = 2      # Never go below 2 nodes (for reliability)
    max_count           = 10     # Never go above 10 nodes (to control costs)
  }

  identity {
    type = "SystemAssigned"   # Managed Identity for AKS to manage Azure resources
  }
}
```

#### Horizontal Pod Autoscaler (HPA) — Adding/Removing App Instances

**HPA** stands for **Horizontal Pod Autoscaler**. 

First: what's a **Pod**? A Pod is the smallest deployable unit in Kubernetes — basically a wrapper around one (or sometimes a few) container(s). Think of it like a worker on an assembly line.

**HPA automatically adds or removes Pods** (more workers!) based on CPU (Central Processing Unit — the main computer processor) usage or memory (RAM) usage.

```yaml
# This is a Kubernetes YAML file — a configuration file written in YAML format
# YAML (Yet Another Markup Language) uses indentation (spaces) to show structure

apiVersion: autoscaling/v2             # Which version of the autoscaling API to use
kind: HorizontalPodAutoscaler          # The type of Kubernetes resource we're creating
metadata:
  name: my-app-hpa                     # Name for this autoscaler
  namespace: default                   # Namespace (like a folder) to put this in

spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment                   # We're scaling a "Deployment" (a running app)
    name: my-web-app                   # The name of the app to scale

  minReplicas: 2    # Always keep at least 2 copies of our app running (for reliability)
  maxReplicas: 20   # Never run more than 20 copies (to control costs)

  metrics:
  - type: Resource
    resource:
      name: cpu                        # Watch CPU usage
      target:
        type: Utilization
        averageUtilization: 70         # When average CPU hits 70%, add more pods!
                                       # When it drops, remove pods to save resources
```

**The result:** When lots of users visit your app simultaneously and CPU usage climbs above 70%, Kubernetes automatically adds more copies (Pods) of your app within minutes. When traffic drops, it removes them. You don't have to do anything!

---

### 🔐 Entra ID Integration — Use Your Azure Login for Kubernetes

**Microsoft Entra ID** is Azure's identity system (like a digital HR department). AKS integrates with it, meaning you can use your Azure credentials to run `kubectl` commands instead of managing separate Kubernetes usernames and passwords.

```bash
# Get credentials for your AKS cluster using your Azure login
# This downloads a "kubeconfig" file — a config file that tells kubectl how to connect to your cluster
az aks get-credentials \
  --resource-group my-resource-group \
  --name my-aks-cluster

# Now you can run kubectl commands! The --admin flag uses Entra ID authentication
kubectl get pods   # List all running pods
kubectl get nodes  # List all worker nodes
```

---

## 🌐 Networking Models in AKS — How Containers Talk to Each Other

This is one of the most important AKS decisions. When you create an AKS cluster, you must choose a **networking model**. Let's explain:

### First: What is a VNet?

A **VNet** (Virtual Network) is a private network inside Azure — like your office's private network. Only resources inside the VNet can talk to each other directly. Resources outside need to go through firewalls and gateways.

An **IP address** (Internet Protocol address) is a unique number assigned to each device on a network, like a mailing address. Example: `10.0.0.5` or `192.168.1.100`.

**Subnets** are smaller divisions of a VNet — like neighborhoods within a city. Each resource in a subnet gets an IP address from that subnet's range.

### 🔵 Option 1: Kubenet (Basic Networking)

🤔 **What is it?**

In Kubenet, only the **Nodes (servers) get real VNet IP addresses**. The **Pods (containers) get IP addresses from a separate, "hidden" address space** — a range of IPs that only exist inside the Kubernetes cluster and aren't part of your Azure VNet.

**Analogy:** Think of a large office building (the VNet). The floors of the building (nodes) have public room numbers (VNet IPs). But inside each floor, there are temporary cubicles (pods) with internal-only desk numbers that nobody outside the floor knows about. To send mail from outside to a cubicle, the mail must go through the floor's front desk first (NAT).

**NAT** (Network Address Translation) is the process of translating between internal and external IP addresses — like a receptionist translating "send this to Desk 42" into an actual room number.

```
External Request → Node IP → (NAT Translation) → Pod's internal IP
```

✅ **Pros:**
- **Conserves VNet IPs** — Pods don't use up your VNet's IP address space. Good when your VNet has limited IP addresses.

❌ **Cons:**
- **Complex troubleshooting** — When something goes wrong, tracing network traffic through NAT layers is harder
- **Pods aren't directly routable** — Other Azure resources (like a database) can't directly reach pods by their IP; traffic must go through a Node

---

### 🟢 Option 2: Azure CNI (Advanced Networking) — Recommended for Production

**CNI** stands for **Container Network Interface** — a standard way for Kubernetes to configure networking. "Azure CNI" is Microsoft's implementation.

🤔 **What is it?**

In Azure CNI, **BOTH Nodes AND Pods get real IP addresses from your VNet**. Every pod is a first-class citizen of your network with its own routable IP address.

**Analogy:** Now every cubicle in the office building gets its own public room number. Anyone (from inside or outside the building) can send mail directly to "Room 10.0.0.42" and it arrives at that specific cubicle with no translation needed.

```
External Request → Pod's actual VNet IP (direct connection, no NAT!)
```

✅ **Pros:**
- **Direct VNet connectivity** — Any Azure resource can talk directly to any Pod
- **No NAT** — Simpler networking, easier to troubleshoot
- **Easier integration** — Databases, other services, firewalls can see real Pod IPs

❌ **Cons:**
- **Consumes many VNet IPs** — Each Pod gets a VNet IP. 100 pods = 100 VNet IPs used! You MUST plan your subnet sizes carefully upfront.

> ⚠️ **Important:** With Azure CNI, you need to plan ahead. If you don't allocate enough IP addresses in your subnet, you'll run out of IPs and won't be able to run more pods. A common formula: `(max nodes × max pods per node) + extra buffer`.

💡 **Terraform Example — Creating an AKS cluster with Azure CNI:**

```hcl
resource "azurerm_kubernetes_cluster" "example" {
  name                = "production-aks"
  location            = "East US"
  resource_group_name = "production-rg"
  dns_prefix          = "prod-aks"

  default_node_pool {
    name            = "systempool"
    node_count      = 3                     # Start with 3 nodes
    vm_size         = "Standard_D4s_v3"     # 4 CPU, 16GB RAM per node
    vnet_subnet_id  = azurerm_subnet.aks_subnet.id  # Which subnet to put nodes and pods in
    
    enable_auto_scaling = true
    min_count           = 3
    max_count           = 20
  }

  network_profile {
    network_plugin = "azure"                # ← "azure" = Azure CNI (Advanced)
                                            # "kubenet" = Kubenet (Basic)
    network_policy = "azure"               # Network Policy controls which pods can talk to which
                                            # "azure" uses Azure's built-in network policy
    service_cidr       = "10.2.0.0/16"    # IP range for Kubernetes internal services
                                            # (must NOT overlap with your VNet!)
    dns_service_ip     = "10.2.0.10"      # IP for Kubernetes' internal DNS server
  }

  identity {
    type = "SystemAssigned"   # AKS uses Managed Identity to manage Azure resources
  }
}
```

---

### Quick Comparison: Kubenet vs Azure CNI

| Feature | Kubenet | Azure CNI |
|---------|---------|-----------|
| Pod IP addresses | Internal only (hidden) | Real VNet IPs |
| Routing | Uses NAT (translation) | Direct (no translation) |
| VNet IP consumption | Low | High (plan carefully!) |
| Troubleshooting | Harder | Easier |
| Direct pod reachability | ❌ No | ✅ Yes |
| Recommended for production | ❌ Not ideal | ✅ Yes |

---

## 💾 Storage Options in AKS

When your containers need to save data that **persists** (survives even if the container restarts), you need storage. Kubernetes calls these **Persistent Volumes (PVs)** — permanent storage attached to pods.

### 🔵 Azure Disks — For Single-Node Databases

**Azure Disks** are like a **USB drive attached to one specific computer**. Once plugged into that computer, only that computer can use it.

- **Access Mode:** `ReadWriteOnce` — meaning only ONE pod (on ONE node) can read and write to it at a time
- **Best for:** Databases (like MySQL, PostgreSQL) running inside Kubernetes, where only one database server needs the storage
- **Backend:** Azure Managed Disks — reliable block storage

```yaml
# A PersistentVolumeClaim (PVC) — a "request" for storage
# Think of it like asking Azure: "Give me 20GB of storage please"

apiVersion: v1
kind: PersistentVolumeClaim   # Type of resource
metadata:
  name: database-storage       # Name for this storage request
spec:
  accessModes:
    - ReadWriteOnce            # Only one pod can use this at a time
  storageClassName: managed-premium   # Use Premium SSD Azure Disks
  resources:
    requests:
      storage: 20Gi            # Request 20 gigabytes of storage
```

### 🟢 Azure Files — For Multi-Node Shared Storage

**Azure Files** is like a **shared network drive** — multiple computers can connect to the same drive simultaneously.

- **Access Mode:** `ReadWriteMany` — multiple pods, across MULTIPLE nodes, can all read AND write to the same storage simultaneously
- **Best for:** Apps that need to share files between multiple instances — for example, a web app with 10 replicas that all need to read/write to the same folder
- **Protocol:** SMB (Server Message Block — the standard Windows file-sharing protocol) or NFS (Network File System — the standard Linux file-sharing protocol)

```yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: shared-file-storage
spec:
  accessModes:
    - ReadWriteMany       # ← Multiple pods across multiple nodes can use this!
  storageClassName: azurefile-premium   # Use Azure Files
  resources:
    requests:
      storage: 50Gi       # 50GB of shared file storage
```

---

## 🏊 Node Pools — Organizing Your Worker Nodes

**Node Pools** are groups of worker nodes with the same configuration (VM size, OS type, etc.). You can have multiple node pools in one cluster.

**Why?** Different workloads have different needs:
- System pods (Kubernetes' own internal services) need reliability but not huge resources
- Application pods might need lots of CPU for web servers
- Machine learning (ML) jobs might need GPU (Graphics Processing Unit — powerful chips for parallel computing) nodes

```hcl
# System node pool — for Kubernetes' own internal services
resource "azurerm_kubernetes_cluster_node_pool" "system" {
  name                  = "systempool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.example.id
  vm_size               = "Standard_D2s_v3"    # Smaller VM (2 CPU, 8GB RAM)
  node_count            = 3
  mode                  = "System"              # "System" = for K8s system pods
  
  node_taints = ["CriticalAddonsOnly=true:NoSchedule"]
  # ☝️ A "taint" is like a label that says "only specific pods can run here"
  # This prevents your app pods from running on system nodes (keeps them separate)
}

# Application node pool — for your actual web application
resource "azurerm_kubernetes_cluster_node_pool" "app" {
  name                  = "apppool"
  kubernetes_cluster_id = azurerm_kubernetes_cluster.example.id
  vm_size               = "Standard_D8s_v3"    # Larger VM (8 CPU, 32GB RAM) for apps
  
  enable_auto_scaling = true
  min_count           = 2
  max_count           = 50                     # Can scale up to 50 nodes for app workloads
  mode                = "User"                 # "User" = for your application pods
}
```

---

## 📊 Monitoring — Container Insights

**Container Insights** is Azure's monitoring solution for AKS. It collects metrics (measurements like CPU usage, memory usage, number of requests) and logs from your cluster and sends them to a **Log Analytics Workspace** (a cloud service for storing and querying logs).

Think of it like a **health monitoring system** — constantly checking your containers' vital signs and alerting you if something is wrong.

> ⚠️ **Important:** The legacy `oms_agent` block (which used the old Log Analytics Agent / OMS Agent) is **deprecated**. The modern approach uses the **Azure Monitor Agent (AMA)** via the `microsoft_monitor_metrics_profile` / `monitor_metrics` block, or by enabling the Container Insights add-on through the AKS `oms_agent` replacement (`azure_monitor_profile`). Always use the AMA-based approach for new deployments.

```hcl
# Modern approach: Enable Azure Monitor Agent (AMA) based Container Insights
resource "azurerm_kubernetes_cluster" "example" {
  # ... other settings ...

  # Azure Monitor profile — uses the Azure Monitor Agent (AMA), NOT the legacy OMS Agent
  monitor_metrics {}
  # Note: Full Container Insights (log collection) is enabled separately via
  # the azurerm_monitor_data_collection_rule resource linked to the cluster.
}
```

---

## ✅ Best Practices Summary

1. **Use Azure CNI for Production** — Direct pod routing makes debugging much easier and enables better integration with other Azure services.

2. **Enable Container Insights** — Always monitor your cluster. "You can't fix what you can't see."

3. **Use Multiple Node Pools** — Separate system pods from app pods. Use different VM sizes for different workload types.

4. **Enable the Cluster Autoscaler** — Don't manually manage node counts. Let AKS scale automatically based on demand.

5. **Use Managed Identity for AKS** — Your AKS cluster needs permissions to create load balancers, manage disks, etc. Use Managed Identity instead of Service Principals with secrets.

6. **Plan your subnet sizes carefully** — Especially with Azure CNI. Running out of IPs is a painful situation to fix after deployment.

---

## ⚠️ Common Mistakes Beginners Make

1. **Choosing Kubenet for production** — Kubenet seems simpler, but the NAT complexity causes real headaches in production. Start with Azure CNI.

2. **Not planning IP address space** — With Azure CNI, if your subnet only has 50 IPs and you try to run 100 pods, you'll fail. Calculate IP needs BEFORE deploying.

3. **Running everything in one node pool** — System pods and app pods competing for the same resources can cause instability. Always separate them.

4. **Not enabling autoscaling** — Manually scaling is tedious and you'll always react too slowly (either paying for idle nodes or running out of capacity during traffic spikes).

5. **Skipping monitoring** — Container Insights feels optional but is essential. When your app starts failing at 3 AM, you'll wish you had set it up.

6. **Using Azure Disks when you need ReadWriteMany** — Azure Disks are ReadWriteOnce only. If you need multiple pods to share the same storage, use Azure Files.

---

## 🎯 Key Takeaway

**AKS** is Microsoft's managed Kubernetes service — Microsoft handles the complex control plane (the brain of Kubernetes) for free, while you manage the worker nodes (where your apps run). Use **Azure CNI** networking for direct pod routing in production, enable the **Cluster Autoscaler** and **HPA** for automatic scaling, use **multiple node pools** to separate different workload types, and always enable **Container Insights** for monitoring.

---

## ❓ Beginner FAQ

**Q1: Do I need to know Kubernetes before using AKS?**
> Yes, at least the basics. AKS makes Kubernetes *easier to operate*, but you still need to understand Kubernetes concepts like Pods, Deployments, Services, and Namespaces. Think of AKS as "Kubernetes with training wheels" — the fundamentals are the same, but Microsoft handles the hardest parts.

**Q2: What's a "Pod" vs a "Container" vs a "Deployment"?**
> A **Container** is the actual running instance of your app (like a Docker container). A **Pod** is a Kubernetes wrapper around one or more containers — it's the smallest thing Kubernetes manages. A **Deployment** is a higher-level resource that manages multiple replicas of a Pod and handles rolling updates (upgrading your app without downtime). Usually: 1 Deployment → manages many Pods → each Pod runs 1 Container.

**Q3: How much does AKS cost?**
> The control plane (the Kubernetes management layer) is FREE on AKS. You only pay for the worker nodes (VMs), storage, networking, and load balancers. A basic cluster with 3 Standard_D2s_v3 nodes costs roughly $150-200/month in East US. Costs vary by region and VM size. Use the Azure Pricing Calculator for estimates.

**Q4: What is `kubectl` and how do I use it?**
> `kubectl` (pronounced "kube-control" or "kube-cuddle") is the command-line tool for interacting with Kubernetes clusters. You type `kubectl` commands in a terminal to deploy apps, check status, view logs, etc. After running `az aks get-credentials`, every `kubectl` command you run goes to your AKS cluster. Common commands: `kubectl get pods` (list pods), `kubectl logs my-pod` (see pod logs), `kubectl apply -f app.yaml` (deploy an app from a config file).

**Q5: What's the difference between Cluster Autoscaler and HPA?**
> **HPA** (Horizontal Pod Autoscaler) adds or removes **Pods** (instances of your app) on existing nodes. If there's enough spare capacity on current nodes, no new servers are needed. **Cluster Autoscaler** adds or removes **Nodes** (the actual servers/VMs) when there aren't enough resources for all the pods that need to run. They work together: HPA says "I need more pods" → if existing nodes are full → Cluster Autoscaler adds a new node → HPA places pods on the new node.
