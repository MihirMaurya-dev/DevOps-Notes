---
tags: [azure, networking, osi-model, ports, firewall]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🚪 Ports, Protocols, and the OSI Model

> "An IP Address gets you to the right apartment building. A Port gets you into the correct apartment door."

---

## 📖 Before You Read
Before you dive into Ports and Protocols, make sure you understand:
- What an **IP Address** is — see [[02-IP-Addressing-and-CIDR|IP-Addressing-and-CIDR]]
- What a **Firewall (NSG)** is — see [[NSG]]

---

## 1. 🤔 What are Ports and Protocols?

### 🤔 What is it?
When your laptop talks to a server, it's not just a single, solid tube of data. Computers do many things at once. A single web server might be serving a website, receiving emails, and allowing an administrator to remotely control it, all at the exact same time.

- A **Protocol** is the language the computers agree to speak (e.g., HTTP for websites, SMTP for email).
- A **Port** is the specific numbered digital "door" on the server assigned to listen for that language.

> 🏢 **Real-World Analogy:**
> Imagine a server is a giant apartment building. The **IP Address** (`10.0.0.5`) is the street address of the building. 
> 
> The building has 65,535 doors (Ports).
> - Behind Door **80**, a web developer is handing out websites (HTTP Protocol).
> - Behind Door **22**, a security guard is waiting to check IDs and let administrators inside (SSH Protocol).
> 
> If you knock on Door 80 and ask for access to the security cameras, they won't understand you, because Door 80 only speaks "Website."

---

## 2. 🧠 Why do we need it?

If you don't know your ports, you cannot write Firewall rules (Network Security Groups) in Azure. 

When you write Terraform code to secure your cloud, you don't say "Allow Web Traffic." You write code that says: "Allow traffic to Destination Port `80` using Protocol `TCP`." If you get the number wrong, your website is broken.

---

## 3. ⚙️ How does it work? (The OSI Model)

To explain how data travels from a physical cable up into an application, scientists invented the **OSI Model**. It is a 7-layer cake of networking. As a cloud engineer, you only really care about 3 of these layers:

| Layer | Name | What happens here? | Cloud Relevance |
|---|---|---|---|
| **Layer 7** | **Application** | This is the actual software (Chrome, Outlook) speaking the language (HTTP, HTTPS). | Azure Application Gateway (A Layer 7 firewall that can read the website text). |
| **Layer 4** | **Transport** | This is where **Ports** live! It handles making sure the data arrives reliably via TCP or UDP. | Azure Network Security Groups (Layer 4 firewalls that just block doors). |
| **Layer 3** | **Network** | This is where **IP Addresses** and Routing live. | Azure VNets and Route Tables. |

---

## 💡 Real Example (The DevOps Port Cheat Sheet)

If you are going to work in the cloud, you must memorize these specific port numbers. You will type them into Terraform constantly.

| Port Number | Protocol | Plain English Name | What does it do? |
|---|---|---|---|
| **22** | TCP | **SSH** | Used to log into the black command-line terminal of Linux Virtual Machines. |
| **3389** | TCP | **RDP** | Used to log into the graphical desktop of Windows Virtual Machines. |
| **80** | TCP | **HTTP** | Unencrypted, basic web browser traffic. |
| **443** | TCP | **HTTPS** | Secure, encrypted web browser traffic (with the little padlock icon). |
| **53** | UDP/TCP | **DNS** | Translates names to IP addresses (The Phonebook). |
| **1433** | TCP | **SQL Server** | Used when your web app needs to talk to a Microsoft SQL Database. |

---

## ⚠️ Common Mistakes Beginners Make

1. **Opening Port 22 or 3389 to the World:** A beginner will create an Azure NSG and write an inbound rule: "Allow Port 22 from `0.0.0.0/0` (The Internet)." This means anyone on Earth can try to guess your Linux password. Always restrict Port 22 and 3389 to your specific home IP address or a secure corporate VPN!
2. **Confusing TCP and UDP:** 
   - **TCP** requires a guaranteed handshake (like a phone call). If a piece of data gets lost, it asks for it to be resent. Used for Websites and Databases.
   - **UDP** just blasts data as fast as possible without checking if it arrived (like a radio broadcast). Used for live video streaming or gaming. Don't select UDP in your firewall if your web app requires TCP!

---

## 🎯 Key Takeaway
Ports (numbered doors) and Protocols (languages) operate at Layer 4 and Layer 7 of the OSI Model. They are the fundamental variables you use when writing Firewall and Security Group rules in Azure. Memorize Port 80, 443, 22, and 3389!

---

## ❓ Beginner FAQ

**Q1: Can I change a port? Like, can I run a website on Port 9999 instead of 80?**
> Yes! Port 80 is just the "default standard" that everyone agreed upon. You can configure your software to listen on any port between 1 and 65,535. However, if you use Port 9999, your users will have to type `http://www.google.com:9999` to reach it!

**Q2: What is a "Stateful" firewall?**
> Azure NSGs are stateful. This means if you create a rule allowing traffic *IN* on Port 80, the firewall remembers the connection and automatically allows the response traffic *OUT*. You don't have to write two separate rules!
