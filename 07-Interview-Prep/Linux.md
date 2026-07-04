---
tags: [interview, prep, linux, bash, questions]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# Linux & Bash Interview Questions

A collection of common interview questions regarding Linux administration and bash scripting.

## Q1: A web application running on port 80 is unreachable. How do you troubleshoot this from the Linux command line?
**A:** 
1. **Check if the process is running and listening:** I would use `ss -tuln | grep :80` to verify that the web server (like Nginx or Apache) is actually bound to port 80.
2. **Check the service status:** I would run `sudo systemctl status nginx` to see if the service is active or if it crashed.
3. **Check the logs:** I would look at `journalctl -u nginx` or `tail -f /var/log/nginx/error.log` to see if there are application-level errors.
4. **Check local connectivity:** I would run `curl -I http://localhost` from the server itself. If this works but external access fails, the issue is likely a firewall (like `iptables` or an Azure NSG).

## Q2: Explain the significance of `chmod 755` vs `chmod 400`.
**A:** 
- `chmod 755`: Assigns read, write, and execute permissions (4+2+1=7) to the owner, and read and execute permissions (4+1=5) to the group and everyone else. This is standard for executable scripts or web directories.
- `chmod 400`: Assigns read-only permission (4) to the owner, and absolutely no permissions (0) to the group or anyone else. This is the mandatory, highly secure permission setting required for SSH private keys (`.pem` files).

## Q3: What is the purpose of `set -euo pipefail` at the top of a bash script?
**A:** It enforces "strict mode" for bash, making automation scripts significantly safer:
- `-e`: Exits immediately if any command returns a non-zero (failure) exit status.
- `-u`: Exits immediately if the script tries to use an undefined variable (prevents dangerous typos like `rm -rf /$UNDEFINED_VAR/`).
- `-o pipefail`: Ensures that if any command in a pipeline fails (e.g., `command1 | command2`), the entire pipeline returns a failure status, rather than just returning the status of `command2`.

## Q4: How do you find a specific file on a Linux system if you don't know where it is?
**A:** I would use the `find` command. For example, to search the entire root filesystem for a file named `database.yml`, I would run: `sudo find / -name "database.yml"`.

For fast searching by filename using a pre-built index, I would use `locate database.yml` (requires `updatedb` to have been run recently).

## Q5: What is the difference between `apt upgrade` and `apt update`?
**A:** 
- `apt update` contacts the configured software repositories and downloads the latest lists of available software versions. It does *not* install or upgrade anything.
- `apt upgrade` actually installs the newer versions of the packages currently installed on the system, based on the lists downloaded by `update`.

## Q6: How do you check which process is listening on a specific port?
**A:** There are two primary commands:
```bash
# Using ss (modern replacement for netstat)
ss -tulnp | grep :443

# Using lsof (List Open Files)
sudo lsof -i :443

# Using netstat (older, may not be installed by default)
netstat -tulnp | grep :443
```
The output shows the PID (Process ID) and the process name holding that port. You can then use `ps aux | grep <PID>` to get more details about that process.

## Q7: Explain the Linux file system hierarchy. What is the purpose of `/etc`, `/var`, `/tmp`, and `/opt`?
**A:**
- **`/etc`** (et cetera): Contains system-wide configuration files. For example, `/etc/nginx/nginx.conf`, `/etc/ssh/sshd_config`, `/etc/passwd`. These files are typically text files edited by the sysadmin.
- **`/var`** (variable): Contains files that are expected to grow in size — primarily log files (`/var/log`), spool data, and runtime files. It changes frequently during system operation.
- **`/tmp`** (temporary): A world-writable directory for temporary files. Files here are typically deleted on reboot. Never store important data here.
- **`/opt`** (optional): For add-on, self-contained application software that is not part of the default OS installation (e.g., `/opt/datadog-agent`).

## Q8: What is `systemd` and how do you use it to manage services?
**A:** `systemd` is the init system (PID 1) and service manager for modern Linux distributions (Ubuntu, RHEL, Debian). It manages the startup of all system processes. Common `systemctl` commands:

```bash
# Check service status
systemctl status nginx

# Start / Stop / Restart a service
sudo systemctl start nginx
sudo systemctl stop nginx
sudo systemctl restart nginx

# Reload config without full restart
sudo systemctl reload nginx

# Enable service to start on boot
sudo systemctl enable nginx

# Disable from starting on boot
sudo systemctl disable nginx

# View logs for a service (live tail)
journalctl -u nginx -f

# View logs since last boot
journalctl -u nginx -b
```

## Q9: How would you write a bash script that reads a list of server hostnames from a file and checks if port 22 is open on each?
**A:**
```bash
#!/usr/bin/env bash
set -euo pipefail

SERVERS_FILE="servers.txt"
TIMEOUT=3

while IFS= read -r server; do
  if timeout "$TIMEOUT" bash -c "echo > /dev/tcp/$server/22" 2>/dev/null; then
    echo "[OK]   $server - Port 22 is OPEN"
  else
    echo "[FAIL] $server - Port 22 is CLOSED or UNREACHABLE"
  fi
done < "$SERVERS_FILE"
```

This uses bash's built-in `/dev/tcp` pseudo-device to attempt a TCP connection without needing `nc` or `nmap` installed.

## Q10: What is the difference between a hard link and a symbolic (soft) link?
**A:**
- **Hard link:** A directory entry that points directly to the same inode (physical data blocks) as the original file. If the original file is deleted, the hard link still works because the data blocks remain referenced. Cannot span file systems.
- **Symbolic link (symlink):** A special file that contains a *path* pointing to another file or directory, like a shortcut. If the original file is deleted, the symlink becomes a "dangling" link and breaks. Can span file systems and can point to directories.

```bash
# Create a hard link
ln /etc/nginx/nginx.conf nginx_config_hardlink

# Create a symbolic link
ln -s /etc/nginx/nginx.conf nginx_config_symlink
```

## Q11: How do you schedule a recurring task in Linux without using cron?
**A:** Several alternatives exist:
- **`systemd` timers:** Modern replacement for cron. Define a `.timer` unit file paired with a `.service` unit file. More controllable (on-boot triggers, missed execution handling) and integrated with `journalctl` logging.
- **`at` command:** For one-time scheduled jobs (`echo "backup.sh" | at 2am`).
- **`anacron`:** For systems that aren't running 24/7. Unlike cron, `anacron` catches up on missed jobs when the system is next powered on (e.g., a laptop that was off at the scheduled cron time).

## Q12: What is the difference between `kill`, `kill -9`, and `killall`?
**A:**
- **`kill <PID>`:** Sends the `SIGTERM` (signal 15) to a process. This is a "polite" termination request — it gives the process a chance to clean up (close files, flush buffers) before exiting. Well-written applications respond to this.
- **`kill -9 <PID>`:** Sends the `SIGKILL` (signal 9). This is an immediate, forceful termination that the process cannot catch, block, or ignore. The kernel kills it without allowing cleanup. Use as a last resort.
- **`killall <process_name>`:** Sends a signal (SIGTERM by default) to all processes matching a given name. Convenient for killing all instances of an application (e.g., `killall nginx`).
