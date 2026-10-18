---
tags: [interview, cloud-fundamentals, azure]
source: devopsinsiders/batch-18
created: 2026-06-08
level: intermediate
---

# 🎯 Cloud Fundamentals: Interview Questions

These questions cover the essentials of Cloud Computing, structured from basic concepts to advanced architecture and real-world scenarios. 

---

## Part 1: Basics

### Q1: What is Cloud Computing?
<details>
<summary><b>Show Answer</b></summary>
<br>
Cloud computing is the delivery of computing services (like servers, storage, databases, and software) over the internet. Instead of buying and owning physical computers, you rent access to them from a cloud provider.
</details>

### Q2: What is IaaS (Infrastructure as a Service)?
<details>
<summary><b>Show Answer</b></summary>
<br>
IaaS provides basic computing infrastructure over the internet. You rent virtual machines, storage, and networks. You have full control over the Operating System (OS) and your applications, but you must manage and update them yourself.
</details>

### Q3: What is PaaS (Platform as a Service)?
<details>
<summary><b>Show Answer</b></summary>
<br>
PaaS provides a ready-to-use platform for developers to build and host applications. The cloud provider manages the underlying servers, OS, and networking, so you only focus on writing your code and managing your data.
</details>

### Q4: What is SaaS (Software as a Service)?
<details>
<summary><b>Show Answer</b></summary>
<br>
SaaS delivers fully functional software over the internet. You just use the application (like webmail or Microsoft 365) in your web browser. The provider manages everything, including the app, data, servers, and security.
</details>

### Q5: What is a Public Cloud?
<details>
<summary><b>Show Answer</b></summary>
<br>
A public cloud is owned and operated by a third-party cloud provider (like Microsoft Azure or AWS). Resources are shared among multiple customers over the public internet.
</details>

### Q6: What is a Private Cloud?
<details>
<summary><b>Show Answer</b></summary>
<br>
A private cloud is a cloud environment dedicated entirely to one single organization. It can be located in the company's own physical data center or hosted by a third party, offering more control and privacy.
</details>

### Q7: What is a Hybrid Cloud?
<details>
<summary><b>Show Answer</b></summary>
<br>
A hybrid cloud combines both public and private clouds. They are connected together, allowing data and applications to move between them for greater flexibility.
</details>

### Q8: What is CapEx (Capital Expenditure)?
<details>
<summary><b>Show Answer</b></summary>
<br>
CapEx refers to spending money upfront to buy physical assets, like servers or a data center. It requires a large initial investment before you can use the resources.
</details>

### Q9: What is OpEx (Operational Expenditure)?
<details>
<summary><b>Show Answer</b></summary>
<br>
OpEx refers to spending money on a day-to-day or month-to-month basis for running operations. In cloud computing, this is the "pay-as-you-go" model where you only pay for what you use, avoiding upfront costs.
</details>

### Q10: What is the main benefit of moving from CapEx to OpEx?
<details>
<summary><b>Show Answer</b></summary>
<br>
You avoid huge upfront costs and the risk of buying too many or too few servers. With OpEx, your costs align exactly with your actual usage.
</details>

---

## Part 2: Advanced

### Q11: What is the Shared Responsibility Model?
<details>
<summary><b>Show Answer</b></summary>
<br>
It is a framework that divides security and management tasks between the cloud provider and the customer. The provider secures the physical data center, while the customer is responsible for securing their data and access.
</details>

### Q12: Under IaaS, what is the customer responsible for?
<details>
<summary><b>Show Answer</b></summary>
<br>
In IaaS, the customer manages the OS, applications, data, runtime, and middleware. The provider only manages the physical servers, storage, and networking.
</details>

### Q13: Under SaaS, what is the cloud provider responsible for?
<details>
<summary><b>Show Answer</b></summary>
<br>
In SaaS, the cloud provider manages almost everything: the physical hardware, OS, networking, application software, and databases. The customer only manages their user access and specific data.
</details>

### Q14: What is a Cloud Region?
<details>
<summary><b>Show Answer</b></summary>
<br>
A Region is a specific geographical location in the world (like "East US" or "West Europe") that contains one or more data centers connected by a fast network.
</details>

### Q15: What is an Availability Zone (AZ)?
<details>
<summary><b>Show Answer</b></summary>
<br>
An Availability Zone is a physically separate data center within a Region. Each AZ has its own independent power, cooling, and network to protect against local failures.
</details>

### Q16: Why should you use multiple Availability Zones?
<details>
<summary><b>Show Answer</b></summary>
<br>
If one data center goes down due to a power outage or fire, your application will continue to run from another Availability Zone, ensuring high uptime.
</details>

### Q17: What is Scalability?
<details>
<summary><b>Show Answer</b></summary>
<br>
Scalability is the ability of a system to handle growing amounts of work by adding more resources. This can be adding more power to an existing server (Scaling Up) or adding more servers (Scaling Out).
</details>

### Q18: What is Elasticity in Cloud Computing?
<details>
<summary><b>Show Answer</b></summary>
<br>
Elasticity is the system's ability to automatically and dynamically scale resources up or down based on real-time demand, ensuring you don't overpay for unused resources.
</details>

### Q19: What is High Availability (HA)?
<details>
<summary><b>Show Answer</b></summary>
<br>
High Availability ensures that an application remains accessible and online for a long period of time, minimizing downtime through backups and redundant systems.
</details>

### Q20: What is Fault Tolerance?
<details>
<summary><b>Show Answer</b></summary>
<br>
Fault tolerance goes a step further than High Availability. It ensures that if a hardware or software component fails, the system continues to operate with exactly zero downtime or data loss.
</details>

---

## Part 3: Scenario-Based

### Q21: The Database Choice
**Scenario:** You need to migrate a database to the cloud. You want full control over the database version and the underlying operating system. Which cloud model should you choose?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>IaaS.</b> Because you want control over the OS and the exact database version, renting a Virtual Machine (IaaS) gives you the necessary administrative access.
</details>

### Q22: The Startup Budget
**Scenario:** A startup is launching a new app but has very little money to buy physical servers upfront. Which financial model does the cloud offer to help them?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>OpEx (Operational Expenditure).</b> The cloud allows them to pay-as-they-go with no upfront CapEx, meaning they only pay for the resources their app actually consumes.
</details>

### Q23: The Viral Traffic Spike
**Scenario:** An online store is featured on a popular TV show, causing web traffic to suddenly increase by 500%. After the show, traffic returns to normal. What cloud characteristic handles this smoothly?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Elasticity.</b> The cloud environment can automatically scale out to handle the massive traffic spike and scale back in when it's over, keeping performance high and costs low.
</details>

### Q24: The Security Blame Game
**Scenario:** A hacker gains access to your Azure Virtual Machine because you left port 22 open to the public internet. Who is responsible for this breach according to the Shared Responsibility Model?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>The Customer.</b> In IaaS, Azure secures the physical infrastructure, but securing the network ports and OS is entirely the customer's responsibility.
</details>

### Q25: The Hybrid Solution
**Scenario:** A bank wants to move its customer-facing web app to the cloud for scalability, but strict laws require them to keep all customer financial records in their own local data center. What cloud deployment model is this?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Hybrid Cloud.</b> They are combining a Public Cloud (for the web app) with their Private Data Center (for the sensitive records) and connecting them together.
</details>

### Q26: The Data Center Fire
**Scenario:** A severe flood destroys an entire Azure data center building. However, your application does not go down. What architecture design made this possible?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Availability Zones.</b> You likely deployed your application across multiple Availability Zones. When one data center flooded, the application continued running in another physically separate building.
</details>

### Q27: Developer Focus
**Scenario:** Your software team wants to build a new web application quickly. They do not want to manage operating system updates, security patches, or server maintenance. Which cloud service model is best?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>PaaS (Platform as a Service).</b> With PaaS, the cloud provider handles the servers and OS, allowing the developers to focus purely on writing code.
</details>

### Q28: Scaling Direction
**Scenario:** Your database is struggling to process complex queries, so you upgrade the server by adding more CPU and RAM. What type of scaling is this?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Scaling Up (Vertical Scaling).</b> You are increasing the power of a single existing resource rather than adding more resources.
</details>

### Q29: Using Software
**Scenario:** Your company decides to use Microsoft 365 for email and document sharing. No one in your company installs servers or updates the email software. What cloud model is this?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>SaaS (Software as a Service).</b> You are consuming a fully finished product hosted and managed entirely by the provider.
</details>

### Q30: Ensuring Zero Downtime
**Scenario:** An application is designed so that if any server component fails, a backup component instantly takes over without the user ever noticing a disruption. What is this concept called?
<details>
<summary><b>Show Answer</b></summary>
<br>
<b>Fault Tolerance.</b> It ensures the system can continue operating without any interruption or downtime even when parts fail.
</details>
