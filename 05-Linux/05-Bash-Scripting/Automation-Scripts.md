---
tags: [linux, bash, scripting, automation]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Bash Scripting for Automation

Bash scripting is the glue of DevOps. While tools like Ansible and Terraform handle stateful infrastructure, Bash is used for CI/CD pipelines, bootstrap scripts (cloud-init), and quick operational automation.

## 1. The Safety First Approach (Unofficial Bash Strict Mode)

By default, Bash is very forgiving: if a variable is unset, it evaluates to an empty string. If a command fails, the script just continues to the next line. This is disastrous in DevOps (e.g., `rm -rf /$UNSET_VAR/` could delete the root filesystem).

**ALWAYS start your scripts with:**
```bash
#!/usr/bin/env bash
set -euo pipefail
```

- `set -e`: Exit immediately if any command exits with a non-zero status.
- `set -u`: Treat unset variables as an error and exit immediately.
- `set -o pipefail`: The return value of a pipeline is the status of the last command to exit with a non-zero status, or zero if no command exited with a non-zero status. (e.g., `curl fails | grep something` will fail the script).

## 2. Variables and Arguments

```bash
#!/usr/bin/env bash
set -euo pipefail

# Assigning variables (NO spaces around =)
DB_USER="admin"
BACKUP_DIR="/mnt/backups"

# Command Substitution (assigning the output of a command to a variable)
CURRENT_DATE=$(date +%F)
ARCHIVE_NAME="backup_${CURRENT_DATE}.tar.gz"

# Positional Arguments
# $0 is the script name itself
ENVIRONMENT=$1  # e.g., 'production'
REGION=$2       # e.g., 'eastus'

if [ -z "$ENVIRONMENT" ]; then
    echo "Error: Environment argument is required."
    echo "Usage: $0 <environment> <region>"
    exit 1
fi
```

## 3. Conditionals (if/else)

```bash
# Check if a directory exists
if [ -d "$BACKUP_DIR" ]; then
    echo "Directory exists, proceeding..."
else
    echo "Directory not found, creating it..."
    mkdir -p "$BACKUP_DIR"
fi

# Check if a command succeeded
if systemctl is-active --quiet nginx; then
    echo "NGINX is running."
else
    echo "NGINX is down, attempting restart..."
    systemctl restart nginx
fi
```

## 4. Loops

**For Loops:** Great for iterating over a list or files.
```bash
# Iterate over a list of servers
SERVERS=("web-01" "web-02" "db-01")

for SERVER in "${SERVERS[@]}"; do
    echo "Pinging $SERVER..."
    ping -c 1 "$SERVER"
done
```

**While Loops:** Great for reading files line by line.
```bash
# Read a CSV file line by line
while IFS=',' read -r user role; do
    echo "Creating user $user with role $role"
done < users.csv
```

## 5. Functions and Logging

Keep scripts modular and readable by using functions. Always redirect output clearly.

```bash
#!/usr/bin/env bash
set -euo pipefail

log_info() {
    echo "[INFO] $(date '+%Y-%m-%d %H:%M:%S') - $1"
}

log_error() {
    echo "[ERROR] $(date '+%Y-%m-%d %H:%M:%S') - $1" >&2
}

backup_database() {
    local db_name=$1
    log_info "Starting backup for $db_name"
    
    # Simulate backup command
    if pg_dump "$db_name" > "/tmp/${db_name}.sql"; then
        log_info "Backup successful."
    else
        log_error "Backup failed!"
        exit 1
    fi
}

# Main execution
backup_database "production_db"
```
