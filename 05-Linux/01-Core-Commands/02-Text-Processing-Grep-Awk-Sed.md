---
tags: [linux, commands, text-processing, grep, awk, sed]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Text Processing in Linux: Grep, Awk, Sed

As a DevOps engineer, you will spend a massive amount of time parsing logs, extracting IP addresses, and replacing configuration values on the fly. The "Holy Trinity" of Linux text processing is `grep`, `awk`, and `sed`.

## 1. `grep` (Global Regular Expression Print)
Used to search for patterns within text or log files.

### Common Flags
- `-i`: Case-insensitive search.
- `-v`: Invert match (show lines that do NOT match the pattern).
- `-r` / `-R`: Recursive search through directories.
- `-n`: Print the line numbers alongside the matched lines.
- `-C <num>`: Context lines (shows N lines before and after the match).
- `-E`: Extended regular expressions (same as `egrep`).

### Real-World DevOps Use Cases
```bash
# Find all "ERROR" or "FATAL" in a log file, ignoring case
grep -iE "error|fatal" /var/log/syslog

# Find all instances of a specific IP address in NGINX logs, excluding lines with HTTP 200
grep "192.168.1.50" /var/log/nginx/access.log | grep -v " 200 "

# Search for a specific function name across an entire codebase, showing line numbers
grep -rn "def connect_db" ./src/
```

## 2. `awk`
A complete pattern scanning and text processing language, best used for extracting specific columns from structured text (like CSVs or space-separated log files).

### Basic Syntax
`awk -F 'separator' '{action}' filename`
- If `-F` is omitted, `awk` defaults to splitting by spaces/tabs.
- `$1, $2, ...` refer to the 1st, 2nd, etc. columns. `$0` refers to the entire line.

### Real-World DevOps Use Cases
```bash
# Extract only the IP addresses (usually column 1) from an NGINX access log
awk '{print $1}' /var/log/nginx/access.log

# Extract the IP addresses, sort them, and count how many times each IP hit the server
awk '{print $1}' /var/log/nginx/access.log | sort | uniq -c | sort -nr

# Find which processes are consuming the most memory (using ps)
ps aux | awk '{print $4 "\t" $11}' | sort -nr | head -n 10

# Print users from /etc/passwd whose shell is /bin/bash (colon separated)
awk -F':' '$7 == "/bin/bash" {print $1}' /etc/passwd
```

## 3. `sed` (Stream Editor)
Used primarily to find and replace text on the fly, either piping it to stdout or editing the file in-place.

### Basic Syntax
`sed 's/search_pattern/replacement_string/g' filename`
- `s` stands for substitute.
- `g` stands for global (replace all occurrences on a line, not just the first).
- `-i` edits the file **in-place**.

### Real-World DevOps Use Cases
```bash
# In-place replace the database URL in a configuration file
sed -i 's/localhost:5432/db.production.internal:5432/g' config.yml

# Uncomment a specific line (e.g., removing the leading # from 'Port 22')
sed -i 's/^#Port 22/Port 2222/g' /etc/ssh/sshd_config

# Delete specific lines: Delete lines 10 through 20 from a file
sed -i '10,20d' large_file.txt

# Delete all empty lines from a file
sed -i '/^$/d' data.txt
```

## Pipeline Power
The true power of Linux comes from chaining these tools together using pipes (`|`).

**Scenario:** We need to find the total sum of bytes transferred by a specific IP from an NGINX log.
```bash
grep "192.168.1.50" access.log | awk '{sum += $10} END {print "Total Bytes: " sum}'
```
