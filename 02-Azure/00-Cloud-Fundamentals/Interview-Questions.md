---
tags: [interview, cloud-fundamentals, azure]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Cloud Fundamentals: High-Quality Interview Questions

These questions test your deep understanding of Cloud Models and Virtualization. They are designed to mimic real-world scenario questions asked during DevOps or Cloud Engineering interviews.

---

## Question 1: The Shared Responsibility Trap
**Scenario:** 
You have deployed a critical corporate database on an Azure Virtual Machine (IaaS). One night, a massive ransomware attack infects the server, encrypting all your data. Your manager blames Microsoft Azure, stating that because the server is hosted in the cloud, Microsoft is responsible for its security and data integrity.

**Question:** 
Is your manager correct? Based on the Shared Responsibility Model, explain exactly who is responsible for this breach and why.

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Your manager is incorrect. The customer is entirely responsible for this breach.</b><br><br>
Because the database was deployed on an Azure Virtual Machine, it falls under the <b>IaaS (Infrastructure as a Service)</b> model. Under IaaS, Microsoft is only responsible for the physical security of the datacenter, the physical servers, and the virtualization hypervisor layer. <br><br>
Everything "above the hypervisor"—including the guest Operating System, antivirus software, firewall rules, and the data itself—is the absolute responsibility of the customer. The ransomware succeeded because the customer failed to properly secure the OS or manage their security patches.
</details>

---

## Question 2: CapEx vs OpEx Architecture
**Scenario:**
A startup is currently hosting their custom-built web application on physical hardware in a local co-location facility. They experience wild spikes in traffic on weekends, but their servers sit idle at 5% utilization Monday through Friday. The CFO is upset about the massive upfront hardware costs (CapEx) they just paid to buy enough servers to handle the weekend spikes. 

**Question:**
How does migrating to the cloud solve the CFO's financial problem? Use the terms "OpEx" and "Elasticity" in your answer.

<details>
<summary><b>Show Answer</b></summary>
<br>
Migrating to the cloud shifts the financial model from <b>CapEx (Capital Expenditure)</b> to <b>OpEx (Operational Expenditure)</b>. Instead of buying physical servers upfront that sit idle 5 days a week, the startup will only pay for the exact compute resources they consume on a pay-as-you-go basis.<br><br>
Furthermore, by leveraging cloud <b>Elasticity</b> (the ability of a system to automatically scale out by adding servers during weekend spikes, and scale in by removing them during the week), the startup eliminates the need to over-provision hardware. They only pay the high OpEx costs during the weekend when revenue is high, dropping their costs significantly during the week.
</details>

---

## Question 3: Migration Strategies (The "R"s)
**Scenario:**
You are migrating a legacy 15-year-old application to Azure. The application's source code was lost years ago, so no developer can rewrite it. It currently runs on a Windows Server 2012 physical machine. 

**Question:**
Which of the standard cloud migration strategies (Rehost, Replatform, Refactor) is your *only* viable option, and why? What is the common nickname for this strategy?

<details>
<summary><b>Show Answer</b></summary>
<br>
Your only viable option is <b>Rehost</b>, commonly nicknamed <b>"Lift and Shift."</b><br><br>
Because the source code is lost, you cannot <i>Refactor</i> (rewrite the code to be cloud-native). Because it is a legacy app tied to a specific older OS, it is highly likely it will fail to run on a managed PaaS service without code modifications, eliminating <i>Replatform</i>.<br><br>
With a Rehost strategy, you take a carbon-copy image of the physical server's hard drive and run it identically inside an Azure Virtual Machine (IaaS). You carry all the legacy technical debt into the cloud, but the application will function exactly as it did on-premises.
</details>

---

## Question 4: Hypervisor Fundamentals
**Scenario:**
A junior engineer asks you why Azure doesn't use the same "VirtualBox" software they use on their laptop to host the cloud datacenters. 

**Question:**
Explain the difference between a Type 1 and Type 2 hypervisor, and state which type Azure uses.

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Type 2 Hypervisors (Hosted)</b>, like VirtualBox, run as an application on top of an existing host Operating System (like Windows 11). They are very slow because every compute command must be translated through the host OS before reaching the physical hardware.<br><br>
<b>Type 1 Hypervisors (Bare-Metal)</b>, like Microsoft Hyper-V or VMware ESXi, are installed <i>directly</i> onto the blank physical server hardware. There is no host OS. They are incredibly fast, secure, and have near-zero overhead.<br><br>
Azure, like all major cloud providers, exclusively uses <b>Type 1 (Bare-Metal) Hypervisors</b> to achieve the performance and isolation required for enterprise workloads.
</details>
