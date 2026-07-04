---
category: Terraform
tags: [terraform, resources, hcl, fundamentals, architecture]
type: fundamental
status: active
level: beginner
---

# Terraform Resources

## 📖 Before You Read
- Make sure you understand what a Provider is by reading [[03-Providers]].

## 🤔 What is it?
If you think of Terraform code as a sentence, **Resources** are the "nouns." A resource block describes the actual, physical thing you are trying to build in the cloud. It could be a Virtual Machine, a Database, a Network, or a Security Group. Everything else in Terraform exists purely to support your Resources.

**Analogy:** Imagine writing a shopping list for a grocery store. The "Resource" is the actual item you want: "1 Gallon of Whole Milk" or "3 Red Apples". The shopping list guarantees you walk out of the store with those specific physical objects.

## 🧠 Why do we need it?
Without resources, Terraform wouldn't build anything! The resource block is the core instruction that tells the Provider (the translator) exactly what buttons to push in the cloud to create the object. It defines the size, the name, the location, and all the properties of the cloud object.

## ⚙️ How does it work?
A resource block is written in three distinct parts:
1. **The Keyword:** Always the word `resource` (tells Terraform what kind of block this is).
2. **The Resource Type:** This is defined by the Provider. It is the exact technical name of the cloud object (e.g., `azurerm_virtual_network`). The prefix (`azurerm_`) tells Terraform which provider to use.
3. **The Local Name:** This is a name you make up! It is used *only* inside your Terraform code so you can refer to this specific resource later. It is NOT the name the resource will have in Azure.

When combined, the Type and the Local Name create a unique ID for that object, called the **Resource Address** (e.g., `azurerm_virtual_network.main`).

## 💡 Real Example
Here is how you build a Virtual Network in Azure using a resource block.

```hcl
# 1. 'resource' is the keyword
# 2. 'azurerm_virtual_network' is the Type (provided by Azure)
# 3. 'main' is the Local Name (chosen by us)
resource "azurerm_virtual_network" "main" {
  
  # Everything inside the curly braces are the "arguments" or settings for the resource

  # This is the actual name the network will have in the Azure Cloud Portal
  name                = "vnet-hub-eus"
  
  # The geographic location (data center)
  location            = "eastus"
  
  # The Resource Group folder it belongs to
  resource_group_name = "rg-hub-eus"
  
  # The IP address range for the network
  address_space       = ["10.0.0.0/16"]
}
```

## ⚠️ Common Mistakes Beginners Make
- **Changing the Local Name later:** If you deploy the code above, and next week you change the Local Name from `"main"` to `"primary"`, Terraform will think you deleted the old resource and added a brand new one! It will delete your existing Virtual Network and build a new one. Be very careful changing Local Names after a deployment.
- **Confusing Local Name with Azure Name:** Beginners often think the Local Name (`"main"`) is what the resource will be called in the Azure portal. It's not! The `name = "vnet-hub-eus"` argument inside the block dictates the real-world name.

## 🎯 Key Takeaway
The `resource` block is the fundamental building block of Terraform, used to define the actual infrastructure objects you want to create in the cloud.

## ❓ Beginner FAQ

**Q: How do I know what arguments (like `address_space`) a resource requires?**
A: You look at the official Terraform Registry documentation for the Provider. The documentation will list every single argument a resource requires, along with optional arguments you can use.

**Q: What is a Dependency Graph?**
A: If you tell Terraform to build a Database, but the Database needs to go inside a Virtual Network, Terraform is smart enough to figure out the order! It automatically builds the Virtual Network *first*, and then builds the Database. You don't have to write complex order-of-operations scripts.

**Q: I have a Database that needs a special security role to be created *before* it starts, but Terraform tries to build them at the same time. How do I fix it?**
A: You can force an order by adding the `depends_on` meta-argument inside your resource block. It explicitly tells Terraform, "Wait for the security role to finish before you start building me."

**Q: Can I build 50 identical servers using one resource block?**
A: Yes! You don't need to copy and paste the block 50 times. You can use special looping arguments like `count` or `for_each` inside the resource block to deploy multiple copies at once.

---
**See Also:**
- [[03-Providers]]
- [[01-Terraform/Resource-Library/Resource-Group|Resource Group]]
- [[13-Loops-Conditionals]]
- [[14-Lifecycle]]