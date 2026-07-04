---
tags: [cloud, models, iaas, paas, saas, capex, opex]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# ☁️ Cloud Service Models (IaaS, PaaS, SaaS)

> "The cloud is just someone else's computer. The service model determines how much of that computer you are responsible for maintaining."

---

## 📖 Before You Read
Before diving into cloud models, make sure you understand:
- The fundamental definition of **The Cloud** — see [[Azure-Fundamentals]]

---

## 🤔 What is it?

When you use the cloud, you are renting technology from Microsoft instead of buying it yourself. But *what* exactly are you renting? Are you renting an empty computer? Or are you renting a fully functioning software application?

To answer this, the cloud is split into three main Service Models: **IaaS, PaaS, and SaaS.**

> 🍕 **Real-World Analogy (The Pizza Model):**
> **On-Premises:** You make pizza at home. You buy the oven, gas, dough, cheese, and you do all the cooking and cleaning. (You manage EVERYTHING).
> 
> **IaaS (Infrastructure as a Service):** "Take and Bake." You go to the store and buy a pre-made raw pizza. You still have to bring it home, use your own oven, and pay for the gas to cook it. (Microsoft gives you the computer, but you have to install the OS and software).
> 
> **PaaS (Platform as a Service):** "Delivery." You order a pizza to your house. You don't care about the oven or the ingredients, but you still have to provide the dining table and plates to eat it on. (Microsoft provides the computer and the OS. You just bring your application code).
> 
> **SaaS (Software as a Service):** "Dining Out." You go to a restaurant. They cook the pizza, serve it on their plates, and clean up afterward. You just eat. (Microsoft provides the fully working software, like Office 365 or Gmail. You just log in and use it).

---

## 🧠 Why do we need it?

We need these different models to solve different business problems.

If you are a startup that just wants an email system, you don't want to build an email server from scratch. You want **SaaS** (like Microsoft Outlook).
If you have a team of developers who want to write a custom Python website, but they hate doing Windows Updates, you want **PaaS** (like Azure App Services).
If you have a 20-year-old legacy database that requires a very specific version of Windows Server 2008, you need full control. You want **IaaS** (like Azure Virtual Machines).

---

## ⚙️ How does it work? (The Shared Responsibility Model)

When you move to the cloud, you don't get to fire your entire IT team. Instead, you enter a "Shared Responsibility Model" with Microsoft. 

| What needs managing? | IaaS | PaaS | SaaS |
| :--- | :--- | :--- | :--- |
| **Data & Access** | 🧑 You | 🧑 You | 🧑 You |
| **Application Code** | 🧑 You | 🧑 You | ☁️ Microsoft |
| **Operating System** | 🧑 You | ☁️ Microsoft | ☁️ Microsoft |
| **Physical Servers** | ☁️ Microsoft | ☁️ Microsoft | ☁️ Microsoft |

*Note: No matter which model you pick, YOU are always responsible for your own data and passwords!*

### The Money: CapEx vs OpEx
- **CapEx (Capital Expenditure):** The old way. You spend $10,000 today to buy a physical server, and you hope it lasts for 5 years.
- **OpEx (Operational Expenditure):** The cloud way. You don't buy anything. You just pay a $50 "utility bill" at the end of the month for the compute power you actually used.

---

## 💡 Real Example

Imagine you work for a company that is migrating to Azure.
- **Project A:** A custom .NET web application. You choose **PaaS** (Azure App Service). You just upload the code, and Azure runs it. You never have to install Windows Updates.
- **Project B:** An old SAP system that requires root administrator access to the server. You choose **IaaS** (Azure Virtual Machine). You have full control, but you are responsible for installing the antivirus and patching the OS.
- **Project C:** The HR department needs a new payroll system. Instead of building it, you choose **SaaS** (Workday). You just pay a monthly fee per employee.

---

## ⚠️ Common Mistakes Beginners Make

1. **Assuming the Cloud fixes bad code:** Moving a slow, badly written application from an On-Premises server to an IaaS Virtual Machine will just result in a slow, badly written application in the cloud. 
2. **Assuming Microsoft backs up everything:** In IaaS, Microsoft guarantees the physical server won't catch fire. They do *not* guarantee you won't accidentally delete your own database. You are still responsible for setting up your own backups!

---

## 🎯 Key Takeaway
The cloud offers three main models: IaaS (renting raw hardware), PaaS (renting a platform to run code), and SaaS (renting finished software). The more you move toward SaaS, the less control you have, but the less maintenance you have to do!

---

## ❓ Beginner FAQ

**Q1: What is "Serverless"?**
> Serverless is a specialized version of PaaS. In normal PaaS, you pay a fixed monthly fee for the platform. In Serverless (like Azure Functions), you literally only pay for the exact milliseconds your code is actively running!

**Q2: Which model is the most expensive?**
> Usually, IaaS is the most expensive because you are paying for the Virtual Machine to be turned on 24/7, even if nobody is using your application at 3:00 AM. PaaS and Serverless can often be much cheaper because they scale down automatically.