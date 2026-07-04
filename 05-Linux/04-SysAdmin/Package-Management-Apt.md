---
tags: [linux, apt, package-management, ubuntu]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# Package Management: APT

Different Linux distributions use different package managers to install, update, and remove software. 
- **Debian/Ubuntu:** Uses `apt` (Advanced Package Tool) which interacts with `.deb` packages.
- **RHEL/CentOS/Amazon Linux:** Uses `yum` or `dnf` which interact with `.rpm` packages.
- **Alpine (Docker):** Uses `apk`.

We focus on `apt` as Ubuntu is the most common cloud deployment environment.

## The Core Concept
When you install software on Linux, you aren't downloading `.exe` files from random websites. You use `apt` to fetch pre-compiled, verified software from central **repositories** maintained by Canonical (Ubuntu's parent company) or third parties.

The list of repositories your system knows about is stored in `/etc/apt/sources.list` and files inside `/etc/apt/sources.list.d/`.

## Essential Commands

### 1. `sudo apt update`
> [!important]
> **Always run this first.** This command does *not* upgrade your software. It simply downloads the latest package lists from the repositories. It updates the local database so your system knows what the newest versions are.

### 2. `sudo apt upgrade`
Upgrades all currently installed software packages to their newest versions based on the updated package lists.

### 3. `sudo apt install <package>`
Installs a new package and automatically resolves and installs any required dependencies.
- Example: `sudo apt install nginx -y` (The `-y` flag answers "yes" to prompts, crucial for automation scripts).

### 4. `sudo apt remove <package>`
Removes the software but leaves its configuration files behind (in case you want to reinstall later).

### 5. `sudo apt purge <package>`
Completely removes the software *and* deletes all its configuration files. Use this for a clean slate.

### 6. `sudo apt autoremove`
Removes orphaned dependencies. If you installed an app that required 5 libraries, and later you removed the app, those 5 libraries are still sitting there wasting space. This command cleans them up.
