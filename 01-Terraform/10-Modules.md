---
category: Terraform
tags: [terraform, modules, architecture, dry, enterprise]
type: fundamental
status: active
level: beginner
---

# Terraform Modules

## 📖 Before You Read
- It is highly recommended to understand [[04-Resources]], [[05-Variables]], and [[07-Outputs]] before diving into Modules, as Modules rely heavily on all three!

## 🤔 What is it?
If a Resource is a single building block (like a single brick), and a Variable is the color you paint the brick, a **Module** is the blueprint for an entire room (like a kitchen). 

A Module is a way to package multiple, related resources together into one reusable container. In traditional programming terms, a module is the Terraform equivalent of a "function" or a "class."

**Analogy:** Imagine you work for a company that opens new retail stores. Every single store needs the exact same setup: 1 Cash Register, 2 Security Cameras, and 4 Display Racks. Instead of writing out the individual orders for the register, cameras, and racks every single time you open a new store, you create a "Store Starter Kit." Now, when you need a new store, you just order 1 "Store Starter Kit," and all those items are built automatically. A Module is that "Starter Kit."

## 🧠 Why do we need it?
Without modules, you violate the DRY (Don't Repeat Yourself) principle. 
If an enterprise needs to deploy 20 different databases across 20 different projects, and their security team requires that every database must have logging enabled and public access disabled, you don't want 20 developers trying to write that complex code from scratch. 
Instead, the senior engineers write a `secure_database` module once. The 20 developers just reference that module in 4 lines of code, and it automatically deploys a database perfectly configured to the company's security standards.

## ⚙️ How does it work?
Physically, a module is nothing more than a folder containing `.tf` files. There is no special "module" file type.
There are two main types of modules:
1. **Root Module:** This is simply the folder where you are currently typing `terraform apply`.
2. **Child Modules:** These are external folders (either on your computer, in GitHub, or in the Terraform Registry) that your Root Module "calls" using a `module` block.

To pass data *into* the child module, you use the child module's Variables. To get data *out* of the child module, you use the child module's Outputs.

## 💡 Real Example
Here is how you call a pre-written "Virtual Network" module from another folder.

```hcl
# Instead of using the 'resource' keyword, we use the 'module' keyword
module "secure_vnet" {
  
  # The 'source' tells Terraform exactly where to find the "Starter Kit" folder
  source        = "../../modules/infrastructure/vnet"
  
  # These are the Variables that the child module requires us to fill out
  environment   = "prod"
  vnet_name     = "vnet-hub-prod"
  address_space = ["10.0.0.0/16"]
}

# Now, we want to build a Virtual Machine and put it inside that network!
# We use the Output from the module to get the Subnet ID.
resource "azurerm_linux_virtual_machine" "my_vm" {
  name      = "my-linux-vm"
  # ... other vm settings ...
  
  # Notice the syntax: module.<module_name>.<output_name>
  subnet_id = module.secure_vnet.frontend_subnet_id
}
```

## ⚠️ Common Mistakes Beginners Make
- **Module nesting hell:** Don't put modules inside of modules inside of modules (A calls B, which calls C, which calls D). Keep your architecture flat. Modules should build resources, not other modules.
- **Making modules too small:** Creating a module just to build a single Resource Group defeats the purpose. Modules should represent an architectural pattern (e.g., "A web server AND its database AND its security rules").

## 🎯 Key Takeaway
Modules allow you to package multiple related resources into reusable, standardized blueprints, drastically reducing code repetition and enforcing security best practices across a company.

## ❓ Beginner FAQ

**Q: How do you pass data INTO and OUT OF a child module?**
A: Data goes *into* a module via the `variable` blocks defined inside the module's folder. Data comes *out* of a module via the `output` blocks defined inside the module's folder. The Root module references those outputs using `module.MODULE_NAME.OUTPUT_NAME`.

**Q: What is the Terraform Registry?**
A: It is a public library (`registry.terraform.io`) where companies and the community share pre-written modules. Instead of writing the 500 lines of code required to build a Kubernetes cluster from scratch, you can just `source` the official Azure verified module and deploy it in 10 lines!

**Q: I updated the code inside my local child module folder, but when I run `terraform plan` in the root folder, it doesn't see my changes. Why?**
A: If you are pulling a module from an external source (like Git or the Registry), Terraform caches it during the initial `terraform init`. You must run `terraform init -upgrade` to force Terraform to re-download the latest changes. (Note: If it's a simple local path like `source = "../module"`, it usually picks up changes instantly).

---
**See Also:**
- [[05-Variables]]
- [[07-Outputs]]
- [[06-Resource-Group|Resource Group]]
- [[01-CAF-Mapping|CAF-Mapping]]