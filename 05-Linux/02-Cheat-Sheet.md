---
tags: [linux, commands, cheat-sheet]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Linux Command Cheat Sheet

A quick reference for the most essential Linux commands used in DevOps and System Administration.

## Navigation & Discovery
```bash
pwd                          # Print Working Directory (where am I?)
ls -la                       # List all files (including hidden) with detailed permissions
ls -lh                       # Human-readable file sizes
cd /var/log                  # Change directory
find / -name "nginx.conf"    # Search filesystem for file by name
find /var/log -mtime -1      # Find files modified in the last 1 day
locate filename              # Fast filename search using pre-built index
which python3                # Show full path of a command
```

## File Inspection & Manipulation
```bash
cat file.txt                 # Print entire file to screen
less file.txt                # Scrollable viewer (q to quit)
tail -f /var/log/syslog      # Follow log file in real-time
tail -n 100 /var/log/app.log # Show last 100 lines
head -n 20 file.txt          # Show first 20 lines
wc -l file.txt               # Count lines in file
diff file1.txt file2.txt     # Show differences between two files
cp -r src/ dest/             # Copy directory recursively
mv oldname newname           # Move/rename file
rm -rf /path/to/dir          # Remove directory recursively (⚠️ irreversible)
mkdir -p /path/to/deep/dir   # Create nested directories
```

## Text Processing
```bash
grep -i "error" app.log          # Search case-insensitively
grep -rn "TODO" ./src            # Recursive search with line numbers
grep -v "INFO" app.log           # Invert: show lines NOT matching
awk '{print $1}' access.log      # Print first column (e.g., IP from access log)
awk -F',' '{print $2}' data.csv  # Use comma as field separator
sed -i 's/old/new/g' config.yml  # In-place replace all occurrences
sed -n '10,20p' file.txt         # Print lines 10-20
cut -d':' -f1 /etc/passwd        # Print first field (username) from /etc/passwd
sort file.txt | uniq -c          # Sort and count unique lines
```

## System & Processes
```bash
top                          # Real-time resource usage (q to quit)
htop                         # Enhanced top (if installed)
ps aux                       # List all processes
ps aux | grep nginx          # Find specific process
kill -15 <PID>               # Graceful terminate (SIGTERM)
kill -9 <PID>                # Force kill (SIGKILL)
killall nginx                # Kill all processes named nginx
df -h                        # Disk space usage (human-readable)
du -sh /var/log              # Directory size summary
free -m                      # RAM usage in MB
uptime                       # System uptime and load averages
uname -a                     # Kernel version and system info
lscpu                        # CPU information
lsblk                        # List block devices (disks)
```

## Networking
```bash
ping google.com              # Test basic ICMP connectivity
curl -I https://google.com   # Fetch HTTP headers
curl -sSL https://url | bash # Download and run script (use with caution!)
wget -qO- https://url        # Download URL content to stdout
ss -tuln                     # Show listening TCP/UDP ports (modern)
ss -tulnp | grep :80         # Check what's using port 80
netstat -an                  # List all connections (older systems)
dig example.com              # DNS lookup
dig example.com @8.8.8.8    # DNS lookup via specific DNS server (Google)
nslookup example.com         # Another DNS tool
traceroute google.com        # Trace network route
ip addr show                 # Show IP addresses on all interfaces
ip route                     # Show routing table
ssh -i key.pem user@host     # Connect with identity file
ssh -L 8080:localhost:80 user@remotehost  # SSH local port forwarding
```

## Permissions & Ownership
```bash
chmod 755 script.sh          # rwxr-xr-x (owner: full, group/others: read+exec)
chmod 644 file.txt           # rw-r--r-- (owner: read+write, others: read)
chmod 400 key.pem            # r-------- (SSH key - owner read only)
chmod +x script.sh           # Add execute bit for all
chown nginx:www-data file    # Change owner and group
chown -R www-data:www-data / # Recursive ownership change
ls -la                       # View permissions
stat file.txt                # Detailed file metadata
```

## Package Management (Ubuntu/Debian)
```bash
sudo apt update              # Refresh package index (always run before install)
sudo apt upgrade -y          # Upgrade all installed packages
sudo apt install -y nginx    # Install package
sudo apt remove nginx        # Remove package (keep config)
sudo apt purge nginx         # Remove package and config
apt list --installed         # List installed packages
dpkg -l | grep nginx         # Check if specific package installed
```

## Systemd Service Management
```bash
systemctl status nginx       # Check service status
systemctl start nginx        # Start service
systemctl stop nginx         # Stop service
systemctl restart nginx      # Restart service (full stop+start)
systemctl reload nginx       # Reload config without full restart
systemctl enable nginx       # Enable to start on boot
systemctl disable nginx      # Disable from starting on boot
systemctl list-units --type=service  # List all services
journalctl -u nginx          # View service logs
journalctl -u nginx -f       # Follow service logs live
journalctl -u nginx -b       # Logs since last boot
journalctl --since "1 hour ago"      # Logs from last hour
```

## User & Group Management
```bash
whoami                       # Current user
id                           # User ID, group IDs
sudo su -                    # Switch to root user
useradd -m -s /bin/bash alice  # Create user with home dir and bash shell
usermod -aG sudo alice       # Add user to sudo group
passwd alice                 # Set user password
userdel -r alice             # Delete user and home directory
groupadd devops              # Create group
groups alice                 # List groups for a user
```

## Bash Scripting Safety
Always start your bash scripts with these safety flags:
```bash
#!/usr/bin/env bash
set -euo pipefail
# -e : exit on error
# -u : exit on undefined variable
# -o pipefail : fail entire pipeline if any command fails
```

## Archive & Compression
```bash
tar -czf archive.tar.gz /path/    # Create gzip-compressed tar archive
tar -xzf archive.tar.gz           # Extract gzip tar archive
tar -czf - /path | ssh user@host "tar -xzf -"  # Compress and pipe to remote
zip -r archive.zip /path/         # Create zip archive
unzip archive.zip                 # Extract zip
gzip file.txt                     # Compress file (creates file.txt.gz)
gunzip file.txt.gz                # Decompress gzip file
```

## Disk & Storage
```bash
df -h                        # File system disk space usage
du -sh /*                    # Summary size of root-level directories
du -sh * | sort -h           # Sort directories by size
lsblk                        # Block devices
fdisk -l                     # Disk partitions (requires root)
mount /dev/sdb1 /mnt/data    # Mount a disk partition
umount /mnt/data             # Unmount
```

## Cron Scheduling
```bash
crontab -e                   # Edit current user's crontab
crontab -l                   # List current user's crontab
# Cron format: min hour day month weekday command
# Example: Run backup.sh every day at 2:30 AM
30 2 * * * /opt/scripts/backup.sh >> /var/log/backup.log 2>&1
```
