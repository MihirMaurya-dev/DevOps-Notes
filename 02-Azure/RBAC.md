---
tags: [azure, rbac, security, entra-id]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# Role-Based Access Control (RBAC) in Azure

## 📖 Before You Read
- Understand the basic Azure Hierarchy (Tenant, Subscription, Resource Group, Resource) from [[Azure-Fundamentals]].

## 🤔 What is it?
**Role-Based Access Control (RBAC)** is the security system Azure uses to manage exactly who is allowed to do what. 

Instead of giving a new employee the master keys to the entire company (which is dangerous!), RBAC lets you give them a specific "Role" that acts like a highly restricted keycard.

**Analogy:** Imagine a bank. 
- The **Bank Teller** role can access the cash register and open customer accounts, but cannot open the main vault.
- The **Bank Manager** role can open the vault and approve large loans, but cannot access the IT server room.
- The **Janitor** role can enter all rooms to clean, but cannot open any safes or computers.

In Azure, RBAC works the exact same way for your cloud resources.

## 🧠 Why do we need it?
Without RBAC, anyone who logs into your Azure account would be able to delete your production databases, turn off your firewalls, or spin up expensive servers. 

The core philosophy of RBAC is the **Principle of Least Privilege (POLP)**: "Give people exactly the access they need to do their job, and nothing more."

## ⚙️ How does it work?
To grant access in Azure, you must combine two things:
1. **The Role (What can they do?):** e.g., "Owner" (can do anything), "Contributor" (can edit things but not give access to others), or "Reader" (can only look).
2. **The Scope (Where can they do it?):** e.g., The entire Subscription, a specific Resource Group, or just one specific Database.

When you combine them, you get an **Assignment**: "I give John the *Contributor* role, but ONLY at the scope of the *HR-App Resource Group*."

### The Two Types of Roles (Crucial Difference)
Azure separates identity (who you are) from resources (what you own).

| Feature | Entra ID Roles (Identity) | Azure Roles (Resources) |
|---|---|---|
| **What it controls** | The company directory: users, passwords, groups, billing. | The cloud stuff: Virtual Machines, Databases, Networks. |
| **Highest Role** | **Global Administrator** | **Owner** |

**WARNING:** A "Global Administrator" is the boss of the company directory, but they do NOT automatically have access to any Virtual Machines! They must explicitly grant themselves an "Azure Role" to touch the cloud stuff.

## 💡 Real Example
Here is the industry standard way of granting access. You almost **never** give access directly to a person (like John). Instead, you use **Groups**.

```hcl
# STEP 1: We create an empty group in Entra ID for the HR App Developers
resource "azuread_group" "hr_devs" {
  display_name     = "sg-hr-app-developers"
  security_enabled = true
}

# STEP 2: We assign the "Contributor" role to the ENTIRE GROUP 
# at the scope of the HR Resource Group.
resource "azurerm_role_assignment" "hr_dev_access" {
  scope                = azurerm_resource_group.hr_app.id
  role_definition_name = "Contributor"
  principal_id         = azuread_group.hr_devs.object_id
}

# STEP 3 (Done manually or via script): We add John to the group.
# John instantly inherits the Contributor access! When John quits, 
# we just remove him from the group, and his access disappears.
```

## ⚠️ Common Mistakes Beginners Make
- **Giving everyone the "Owner" role:** This is the #1 mistake. Owners can do anything, including locking out the real administrators. Only 1 or 2 highly trusted people should be Owners.
- **Direct User Assignment:** Assigning roles directly to `john@company.com` instead of a group. When John leaves the company, you have to hunt down 50 different resources to remove his access. If you used a group, you just remove him from the group once.

## 🎯 Key Takeaway
RBAC is how Azure ensures the Principle of Least Privilege by combining a "Role" (what you can do) with a "Scope" (where you can do it), preferably assigned to Groups rather than individuals.

## ❓ Beginner FAQ

**Q: Who is allowed to assign an Azure role to a new user?**
A: To give someone else a role, you must have the **Owner** role yourself, or a special role called **User Access Administrator**.

**Q: If an intern joins the team just to learn how Azure works, what role should they get?**
A: The **Reader** role at the Resource Group or Subscription level. They can look at all the settings to learn, but they can't break or delete anything.

**Q: What is a "Custom Role"?**
A: If the built-in roles (like Contributor or Reader) don't fit perfectly, you can write a Custom Role. For example, you can create a role that says "Can restart Virtual Machines, but cannot delete them or change their sizes."

**Q: How do you offboard a user cleanly in a Group-Based RBAC model?**
A: You simply remove the user's account from your central Entra ID directory. Because all their access was tied to their membership in groups, their access to all Azure resources is instantly and automatically revoked. No cleanup needed!

---
**See Also:**
- [[Azure-Fundamentals]]
- [[Managed-Identity]]: How machines use RBAC to talk to each other securely.
