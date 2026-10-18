---
tags: [azure, cli, cheat-sheet, imperative]
source: devopsinsiders/batch-18
created: 2026-06-08
level: beginner
---

# ⌨️ Azure CLI Cheat Sheet

> "The Azure CLI is how you talk to the cloud using your keyboard instead of clicking buttons with your mouse."

---

## 📖 Before You Read
Before looking at these commands, make sure you understand:
- What a **Virtual Machine** and **Resource Group** are — see [[VM]] and [[14-Resource-Groups|Resource-Groups]]
- The difference between **Click-Ops** (using the website) and **Infrastructure as Code** (Terraform).

---

## 🤔 What is it?

The **Azure Command-Line Interface (CLI)** is a small program you install on your laptop. It allows you to open a black text terminal and type commands to create, delete, and manage things in Azure. Every command starts with the letters `az`.

> 💻 **Real-World Analogy:**
> You can order food at a restaurant by pointing at pictures on a menu (Using the Azure Portal website). 
> Or, you can walk straight into the kitchen and shout instructions directly to the chef (Using the Azure CLI). It's much faster, but you have to know exactly what to say!

---

## 🧠 Why do we need it?

If you want to create 1 Virtual Machine, clicking buttons on the website is fine.
If your boss asks you to create 50 Virtual Machines, clicking buttons will take you all day. With the Azure CLI, you can write a tiny script that loops a command 50 times and finishes the job while you get coffee.

*Note: While the CLI is great for quick scripts, professional DevOps teams use **Terraform** to build production infrastructure. We only use the CLI for quick administrative tasks.*

---

## ⚙️ How does it work?

All Azure CLI commands follow a strict logical pattern:
`az <service> <action> --parameters`

For example, to list all your Virtual Machines:
`az vm list`

---

## 💡 Real Example (The Commands)

Here are the most common commands you will use every day.

### 1. Logging In & Basic Setup
| Command | Plain English |
|---|---|
| `az login` | Opens a web browser so you can type your password and connect your terminal to Azure. |
| `az --version` | Checks if the CLI is installed and what version it is. |
| `az account list --output table` | Shows a clean table of all the billing Subscriptions you have access to. |
| `az account set --subscription "MySub"`| Tells Azure "I want to work inside the 'MySub' subscription right now." |

### 2. Managing Resource Groups (Folders)
| Command | Plain English |
|---|---|
| `az group create --name rg-test --location eastus` | Creates a new folder called "rg-test" located in the East US datacenter. |
| `az group list -o table` | Shows you a list of all your folders. |
| `az group delete --name rg-test --yes --no-wait` | **DANGER!** Deletes the folder and everything inside it instantly without asking "Are you sure?" |

### 3. Managing Virtual Machines (Computers)
| Command | Plain English |
|---|---|
| `az vm list -d -o table` | Shows a list of all your computers and whether they are currently turned on or off. |
| `az vm start -g rg-test -n my-vm` | Presses the "Power On" button on the computer named 'my-vm'. |
| `az vm deallocate -g rg-test -n my-vm` | Pulls the plug on the computer so you stop getting billed for it. |

---

## ⚠️ Common Mistakes Beginners Make

1. **Forgetting to Login:** If you open a new terminal window and start typing `az vm list`, it will throw a massive red error. You must run `az login` first!
2. **Missing the `--output table` flag:** If you just run `az group list`, Azure will print hundreds of lines of confusing, raw JSON code to your screen. Adding `-o table` (or `--output table`) formats it into a nice, readable Excel-style grid.
3. **Using `az vm stop` instead of `az vm deallocate`:** If you run `stop`, the VM shuts down, but *you still get billed for the CPU hardware reservation!* You must run `az vm deallocate` to actually stop the billing meter.

---

## 🎯 Key Takeaway
The Azure CLI (`az`) is a fast, imperative way to manage cloud resources directly from your terminal. It's the perfect tool for quickly checking the status of resources, starting/stopping servers, or running small automation scripts.

---

## ❓ Beginner FAQ

**Q1: How do I get help if I forget a command?**
> Just add `--help` to the end of anything! For example, if you know you want to do something with a network but forgot the exact command, type `az network --help` and it will print out a list of all possible network commands!

**Q2: Is the Azure CLI the same as PowerShell?**
> No. Microsoft has two different command-line tools. The Azure CLI (`az`) is written in Python and works exactly the same on Mac, Linux, and Windows. Azure PowerShell uses `Get-AzVM` style commands and is mostly used by heavy Windows administrators.

**Q3: Where do I type these commands?**
> You can download the CLI and type them in Command Prompt (Windows) or Terminal (Mac). Or, you can use the **Azure Cloud Shell**—a free terminal built directly into the Azure website that already has the CLI installed and logged in!
