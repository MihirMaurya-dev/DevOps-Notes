---
tags: [azure, cloud-fundamentals, hierarchy, auth]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# Azure Fundamentals

## 📖 Before You Read
- No prior knowledge is needed! This is your entry point into the world of Cloud Computing.

## 🤔 What is it?
Microsoft Azure is a **Cloud Computing Platform**. 

Before "The Cloud", companies had to buy physical computers (servers), put them in a cold room in their office building, pay for the electricity, and hire people to fix them when they broke. This is called **On-Premises** (or "On-Prem"). 

**The Cloud** is just someone else's computers. Microsoft has built massive, highly secure warehouses all over the world filled with thousands of servers. They offer to rent you a slice of this computing power over the internet.

**Analogy:** Think of it like a pizza. 
- **On-Premises** is making a pizza from scratch at home. You buy the oven, the dough, the cheese, and pay for the gas. You do all the work.
- **The Cloud** is like ordering a pizza from a restaurant. You don't care how the oven works or who pays the electric bill. You just pay for exactly what you eat, when you want it.

## 🧠 Why do we need it?
1. **No CapEx (Capital Expenditure):** You don't have to spend $100,000 upfront to buy physical servers. You just pay a few dollars a month for what you use (OpEx - Operating Expenditure).
2. **Scalability:** If your website suddenly gets famous and you need 50 more servers, Azure can give them to you in 2 minutes. If you owned the servers yourself, you'd have to order them online and wait 3 weeks for shipping!
3. **High Availability:** If a server breaks in your office, your app is down. Azure has backups of backups. If a server breaks, Microsoft seamlessly moves your app to another server without you even noticing.

## ⚙️ How does it work?
Azure provides thousands of different "services" (rentable items) that fall into a few main categories:
- **Compute:** Virtual Machines (fake computers running inside Microsoft's real computers).
- **Storage:** Hard drives in the sky where you can save files.
- **Networking:** The digital cables and routers that connect your servers to the internet.

You log into a website called the `portal.azure.com`. From there, you click buttons to order what you need. 

**The Azure Hierarchy**
To keep everything organized, Azure uses a strict folder structure:
1. **Tenant (Entra ID):** The very top level. This is your company's identity (e.g., `mycompany.com`). It holds all the user accounts.
2. **Subscription:** The billing boundary. Every resource must live in a subscription, and the subscription has a credit card attached to it.
3. **Resource Group:** A logical folder. You put related things in a Resource Group (e.g., "HR-App-ResourceGroup").
4. **Resources:** The actual items (a Virtual Machine, a Database).

## 💡 Real Example (Concept)
Here is a table comparing the concepts of a physical building to Azure Concepts:

| House Element | IT System Equivalent | Azure Service Equivalent |
|---|---|---|
| Guard at the gate | Security / Firewalls | Azure Firewall / NSG |
| Checking your ID card | Authentication (Who are you?) | Microsoft Entra ID |
| VIP room access list | Authorization (What can you do?) | Role-Based Access Control (RBAC) |
| CCTV Cameras | Monitoring | Azure Monitor / Log Analytics |
| Store Room | Backup | Azure Backup Vault |

## ⚠️ Common Mistakes Beginners Make
- **Confusing Authentication and Authorization:** 
  - *Authentication* is proving who you are (e.g., entering your username and password). 
  - *Authorization* happens AFTER you log in. It determines what you are allowed to touch (e.g., you can read files, but you can't delete them).
- **Forgetting to turn things off:** The cloud is pay-as-you-go. If you spin up a giant $500/month server to test something for an hour, and forget to delete it, you will get a massive bill at the end of the month!

## 🎯 Key Takeaway
Azure is a global network of rentable computers that allows you to pay only for what you use, without worrying about maintaining physical hardware.

## ❓ Beginner FAQ

**Q: What are the other big Cloud Providers besides Azure?**
A: The "Big Three" are Amazon Web Services (AWS), Microsoft Azure, and Google Cloud Platform (GCP). They all do basically the same things, just with different names.

**Q: If my server is in the cloud, where is it physically located?**
A: When you create a resource in Azure, it asks you to pick a "Region." A region is a specific geographical location, like `East US` (Virginia) or `West Europe` (Netherlands). You choose a region close to your customers so the app loads faster!

**Q: Is the cloud secure?**
A: Extremely. Microsoft spends billions on physical and digital security. Your data is encrypted, and Microsoft employees cannot see it. However, it operates on a "Shared Responsibility Model". Microsoft secures the physical building, but if you accidentally set your password to "12345", that's your fault, not theirs!

**Q: How do DevOps engineers interact with Azure?**
A: While beginners use the website portal, DevOps engineers almost exclusively use code (like Terraform) or the Command Line Interface (CLI) to build things automatically.

---
**See Also:**
- [[VNet]]: How networking works in the cloud.
- [[RBAC]]: How authorization works.
- [[Storage-Account]]: Where data is stored.
