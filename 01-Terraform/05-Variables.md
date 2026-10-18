---
category: Terraform
tags: [terraform, variables, hcl, fundamentals, parameters]
type: fundamental
status: active
level: beginner
---

# Terraform Variables (Input Variables)

## 📖 Before You Read
- Understand how resources are built from [[04-Resources]].

## 🤔 What is it?
If `resource` blocks are the "nouns" (the physical objects you are building), **Variables** are the "adjectives" (how you describe those objects). 

Variables act as "fill-in-the-blank" placeholders for your code. Instead of permanently hardcoding a value like `"East US"` directly into your Virtual Machine resource block, you use a variable. Later, you can tell Terraform to replace that variable with whatever value you want without actually changing the original code.

**Analogy:** Imagine a generic contract template. Instead of writing a new contract from scratch for every client, you have blanks for "[CLIENT NAME]" and "[DATE]". In Terraform, Variables are the blanks in your infrastructure contract.

## 🧠 Why do we need it?
The most important rule in coding is "DRY" (Don't Repeat Yourself). 
If a company has a "Development" environment, a "Testing" environment, and a "Production" environment, they don't want to copy and paste the entire Terraform codebase three times. With variables, they write the code ONCE. Then, they just pass in different variable files: "deploy this code with the *dev* variables," or "deploy this same code with the *prod* variables."

## ⚙️ How does it work?
Using variables is a two-step process:
1. **Declare the Variable:** You tell Terraform, "Hey, I'm going to need a piece of information called `environment`." You do this in a `variable` block.
2. **Provide the Value:** When you actually run `terraform apply`, you provide the real answer (e.g., `"dev"` or `"prod"`).

## 📨 How Variables are Passed (Order of Precedence)

There are exactly **6 ways** to pass a variable value to Terraform. 

If you accidentally provide the *same* variable in two different places (like putting `region="eastus"` in a file, but typing `region="westus"` in the terminal), Terraform uses a strict **Order of Precedence** to decide who wins. 

Here are the 6 ways, ranked from Lowest Priority (1) to Highest Priority (6):

### 1. Interactive Prompt (Absolute Lowest Priority)
If you don't provide a value using any of the methods below, Terraform will actually pause execution in your terminal and ask you to type the answer manually. This is terrible for automation!

### 2. Environment Variables
If you export a variable on your computer's operating system starting with `TF_VAR_`, Terraform will automatically find it. This is useful for passing secret passwords in a CI/CD pipeline so they don't get saved to a file.
- *Example (Linux/Mac):* `export TF_VAR_environment="dev"`
- *Example (Windows PowerShell):* `$env:TF_VAR_environment="dev"`

### 3. The `terraform.tfvars` File
This is the standard, most common method. You create a plain text file named exactly `terraform.tfvars` in the same folder as your code. Terraform loads it automatically.
- *Example inside `terraform.tfvars`:*
  ```hcl
  environment = "prod"
  ```

### 4. The `terraform.tfvars.json` File
Exactly the same as above, but formatted as pure JSON. This is rarely written by humans. It is used when an external script or machine generates the variables automatically.
- *Example:* `{"environment": "prod"}`

### 5. The `*.auto.tfvars` or `*.auto.tfvars.json` Files
If you have a massive project, you might want to split your variables into multiple files. Any file ending in `.auto.tfvars` is automatically loaded, and it will *override* whatever is written in the standard `terraform.tfvars` file!
- *Example filename:* `database.auto.tfvars`

### 6. Command-Line Flags (`-var` or `-var-file`) (Highest Priority)
If you type the value directly into the terminal when you run the apply command, it overrides absolutely everything else. This is the ultimate trump card, great for quick testing!
- *Example passing a direct value:* `terraform apply -var="environment=qa"`
- *Example passing a custom file:* `terraform apply -var-file="custom_testing.tfvars"`

## 🗂️ Variable Types (All Types & How to Use Them)

Terraform enforces strict data typing to ensure you pass the correct data structure into your modules. They are broken down into Primitives, Collections, and Structural types.

### 1. Primitive Types (The Basics)
- **`string`**: Plain text.
  - *Usage:* `variable "region" { type = string }`
  - *Value:* `"eastus"`
- **`number`**: Numeric values (whole numbers or decimals).
  - *Usage:* `variable "cpu_count" { type = number }`
  - *Value:* `4`
- **`bool`**: True or false values.
  - *Usage:* `variable "enable_backups" { type = bool }`
  - *Value:* `true`

### 2. Collection Types (Grouping Multiple Values)
- **`list`**: An ordered array of values of the *same* type. You access them by their position number (e.g., `var.vnet_address_space[0]`).
  - *Usage:* `variable "vnet_address_space" { type = list(string) }`
  - *Value:* `["10.0.0.0/16", "10.1.0.0/16"]`
- **`set`**: Like a list, but the values are unordered and must be *unique*. Used heavily with `for_each` loops.
  - *Usage:* `variable "admin_users" { type = set(string) }`
  - *Value:* `["alice", "bob"]`
- **`map`**: A collection of key-value pairs of the *same* type. You access them by their key (e.g., `var.tags["environment"]`).
  - *Usage:* `variable "tags" { type = map(string) }`
  - *Value:* `{ environment = "prod", department = "finance" }`

### 3. Structural Types (Complex Configurations)
- **`object`**: A complex structure where you define specific keys, and each key can be a *different* type! This is perfect for defining strict, structured configurations (like the settings for a specific VM).
  - *Usage:* 
    ```hcl
    variable "database_config" {
      type = object({
        name        = string
        size_gb     = number
        is_multi_az = bool
      })
    }
    ```
  - *Value:* `{ name = "sql-prod", size_gb = 100, is_multi_az = true }`
- **`tuple`**: Like a list, but each element in the sequence can have a *different* type (very rarely used in standard Terraform).
  - *Usage:* `variable "server_data" { type = tuple([string, number, bool]) }`
  - *Value:* `["web-server", 8080, true]`

## 💡 Real Example
Here is how you declare a variable and use it to build a secure database.

```hcl
# 1. We declare a variable for the environment
variable "environment" {
  type        = string  # It must be text
  description = "The deployment environment (dev, qa, prod)"
  
  # We can add validation guardrails to prevent mistakes!
  validation {
    condition     = contains(["dev", "qa", "prod"], var.environment)
    error_message = "Environment must be dev, qa, or prod."
  }
}

# 2. We declare a variable for a sensitive password
variable "db_password" {
  type        = string
  description = "Administrator password for the database."
  # This tells Terraform NOT to print the password to the terminal screen
  sensitive   = true
}

# 3. We use the variables in our resource block!
resource "azurerm_sql_server" "main" {
  name                         = "sql-server-${var.environment}" # Evaluates to "sql-server-prod"
  resource_group_name          = "rg-database"
  location                     = "eastus"
  version                      = "12.0"
  administrator_login          = "adminuser"
  administrator_login_password = var.db_password # Injects the password securely
}
```

## ⚠️ Common Mistakes Beginners Make
- **Putting passwords in the `.tfvars` file:** Never write a real password inside your `terraform.tfvars` file if you are going to save that file to Git! Everyone in your company will be able to see it. Passwords should be passed dynamically from secure tools like Azure Key Vault.
- **Confusing Variables with Locals:** Variables are inputs provided from the *outside*. Locals (which we learn about next) are calculations made on the *inside*.

## 🎯 Key Takeaway
Variables allow you to customize your deployments without changing the underlying code, making your infrastructure highly reusable across different environments.

## ❓ Beginner FAQ

**Q: What is the difference between a Variable and a Local?**
A: A Variable is an external input (like a parameter you give to a function). A Local is an internal constant or calculation that cannot be overridden from the outside. 

**Q: How do you securely handle a database password in Terraform?**
A: First, add `sensitive = true` to the variable block so it doesn't print to the console. Second, NEVER hardcode the password in a `.tfvars` file that gets committed to version control. Have your CI/CD pipeline inject it secretly during deployment.

**Q: If I have `location="eastus"` written in my `terraform.tfvars` file, but I type `terraform apply -var="location=westus"` in the terminal, where does the server get built?**
A: It gets built in `westus`. The command-line flags have the highest priority and will always override file settings.

**Q: What are variable "types"?**
A: Types tell Terraform what kind of data to expect. Common types are `string` (text), `number` (digits), `bool` (true/false), and `list` (an array of items).

---
**See Also:**
- [[06-Locals]]
- [[06-Resource-Group|Resource Group]]
- [[05-Terraform-Pipeline|Terraform-Pipeline]]
- [[Key-Vault]]