---
tags: [azure, storage, data]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# ☁️ Azure Storage Accounts — The Beginner's Complete Guide

---

## 📖 Before You Read

Make sure you're comfortable with these ideas first:
- What "the cloud" means (hint: it's just someone else's computer/server)
- What a file is (documents, images, videos, etc.)
- Basic idea of what [[01-Azure|Azure]] is — Microsoft's cloud platform
- What a database is at a high level (a place to store organized data)

If you don't know these yet, no worries — this guide will explain everything as we go!

---

## 🤔 What is Azure Storage? — Plain English + Real-World Analogy

Imagine you're moving to a new city and you need a place to store your belongings. You rent a **storage unit facility**. Inside this facility, you can rent different types of units:

- A **big open warehouse** for large, bulky items (like furniture or boxes)
- A **filing cabinet room** for important documents
- A **message board** where delivery people can leave notes
- A **small locker** for quick-access items

**Azure Storage Account** is exactly like that storage facility — but for your **digital data** on Microsoft's cloud (Azure). Instead of physical items, you store digital things like files, images, videos, messages, and database records.

> 🧠 **In simple words:** An Azure Storage Account is a container (think: a rental unit) in the cloud where you can store different types of digital data. It's managed by Microsoft, so you don't need to buy hard drives or maintain servers yourself.

---

## 🧠 Why Do We Need It? — The Problem It Solves

Imagine you're building a website or an app. Your app needs to:
- Store **profile pictures** that users upload
- Keep **log files** recording what happened in your app
- Send **messages** between different parts of your app
- Store **user records** in a fast, flexible way

You could buy your own physical hard drives and servers, but that means:
- 💸 High upfront cost
- 🔧 You have to maintain them yourself
- 😟 If the hard drive fails, your data is lost
- 🌍 Difficult to access from anywhere in the world

**Azure Storage** solves all of this:
- ✅ Pay only for what you use (no upfront cost)
- ✅ Microsoft handles maintenance, backups, and hardware
- ✅ Your data is automatically copied multiple times (so it's safe)
- ✅ Accessible from anywhere in the world via the internet

---

## ⚙️ How Does It Work? — The Technical Explanation

When you create an **Azure Storage Account**, you're essentially registering a named "home base" in Microsoft's cloud. Think of it like signing a lease for your storage facility — you give it a unique name, choose a region (e.g., "East US" or "West Europe"), and pick your settings.

Inside that Storage Account, you can use **four different types of storage services** — like choosing different rooms inside your facility:

---

## 🗂️ Core Services Inside a Storage Account

### 1. 🗃️ Blob Storage (Object Storage)

🤔 **What is it?**

"Blob" stands for **Binary Large Object**. Don't let the name scare you! It basically means: a **chunk of unstructured data** — things that don't fit neatly into rows and columns like a spreadsheet.

Think of Blob Storage like a **giant filing cabinet** where you can throw in anything — documents, images, videos, audio files, backups — without needing to organize them in a specific format.

🧠 **Why do we need it?**

Your web app needs to store user-uploaded photos. You can't put a photo inside a regular database easily. Blob Storage is the perfect place — it can hold files of any type, any size.

⚙️ **How does it work?**

You create a **container** (like a folder) inside your Storage Account, then upload **blobs** (files) into it. Each blob gets a unique URL so you can access it from anywhere.

💡 **Real Example — Uploading a file using Azure CLI:**

```bash
# az = Azure CLI (Command Line Interface, a tool you type commands into)
# storage blob upload = the command to upload a file to blob storage
# --account-name = the name of YOUR storage account
# --container-name = the folder inside your storage account
# --name = what you want to call this file in the cloud
# --file = the actual file on your computer you want to upload

az storage blob upload \
  --account-name mystorageaccount123 \
  --container-name profile-pictures \
  --name user-john-photo.jpg \
  --file C:\Users\John\photo.jpg
```

**Common uses:** Profile pictures, website images, video files, database backups, log archives.

---

### 2. 📁 Azure Files (File Shares)

🤔 **What is it?**

Azure Files is like a **shared network drive** in the cloud. Imagine the shared drive at an office where multiple computers can all access the same folder — Azure Files does exactly this, but over the internet.

It uses protocols called **SMB** (Server Message Block — a standard for sharing files between computers on a network, the same thing Windows uses for shared folders) and **NFS** (Network File System — similar but used more on Linux systems).

🧠 **Why do we need it?**

Great for **lift-and-shift** scenarios. "Lift-and-shift" means taking an old application that's currently running on a physical server in your office and moving it to the cloud without rewriting it. If the old app expects to read files from a shared folder (like `\\server\files\`), Azure Files can act as that shared folder in the cloud.

💡 **Real Example:**
```
Old setup:  Your app reads from \\office-server\shared-files\config.xml
New setup:  Your app reads from \\mystorageaccount.file.core.windows.net\shared-files\config.xml
           (same path format, same protocol — the app doesn't even know it moved to the cloud!)
```

---

### 3. 📬 Queue Storage (Message Queue)

🤔 **What is it?**

Think of Queue Storage like a **to-do list** or a **ticket queue at a government office**. People take a number (put a message in the queue) and wait for an officer (a background worker) to call their number (process the message).

🧠 **Why do we need it?**

Imagine your e-commerce website. When a customer places an order:
1. The website (frontend) **puts a message** in the queue: "Order #1234 placed"
2. The warehouse system **reads the message** from the queue and processes it
3. The email system **reads another message** and sends a confirmation email

This is called **decoupling** — the website doesn't need to wait for the warehouse system to respond. They work independently through the message queue. If the warehouse system is slow or down, the messages just wait in the queue safely.

⚙️ **How does it work?**

Messages are stored in the queue. A background worker (like a separate program or Azure Function) checks the queue, picks up messages, processes them, and deletes them from the queue once done.

---

### 4. 📋 Table Storage (NoSQL Key-Value Store)

🤔 **What is it?**

Table Storage is a **simple, fast database** that stores data as key-value pairs. Think of it like a giant Excel spreadsheet — each row has a unique key and various columns of data.

"NoSQL" means it's **Not Only SQL** — unlike traditional databases (SQL databases) that require rigid tables with fixed columns, NoSQL storage is flexible and can store rows with different structures.

🧠 **Why do we need it?**

Great for **semi-structured data** that you need to store and retrieve quickly. For example: storing user session data, device telemetry (readings from IoT sensors), or app configuration settings.

> ⚠️ **Note for beginners:** Table Storage is simple and cheap but has limited query abilities. For complex applications, Azure Cosmos DB is often better.

---

## 📦 Storage Account Types (Kinds)

When you create a Storage Account, you choose a "kind" — think of it like choosing what **type of storage facility** you want to rent:

### 1. 🌟 General-Purpose v2 (StorageV2) — **The One You Should Use**

- The **standard, modern, recommended type**
- Supports ALL four services: Blob, Files, Queue, and Table
- Has both **Standard** and **Premium** performance options
  - **Standard** = uses regular hard drives (HDDs) — slower but cheaper
  - **Premium** = uses solid-state drives (SSDs) — faster but costs more

> 🎯 **Rule of thumb:** Unless you have a specific reason not to, always choose General-Purpose v2.

### 2. 🏚️ General-Purpose v1 (Storage) — **Legacy, Don't Use**

- The old version — exists only for backward compatibility
- **Avoid for new deployments** — it doesn't support all modern features

### 3. ⚡ BlockBlobStorage — **Premium Blobs Only**

- Only for Blob Storage, with Premium (SSD) performance
- Use when you need: **very high transaction rates** (millions of reads/writes per second) or **very low latency** (data must be returned in milliseconds)
- Example use case: streaming video platforms, gaming leaderboards

### 4. 🚀 FileStorage — **Premium Files Only**

- Only for Azure Files, with Premium (SSD) performance
- Use for enterprise applications that need **high-performance file sharing**
- Example: Large financial firms running complex applications that need fast shared file access

---

## 🌡️ Access Tiers (Blob Storage Only)

This is one of the smartest features of Azure Blob Storage! You can choose **how "hot" (frequently accessed) your data is**, and Azure charges you accordingly.

Think of it like **parking spots** near a building:
- A spot right at the entrance costs the most but is most convenient (Hot)
- A spot further away costs less but takes longer to walk (Cool/Cold)
- A spot in a distant parking garage costs the least but you need to call a shuttle (Archive — "rehydration")

### 🔴 Hot Tier — Frequently Accessed Data
- **Use when:** Data is accessed daily or very often
- **Cost:** Highest storage cost per GB, but cheapest access cost per operation
- **Examples:** Your app's current profile pictures, active documents, website images

### 🔵 Cool Tier — Infrequently Accessed Data
- **Use when:** Data won't be accessed for at least **30 days**
- **Cost:** Lower storage cost, higher access cost
- **Examples:** Short-term backups, older invoices, monthly reports

### 🟢 Cold Tier — Rarely Accessed Data
- **Use when:** Data won't be accessed for at least **90 days**
- **Cost:** Even lower storage cost, even higher access cost
- **Examples:** Compliance data, old project archives

### ⚫ Archive Tier — Almost Never Accessed Data
- **Use when:** Data won't be accessed for at least **180 days**
- **Cost:** Cheapest storage cost, highest access cost
- **Special rule:** Data is **offline** — before you can read it, you must "rehydrate" it (move it back to Hot or Cool tier), which can take **hours**!
- **Examples:** Legal records that must be kept for 7 years, old security camera footage

💡 **Real Example — Setting a blob's access tier using Terraform (Infrastructure as Code):**

```hcl
# This is Terraform code — a tool to create Azure resources by writing code
# instead of clicking around in the Azure Portal (website)

resource "azurerm_storage_blob" "example" {
  name                   = "my-backup-file.zip"          # Name of the file in the cloud
  storage_account_name   = "mystorageaccount"            # Which storage account to use
  storage_container_name = "backups"                     # Which container (folder) to use
  type                   = "Block"                       # Type of blob (Block is most common)
  access_tier            = "Cool"                        # We rarely access backups, so use Cool tier
}
```

---

## 🛡️ Redundancy Options — How Your Data Is Protected

"Redundancy" means making **extra copies of your data** so that if something goes wrong (a disk fails, a building burns down, an earthquake hits), your data is still safe.

Think of it like **making photocopies of important documents**. The more copies you make in different places, the safer your document is.

### 📍 LRS — Locally Redundant Storage
- **Full name:** Locally Redundant Storage
- **What it does:** Makes **3 copies** of your data, all within the **same physical building** (data center)
- **Protection against:** Hardware failures (one disk dying)
- **Does NOT protect against:** Entire data center disasters (fire, flood, power outage)
- **Cost:** Cheapest option
- **Use for:** Non-critical development/test data

```
[Your Data] → Copy 1 (Rack A) → Copy 2 (Rack B) → Copy 3 (Rack C)
               All in the same building!
```

### 🏙️ ZRS — Zone-Redundant Storage
- **Full name:** Zone-Redundant Storage
- **What it does:** Makes **3 copies** across **3 different Availability Zones** (separate physical buildings with independent power, cooling, and networking) in the same region
- **Protection against:** An entire data center going down
- **Cost:** More than LRS

```
[Your Data] → Copy 1 (Building A, Zone 1)
            → Copy 2 (Building B, Zone 2)  ← Different buildings in same city
            → Copy 3 (Building C, Zone 3)
```

### 🌍 GRS — Geo-Redundant Storage
- **Full name:** Geo-Redundant Storage
- **What it does:** LRS in your primary region PLUS an **asynchronous copy** to a secondary region hundreds of miles away
- "Asynchronous" means the copy happens in the background — there's a small delay, but it doesn't slow down your app
- **Protection against:** Entire regional disasters (hurricanes, widespread power failures)
- **Cost:** More expensive

```
[Your Data] → LRS copies in East US (primary)
            → LRS copies in West US (secondary, updated in background)
```

### 🌐 GZRS — Geo-Zone-Redundant Storage
- **Full name:** Geo-Zone-Redundant Storage
- **What it does:** Combines ZRS (3 zones in primary region) + GRS (copy to secondary region)
- **The most protected option** — survives zone failures AND regional disasters
- **Cost:** Most expensive
- **Use for:** Mission-critical production data where downtime is unacceptable

---

## 🔒 Security Best Practices

> ⚠️ **This section is important!** Misconfigured storage accounts are one of the most common causes of data breaches. Many companies have accidentally exposed customer data by not following these rules.

### 1. ❌ Never Allow Public Access

```hcl
# In Terraform (Infrastructure as Code):
resource "azurerm_storage_account" "example" {
  name                     = "mystorageaccount"
  resource_group_name      = "my-resource-group"
  location                 = "East US"
  account_tier             = "Standard"
  account_replication_type = "GRS"

  # This line is CRITICAL — it prevents anyone on the internet from
  # reading your blobs without proper authentication
  allow_nested_items_to_be_public = false  # ✅ ALWAYS set this to false!
}
```

### 2. 🔐 Enforce HTTPS

**HTTPS** (HyperText Transfer Protocol Secure) encrypts data while it travels between your app and Azure. Without it, anyone who intercepts your network traffic can read your data in plain text.

```hcl
  https_traffic_only_enabled = true  # ✅ Forces all connections to use encryption
```

### 3. 🪪 Use Managed Identities Instead of Connection Strings

A **connection string** is like a password embedded in your code. If someone steals your code (e.g., from GitHub), they get your password too.

A **Managed Identity** (see [[08-Managed-Identity|Managed-Identity]]) is like a **ID badge** — your app proves its identity automatically through Azure, no passwords needed.

```
❌ BAD:  connectionString = "DefaultEndpointsProtocol=https;AccountName=foo;AccountKey=abc123..."
✅ GOOD: Use Managed Identity — no secrets in code at all!
```

### 4. 🔒 Restrict Network Access

Instead of letting the entire internet reach your storage, restrict it to specific **Virtual Networks** (VNets — private networks inside Azure, like your office's private network):

- **Service Endpoints:** Keeps traffic on Azure's private network (faster, more secure)
- **Private Endpoints:** Gives your storage account a private IP address — only reachable from within your VNet

---

## ⚠️ Common Mistakes Beginners Make

1. **Leaving public access ON** — This is dangerous. Always set `allowBlobPublicAccess = false` unless you intentionally want public files (like a public image CDN).

2. **Using LRS for production data** — LRS is fine for development, but for real user data, use at least GRS. A single data center failure shouldn't wipe out your users' data.

3. **Using connection strings in code** — Never paste your storage account key directly into your application code or config files. Use Managed Identities or Azure Key Vault (see [[Key-Vault]]).

4. **Forgetting to set access tiers** — Storing terabytes of old backup data in Hot tier when it should be Archive tier wastes a lot of money.

5. **Not planning IP address space for Azure Files** — Running out of IP addresses in your network when connecting Azure Files can cause connectivity problems.

---

## 🎯 Key Takeaway

An Azure Storage Account is your **one-stop cloud storage facility**, offering four types of storage (Blob for files, Files for shared drives, Queue for messages, Table for NoSQL data). Always use General-Purpose v2, choose the right redundancy for how critical your data is, pick the right access tier to save money, and **never expose your data publicly or hardcode connection strings**.

---

## ❓ Beginner FAQ

**Q1: What's the difference between Blob Storage and Azure Files?**
> Blob Storage is for storing individual files that your app reads/writes programmatically (like uploading photos). Azure Files is for shared drives that multiple computers/VMs need to "mount" (connect to) like a network drive, the same way you'd map a drive letter in Windows.

**Q2: Can I change the access tier later?**
> Yes! You can move blobs between Hot, Cool, Cold, and Archive tiers at any time. However, moving FROM Archive requires "rehydration" which can take up to 15 hours. You can also set lifecycle policies to automatically move data to cheaper tiers after a set number of days.

**Q3: What happens if I forget to set redundancy and my data center goes down?**
> With LRS, if the entire physical data center has a disaster, you could lose your data. This is why for production (real user-facing) data, GRS or GZRS is strongly recommended. You cannot easily change redundancy after the fact without copying data.

**Q4: How much does Azure Storage cost?**
> It varies by region, tier, and redundancy. As a rough guide: Hot tier LRS is around $0.02 per GB per month. Archive tier is as low as $0.001 per GB per month. You also pay for operations (reads/writes). Use the [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) for exact estimates.

**Q5: Is a Storage Account the same as a database?**
> Not quite. Table Storage is a very basic NoSQL database. For full database features (complex queries, relationships, transactions), use Azure SQL Database or Azure Cosmos DB instead. Storage Accounts are best for files, messages, and simple key-value data.
