---
category: Azure-Networking
tags: [azure, networking, nsg, security, firewall, terraform, implementation]
type: implementation
status: active
level: beginner
---

# 🛡️ Network Security Groups (NSGs) — Beginner's Guide

> "An NSG is the bouncer at your cloud nightclub — it checks everyone at the door and decides who gets in and who doesn't."

---

## 📖 Before You Read

This note will make much more sense if you first understand:
- What a network is (computers talking to each other) — see [[VNet]]
- What IP addresses and ports are (how computers identify each other and what "door" to knock on) — see [[03-Ports-and-Protocols|Ports-and-Protocols]]
- What a Subnet is (a section of a network) — see [[04-Subnets|Subnets]]
- Basic Azure resource concepts — see [[01-Azure-Fundamentals|Azure-Fundamentals]]

---

## 1. 🤔 What is a Network Security Group (NSG)?

### 🤔 What is it?

An **NSG (Network Security Group)** is basically a **firewall** (a security filter) for your Azure network. It's a list of rules that says:

- "Allow traffic from the internet to reach port 80" (so web browsers can access your website)
- "Deny ALL traffic from the internet trying to reach port 3306" (block public access to your database)
- "Allow traffic from the web server subnet to reach the database subnet on port 3306" (only YOUR web server can access the database)

> 🏢 **Real-World Analogy:**
> Imagine a large office building with different floors:
> - **Ground floor** = Reception area (public-facing, anyone can enter)
> - **5th floor** = Engineering department (only employees allowed)
> - **Basement** = Server room (only senior IT staff allowed)
>
> The **NSG is like the security rules enforced at each floor's elevator or door**. The security guard (NSG) has a checklist: "Who is knocking? Where did they come from? Which door are they trying to use? Are they on the allowed list?" Based on the checklist, they either let the person through or turn them away.

---

### 🧠 Why do we need NSGs?

Without NSGs, **every resource in your VNet would be open to every other resource** — and potentially to the entire internet. This would be catastrophic.

For example, imagine you have:
- A web server that should be accessible from the internet (ports 80 and 443)
- An application server that should only be reachable from the web server
- A database that should only be reachable from the application server

Without NSGs, someone on the internet could try to directly connect to your database — which is a massive security risk. NSGs let you enforce these boundaries.

---

### ⚙️ How does it work?

An NSG contains **Security Rules**. Each rule is defined by a **5-tuple** — five pieces of information that together describe what traffic the rule applies to:

| 5-Tuple Component | What it is | Example |
|---|---|---|
| **Source IP/Range** | Where is the traffic coming FROM? | `0.0.0.0/0` = anywhere on the internet |
| **Source Port** | Which port is the sender using? | `*` = any port |
| **Destination IP/Range** | Where is the traffic going TO? | `10.0.2.0/24` = a specific subnet |
| **Destination Port** | Which port is the receiver listening on? | `8080` = a specific application port |
| **Protocol** | What type of traffic? | `TCP`, `UDP`, or `*` (any) |

> 💡 **What is a Port?**
> A port is like a specific "door number" on a computer. Just like an apartment building has one street address but many individual apartment doors, a computer has one IP address but thousands of ports.
>
> Common port numbers you'll see:
> - Port **80** = HTTP (regular, unencrypted web traffic)
> - Port **443** = HTTPS (secure, encrypted web traffic — what your browser uses for `https://` websites)
> - Port **22** = SSH (Secure Shell — how Linux admins connect to a server remotely, like remote desktop but for command-line)
> - Port **3389** = RDP (Remote Desktop Protocol — how Windows admins remotely control a Windows server)
> - Port **3306** = MySQL database
> - Port **1433** = Microsoft SQL Server database

---

## 2. 🏢 Stateful Evaluation — The "Smart Memory" Feature

### 🤔 What is "Stateful"?

NSGs are described as **stateful** firewalls. This sounds technical but it's actually a very helpful feature.

> 📬 **Real-World Analogy:**
> Imagine you send a letter to a friend. Your friend writes back. The building security guard (NSG) knows you sent the original letter, so when your friend's reply arrives, they automatically let it through — they don't need a separate rule saying "allow incoming mail from your friend."

In technical terms: if an **inbound (incoming) packet** is allowed by an NSG rule, the **return outbound (outgoing) traffic** is **automatically allowed** — you don't need to write a separate rule for it.

Compare this to a **stateless** firewall, which would require explicit rules for BOTH directions of traffic. Stateful is much simpler.

---

## 3. 📍 Where Can You Attach an NSG?

NSGs can be attached to:

1. **A Subnet** — The NSG filters ALL traffic going in and out of the entire subnet. This is the **recommended enterprise approach** — you protect an entire zone at once.

2. **A Network Interface Card (NIC)** — A NIC is the "network adapter" for a specific VM (Virtual Machine). Attaching an NSG at the NIC level means it only applies to that one specific VM.

> 🏢 **Analogy:**
> - Attaching to a **Subnet** = Posting a security guard at the **elevator on each floor** — everyone on that floor is protected.
> - Attaching to a **NIC** = Posting a guard at the **door of one specific office** — only that one office is protected.
>
> For enterprise security, you secure at the **Subnet** level (the floor) as your baseline.

---

## 4. 🎛️ Default Rules — What Azure Creates Automatically

Every NSG comes with **built-in default rules** that Azure creates automatically. You cannot delete these, but your custom rules can override them (by using a lower priority number).

| Rule Name | Priority | What it does |
|---|---|---|
| `AllowVnetInBound` | 65000 | Allows all traffic between resources within the same VNet |
| `AllowAzureLoadBalancerInBound` | 65001 | Allows Azure's load balancer to health-check your VMs |
| `DenyAllInBound` | 65500 | Denies all other inbound traffic (the final catch-all block) |

> 💡 **Priority** = Lower number = Higher priority = Rule is checked first. Think of it like a numbered queue — Rule 100 is checked before Rule 200, which is checked before Rule 65500.

---

## 5. 🏗️ Tier Isolation — Separating Your Application Layers

A best practice in cloud security is **separating your application into security zones** called "tiers." Each tier only talks to the next tier — never directly to unrelated tiers.

For a typical 3-tier web application:

```text
[Internet] 
    |
    | (ports 80, 443 allowed)
    v
[Frontend Subnet]  -- web servers, load balancers
    |
    | (only port 8080 from Frontend allowed)
    v
[Backend Subnet]   -- application/API servers
    |
    | (only port 3306 from Backend allowed)
    v
[Database Subnet]  -- databases
```

NSG rules to implement this:

| Subnet | What Traffic To Allow | What To Block |
|---|---|---|
| **Frontend** | Internet → port 80 and 443 | Everything else |
| **Backend** | Frontend subnet → port 8080 only | Internet and anything else |
| **Database** | Backend subnet → port 3306 (MySQL) or 1433 (SQL Server) only | Everything else, especially internet |

---

## 6. 💡 Real Example — Terraform Code to Create a Backend NSG

```hcl
# ---- LOCALS: Define our security rules in a reusable variable ----
# "locals" is like a notepad where you write things down to use later.
# Here, we're defining all the rules for our backend subnet NSG.
locals {
  backend_security_rules = {
    
    # Rule name: allow HTTP traffic from the frontend subnet to the backend
    "allow_http_from_frontend" = {
      
      # Priority 100: This rule is checked first (lower number = higher priority)
      priority = 100
      
      # "Inbound" = this rule applies to traffic COMING IN to the backend subnet
      direction = "Inbound"
      
      # "Allow" = let this traffic through (alternative would be "Deny")
      access = "Allow"
      
      # "Tcp" = this rule only applies to TCP traffic (most web/app traffic uses TCP)
      # TCP = Transmission Control Protocol — the reliable, connection-oriented protocol
      # Think of TCP like a phone call: you establish a connection, talk, then hang up.
      protocol = "Tcp"
      
      # "*" for source port means: any port on the sender's side is fine
      # (The source port is usually randomly assigned by the OS anyway)
      source_port_range = "*"
      
      # Only allow traffic headed for port 8080 (our backend app's listening port)
      destination_port_range = "8080"
      
      # Only allow traffic coming FROM the frontend subnet (10.0.1.0/24)
      # Meaning: ONLY the frontend web servers can reach the backend — not random internet traffic
      source_address_prefix = "10.0.1.0/24"
      
      # This traffic is going TO the backend subnet (10.0.2.0/24)
      destination_address_prefix = "10.0.2.0/24"
    }
  }
}

# ---- RESOURCE 1: Create the Network Security Group ----
resource "azurerm_network_security_group" "backend_nsg" {
  
  # Name includes the environment (dev/staging/prod) for easy identification
  # var.environment is a variable — think of it as a placeholder filled in later
  name                = "nsg-backend-${var.environment}-eus"
  location            = var.location
  resource_group_name = var.resource_group_name

  # "dynamic" block is a Terraform trick to generate repeating blocks automatically
  # Instead of writing one "security_rule" block per rule (tedious for 20+ rules),
  # we loop through our local.backend_security_rules map and create them all at once.
  dynamic "security_rule" {
    
    # Loop through each rule we defined in locals above
    for_each = local.backend_security_rules
    
    content {
      # security_rule.key = the rule name (e.g., "allow_http_from_frontend")
      name = security_rule.key
      
      # security_rule.value.priority = the priority from the map above (100)
      priority  = security_rule.value.priority
      direction = security_rule.value.direction
      access    = security_rule.value.access
      protocol  = security_rule.value.protocol
      
      source_port_range          = security_rule.value.source_port_range
      destination_port_range     = security_rule.value.destination_port_range
      source_address_prefix      = security_rule.value.source_address_prefix
      destination_address_prefix = security_rule.value.destination_address_prefix
    }
  }

  tags = var.tags
}

# ---- RESOURCE 2: Associate the NSG with the Backend Subnet ----
# Creating the NSG is not enough — you must ATTACH it to a subnet.
# Think of it like writing a security policy on paper vs. actually posting
# the security guard at the door. This step "posts the guard."
resource "azurerm_subnet_network_security_group_association" "backend_assoc" {
  
  # The ID of the backend subnet (comes from another Terraform resource or variable)
  subnet_id = var.backend_subnet_id
  
  # The ID of the NSG we just created above
  network_security_group_id = azurerm_network_security_group.backend_nsg.id
}
```

---

## 7. 🔒 Security Considerations & Advanced Concepts

### ☠️ The "Any-Any" Danger — NEVER Do This in Production

```hcl
# DANGEROUS - DO NOT USE IN PRODUCTION
source_address_prefix      = "*"   # Allows traffic from ANYWHERE on the internet
destination_port_range     = "22"  # On SSH port (lets anyone SSH into your server)
```

This would let anyone in the world try to SSH (remotely connect) to your server. Hackers run automated bots that continuously scan the internet for exactly this kind of open port. You will get hacked.

**Always restrict admin ports (22 for Linux SSH, 3389 for Windows RDP) to specific IP addresses** — ideally just your company's office IP address.

---

### 🏷️ Application Security Groups (ASGs) — Rules Based on Identity, Not IP

Normally, NSG rules use IP addresses to identify sources and destinations. But IP addresses can change when VMs are recreated or scaled.

An **ASG (Application Security Group)** is a way to tag VMs with a label (like "WebServer" or "DatabaseServer") and write NSG rules using those labels instead of IP addresses.

> 🧑‍💼 **Analogy:** Instead of saying "Allow person at desk number 42 to enter the server room," you say "Allow anyone with the 'IT Admin' badge to enter the server room." If the IT admin changes desks, the rule still works — you don't need to update it.

---

### 📊 NSG Flow Logs — Recording What Happens

**NSG Flow Logs** record all traffic decisions made by your NSG — which connections were allowed, which were denied, from where, to where. In production environments (real live systems), you should ALWAYS enable these for:
- **Security auditing** (who tried to connect and was blocked?)
- **Troubleshooting** (why can't my app talk to the database?)
- **Compliance** (many industries require you to prove you're monitoring network traffic)

---

## ⚠️ Common Mistakes Beginners Make

1. **Opening port 22 or 3389 to `0.0.0.0/0` (the whole internet)** — This is the #1 way systems get hacked. Never allow SSH or RDP from any IP. Use Azure Bastion (a secure browser-based way to connect to VMs) instead. See [[01-Azure-Fundamentals|Azure-Fundamentals]].

2. **Forgetting to associate the NSG to a subnet** — Creating an NSG in Terraform does nothing on its own. You MUST create the association resource too (the `azurerm_subnet_network_security_group_association`), otherwise your NSG rules are never enforced.

3. **Priority conflicts** — If you have Rule 100 that allows traffic and Rule 200 that denies the same traffic, the Allow wins (because 100 comes first). Always think carefully about your rule priorities.

4. **Thinking stateful means you don't need any outbound rules** — Stateful means RETURN traffic is automatic. But if your application needs to INITIATE outbound traffic (e.g., a server calling an external API), you still need an outbound rule for that.

5. **Blocking Azure infrastructure traffic** — Azure's default rules allow the load balancer to health-check your VMs. If you accidentally override these with a Deny-All, Azure can't check if your VMs are healthy.

---

## 🎯 Key Takeaway
An NSG is a stateful firewall for your Azure network. It uses rules (based on source IP, destination IP, port, and protocol) to allow or deny traffic. Attach it at the subnet level, never open admin ports to the internet, and always enable Flow Logs in production.

---

## 🔗 Related Notes
- [[03-Ports-and-Protocols|Ports-and-Protocols]]
- [[04-Resources]]
- [[20-Loops-Conditionals|13-Loops-Conditionals]]
- [[04-Subnets|Subnets]]
- [[02-Zero-Trust-Basics|Zero-Trust-Basics]]
- [[VNet]]

---

## ❓ Beginner FAQ

**Q1: What's the difference between an NSG and a Firewall?**
> An **NSG** is a simple Layer 4 filter — it can only look at IP addresses and port numbers. It can't inspect the actual content of the traffic. An **Azure Firewall** is a more intelligent, full-featured network security service that can inspect traffic content, filter domain names (URLs), detect threats, etc. NSGs are free and simple; Azure Firewall is powerful but costs money. Use NSGs for basic subnet-level filtering, Azure Firewall for enterprise-grade security.

**Q2: What does "Layer 4" mean?**
> Networks operate in "layers" — like a stack of different systems that each handle a part of communication. **Layer 4** is the "Transport Layer" — it deals with how data is broken into packets and delivered (TCP and UDP). An NSG filters at this level, meaning it can see IP addresses and ports but can't read the actual content of the message. Think of it like a security guard who can see *who* is entering and *which door* they're using, but can't read their mail.

**Q3: If my NSG has a Deny rule and an Allow rule for the same traffic, which wins?**
> **The rule with the LOWER priority number wins** because it's evaluated first. Priority 100 is evaluated before Priority 200. So if Priority 100 = Allow and Priority 200 = Deny for the same traffic, the Allow rule at 100 wins and traffic is allowed through.

**Q4: Do I need an NSG on every single subnet?**
> Best practice says yes — every subnet that contains resources should have an NSG attached. Even if the NSG only has the default rules, explicitly associating one ensures you have a foundation to add rules later. The goal is "least privilege" — by default block everything, then explicitly allow only what's needed.

**Q5: Can one NSG be associated with multiple subnets?**
> Yes! You can create one NSG and associate it with multiple subnets. This is useful when multiple subnets need the same security rules. For example, you might have a "common baseline NSG" applied to all subnets, and then additional specific NSGs for each subnet on top.