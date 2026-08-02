---
tags: [azure, compute, workload, migration, cloud-fundamentals]
title: Compute Workloads & Cloud Migration
created: 2026-08-01
---

# 🚀 Compute Workloads & Cloud Migration

Understanding the relationship between workloads and migrations is essential for transitioning from on-premises data centers to the cloud.

## 1. What is a "Compute Workload"?
A **Workload** is any application, service, or capability that takes up computing resources (CPU, Memory, Storage) to do a job. 
When we say **Compute Workload**, we are specifically referring to the resources actively running the logic of your application. 

In Azure, compute workloads usually fall into these deployment models:

| Deployment Model | Azure Service Example | Description | Management Overhead |
| :--- | :--- | :--- | :--- |
| **IaaS (Infrastructure)** | Azure Virtual Machines (VMs) | You manage the OS, runtime, and the application. | High |
| **Containers** | Azure Kubernetes Service (AKS), ACI | Running applications packaged with their dependencies. | Medium |
| **PaaS (Platform)** | Azure App Service, Azure SQL | You just deploy your code/data; Azure manages the underlying servers. | Low |
| **Serverless (FaaS)**| Azure Functions | Small pieces of code that only run (and bill) when triggered. | Very Low |

*Example:* If you host a Netflix-style website, the web servers handling user logins and streaming video are your "compute workloads."

---

## 2. What is "Cloud Migration"?
**Migration** is the process of moving those workloads, along with their data and configurations, from one environment to another. Usually, this means moving from a traditional on-premises data center into the public cloud (like Azure).

### The "R's" of Migration Strategies
When planning a migration, architects choose a path for each workload. Here are the most common strategies:

#### 1. Rehost (Lift and Shift)
* **What it is:** Moving a physical or virtual server exactly as-is into an Azure Virtual Machine.
* **Pros:** It's the fastest and easiest way to migrate. No code changes required.
* **Cons:** It doesn't take full advantage of cloud-native features (like auto-scaling or PaaS benefits). You still have to patch the OS.

#### 2. Refactor / Repackage
* **What it is:** Taking an application running on an old VM and putting it into a Docker Container (AKS) or an Azure App Service. 
* **Pros:** Makes the app much easier to scale, deploy, and manage without a full code rewrite.
* **Cons:** Requires some configuration changes and learning new deployment pipelines.

#### 3. Rearchitect (Redesign)
* **What it is:** Completely rewriting the application to use modern cloud-native tools (e.g., breaking a legacy monolithic app into independent microservices or Azure Functions).
* **Pros:** Maximizes cloud agility, performance, and cost-efficiency.
* **Cons:** Very expensive and time-consuming upfront.

#### 4. Rebuild / Replace
* **What it is:** Throwing away the old application entirely. Replacing it with a SaaS (Software as a Service) solution.
* **Example:** Moving from an on-prem custom email server to Microsoft 365 or Google Workspace.

---

## 3. How Terraform Plays a Role
When migrating to Azure, **Terraform** is used to build the *Landing Zone* (the foundation). 

You do not "migrate" using Terraform. Instead:
1. You use Terraform to create the empty Virtual Networks, Subnets, and Virtual Machines in Azure.
2. You use migration tools (like **Azure Migrate**) to copy the actual data and workload from the on-premises servers into the infrastructure that Terraform just built.
