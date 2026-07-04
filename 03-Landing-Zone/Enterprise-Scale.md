---
tags: [landing-zone, accelerator, enterprise-scale, architecture]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# 🚀 Azure Landing Zone Accelerator (Enterprise-Scale)

> "Instead of forcing you to design a cloud foundation from scratch, Microsoft gives you the exact blueprints they use. The Accelerator is the gold standard cheat code."

---

## 📖 Before You Read
Before you dive into the Accelerator, make sure you understand:
- What a **Landing Zone** is — see [[Introduction]]
- What **CAF** is — see [[CAF-Overview]]

---

## 🤔 What is it?

*Note: This used to be called "Enterprise-Scale Landing Zone," but Microsoft renamed it to the "Azure Landing Zone Accelerator" in 2022. You will hear older engineers use the old name constantly!*

We know from CAF that we must build a Landing Zone before moving to the cloud. But how *exactly* should we build it? How many Management Groups do we need? What IP ranges should the Hub VNet use? What security policies are mandatory?

The **Azure Landing Zone Accelerator** is Microsoft's official, highly opinionated reference architecture. It is a massive set of blueprints and pre-written Terraform code provided by Microsoft that says: "If you want to build a perfect Landing Zone, deploy this exact code."

> 🏡 **Real-World Analogy:**
> If you want to build a house, you could hire an architect to draw custom blueprints from scratch (expensive, high risk of mistakes). 
> Or, you can go online and buy a pre-made, award-winning architectural blueprint package that comes with step-by-step instructions. The **Accelerator** is that pre-made, award-winning blueprint.

---

## 🧠 Why do we need it?

If every company designs their own Landing Zone from scratch, 90% of them will make terrible mistakes. 
- They might put all their resources into one Subscription (which hits an Azure limit and breaks).
- They might forget to turn on Microsoft Defender.
- They might configure their DNS incorrectly.

By using the Accelerator, you are standing on the shoulders of giants. Microsoft interviewed thousands of successful Fortune 500 companies, found out exactly how they built their networks, and packaged those best practices into this Accelerator.

---

## ⚙️ How does it work? (The 4 Design Principles)

The Accelerator is built on four golden rules:

1. **Subscription Democratization:** Don't cram everything into one subscription. Use Subscriptions as folders! Give the HR app its own Subscription, and give the Finance app its own Subscription.
2. **Policy-Driven Governance:** Don't rely on humans to follow the rules. Use **Azure Policy** to physically block engineers from deploying unencrypted hard drives or building servers outside of the approved region.
3. **Single Control and Management Plane:** Keep all your logs in one central Log Analytics Workspace. Don't scatter them across the company.
4. **Application-Centric:** The Landing Zone should be generic enough that it doesn't care if you are deploying 1990s Virtual Machines or modern 2025 Kubernetes clusters. It supports everything equally.

---

## 💡 Real Example (The Terraform Module)

Microsoft doesn't just give you a PDF blueprint; they give you the actual code to build it!

If your boss asks you to build a Landing Zone, you don't have to write 10,000 lines of Terraform. You simply call Microsoft's official open-source Terraform module: `Azure/caf-enterprise-scale`.

```hcl
# This tiny block of code downloads Microsoft's official Accelerator
# and automatically deploys dozens of Management Groups and Policies!

module "enterprise_scale" {
  source  = "Azure/caf-enterprise-scale/azurerm"
  version = "5.0.0"

  root_parent_id   = data.azurerm_client_config.core.tenant_id
  root_id          = "my-company"
  root_name        = "My Awesome Company"
  deploy_core_landing_zones = true
}
```

---

## ⚠️ Common Mistakes Beginners Make

1. **Thinking the Accelerator is "too big" for them:** A startup might look at the massive Management Group structure of the Accelerator and think, "We only have 5 employees, we don't need this." This is a mistake! The Accelerator is designed to scale. It is perfectly fine to deploy it for a small company—it just means when you grow to 500 employees, you won't have to tear down your network and start over.
2. **Ignoring the documentation:** The Terraform module for the Accelerator is incredibly complex. If you just copy-paste code without reading Microsoft's extensive documentation, you will get lost in the configuration files.

---

## 🎯 Key Takeaway
The Azure Landing Zone Accelerator is Microsoft's official, pre-packaged architecture and code module. It allows organizations to instantly deploy a highly secure, scalable, and policy-driven cloud foundation based on industry best practices.

---

## ❓ Beginner FAQ

**Q1: Is the Accelerator free?**
> The blueprints and the Terraform code are 100% free and open-source on GitHub! However, when you run the code, it deploys real Azure resources (like Firewalls and Log Analytics) which will cost you money on your monthly Azure bill.

**Q2: What if I don't know Terraform? Can I still use the Accelerator?**
> Yes! Microsoft provides several ways to deploy it. If you don't know Terraform, you can go to the Azure Portal website, search for "Landing Zone," and deploy the exact same architecture by clicking through a UI wizard (Click-Ops) or using Bicep!
