---
tags: [interview, networking, azure]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Networking Fundamentals: High-Quality Interview Questions

These questions test your deep understanding of IP Addressing, Routing, DNS, and Azure Networking. They are designed to mimic real-world scenario questions asked during DevOps or Cloud Engineering interviews.

---

## Question 1: The CIDR Math Failure
**Scenario:** 
A junior engineer is writing Terraform code to deploy a highly available Kubernetes cluster. They create a subnet and assign it the CIDR block `10.0.5.0/29`. When the pipeline runs, it instantly fails, stating there are not enough IP addresses available to boot the cluster nodes. The junior engineer is confused, stating "A /29 gives us 8 IP addresses, and we only asked for 2 nodes!"

**Question:** 
Explain to the junior engineer why the deployment failed, detailing exactly how Azure handles IP addresses within a subnet.

<details>
<summary><b>Show Answer</b></summary>
<br>
While the junior engineer is mathematically correct that a `/29` block contains 8 IP addresses, they forgot about <b>Azure's Reserved IP rule</b>. <br><br>
Azure permanently reserves exactly <b>5 IP addresses</b> in every single subnet you create (The Network Address, the Default Gateway, the Azure DNS mapping, a future reserved IP, and the Broadcast Address). <br><br>
Therefore, out of the 8 IPs in a `/29`, 5 are stolen by Azure, leaving only <b>3 usable IP addresses</b>. Because Kubernetes requires several IPs for its control plane and internal routing before it even boots the 2 worker nodes, 3 usable IPs is vastly insufficient, causing the deployment to crash.
</details>

---

## Question 2: Peering Transitivity
**Scenario:**
You have three Virtual Networks: VNet A (Web), VNet B (Hub/Firewall), and VNet C (Database). 
VNet A is successfully peered to VNet B. 
VNet C is successfully peered to VNet B. 

**Question:**
Can a web server in VNet A ping the database in VNet C directly? If not, what two networking configurations must you implement to make this work?

<details>
<summary><b>Show Answer</b></summary>
<br>
<b>No, the web server cannot ping the database.</b> Azure VNet Peering is <b>NOT transitive</b> by default. Traffic cannot "pass through" VNet B automatically.<br><br>
To fix this and establish a Hub & Spoke architecture, you must implement two things:<br>
1. <b>A Router/Firewall:</b> You must deploy a Virtual Appliance (like Azure Firewall) into VNet B to act as a traffic router.<br>
2. <b>User Defined Routes (UDRs):</b> You must create a Route Table, attach it to VNet A, and create a UDR telling traffic destined for VNet C to route to the Firewall's IP in VNet B. You must do the same in reverse for VNet C.
</details>

---

## Question 3: The OSI Model and NSGs
**Scenario:**
An application developer complains that they cannot reach their new Web API over the internet. You inspect the Azure Network Security Group (NSG) attached to their VM's subnet. You see an inbound rule allowing traffic on `Port 80`, Protocol `UDP`. 

**Question:**
At what layer of the OSI model does the NSG operate? Why is the developer's Web API failing to load, and how do you fix the rule?

<details>
<summary><b>Show Answer</b></summary>
<br>
An NSG operates primarily at <b>Layer 4 (The Transport Layer)</b> of the OSI model.<br><br>
The developer's Web API is failing because standard web traffic (HTTP) requires the <b>TCP (Transmission Control Protocol)</b>, not UDP. TCP establishes a reliable, guaranteed handshake, which is mandatory for loading web pages. UDP is a connectionless protocol used for things like video streaming.<br><br>
To fix the issue, you must modify the NSG rule to Allow Port `80`, Protocol `TCP`.
</details>

---

## Question 4: DNS Resolution Boundaries
**Scenario:**
You have a Virtual Machine deployed in an Azure VNet. When you type `ping db-server` into the terminal of that VM, it successfully finds the database VM in the same VNet because Azure's default DNS (`168.63.129.16`) resolves the name. 
However, your company connects an On-Premises office to this VNet via a VPN. When a user in the physical office types `ping db-server`, it says "Host Not Found."

**Question:**
Why can't the on-premises user resolve the name, and what Azure service should you implement to fix this?

<details>
<summary><b>Show Answer</b></summary>
<br>
Azure's default, magic DNS server (`168.63.129.16`) is strictly localized. It can only resolve hostnames for VMs that live <b>inside that exact same VNet</b>. It cannot answer DNS queries coming from across a VPN or from peered VNets.<br><br>
To fix this, you must implement <b>Custom DNS</b> (such as an active directory domain controller) or deploy an <b>Azure Private DNS Resolver</b>. This creates an inbound endpoint in your VNet that the on-premises office can forward their DNS queries to, allowing them to finally resolve the Azure hostnames.
</details>
