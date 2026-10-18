---
tags: [bash, scripting, linux, variables]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# Bash Scripting: Variables and Logic

Bash is the default command-line shell for most Linux distributions. Bash scripting allows you to write programs to automate OS-level tasks.

## The Shebang
Every bash script must start with a shebang. This tells the kernel which interpreter should execute the file.
```bash
#!/bin/bash
```

## Variables

Bash variables are untyped and generally treated as strings.
- **Assignment:** No spaces around the equals sign!
  - Correct: `NAME="DevOps"`
  - Wrong: `NAME = "DevOps"`
- **Referencing:** Use the `$` symbol.
  - `echo "Hello, $NAME"`

### Environment Variables
Variables that are exported and made available to child processes.
- `export API_KEY="xyz123"`
- Often stored in `~/.bashrc` or passed directly to Docker containers/Pipelines.

### Special Variables
- `$0`: The name of the script itself.
- `$1, $2, ...`: The first, second, etc., arguments passed to the script.
- `$#`: The total number of arguments passed.
- `$?`: The exit status of the *last* command run (0 means success, anything else means failure). Very important for error checking.

## Conditional Logic (`if` statements)

Bash uses square brackets `[ ]` for evaluation. Spaces inside the brackets are **mandatory**.

```bash
#!/bin/bash

# Check if a file exists
if [ -f "/etc/nginx/nginx.conf" ]; then
    echo "Nginx config found."
else
    echo "Config missing!"
fi

# Compare strings
if [ "$1" == "prod" ]; then
    echo "Deploying to production"
fi

# Compare numbers (-eq, -ne, -lt, -gt)
if [ $# -lt 2 ]; then
    echo "Error: This script requires at least 2 arguments."
    exit 1
fi
```

## Loops

### `for` loop
Used to iterate over a list of items.
```bash
for SERVER in "web1" "web2" "db1"; do
    echo "Pinging $SERVER..."
    ping -c 1 $SERVER
done
```

### `while` loop
Used to run a command as long as a condition is true. Often used for reading files line-by-line.
```bash
while read LINE; do
    echo "Processing user: $LINE"
done < users.txt
```
