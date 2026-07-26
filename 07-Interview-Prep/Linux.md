---
tags: [interview, prep, linux, bash, questions]
source: devopsinsiders/batch-18
updated: 2026-07-26
---

# Linux & Bash Interview Questions

A collection of comprehensive interview questions regarding Linux administration and bash scripting, ranging from basics to scenario-based troubleshooting.

---

## Basics

### Q1: Explain the Linux file system hierarchy. What is the purpose of `/etc`, `/var`, and `/opt`?
**A:**
- **`/etc`**: Contains system-wide configuration files (e.g., `/etc/nginx/nginx.conf`, `/etc/passwd`). These are text files edited by sysadmins.
- **`/var`**: Contains variable data files that grow over time, most importantly system and application logs (`/var/log`).
- **`/opt`**: Intended for optional, self-contained add-on application software packages not provided by the default OS distribution.

### Q2: What is the difference between `apt update` and `apt upgrade`?
**A:** 
- `apt update` contacts the configured software repositories and downloads the latest lists of available software versions and dependencies. It does not install anything.
- `apt upgrade` applies those updates by downloading and installing the newer versions of the packages currently installed on your system.

### Q3: Explain the significance of file permissions like `chmod 755` vs `chmod 400`.
**A:** 
- `chmod 755`: Grants read (4), write (2), and execute (1) to the owner (7). Group and others get read and execute (5). Standard for executable scripts or web directories.
- `chmod 400`: Grants read-only permission (4) to the owner, and zero access to group and others. This is highly secure and strictly required for SSH private keys (`.pem`).

### Q4: How do you search for a specific string of text inside multiple files?
**A:** I would use the `grep` command. To search recursively through all files in a directory for the word "Error", I would run:
```bash
grep -r "Error" /var/log/
```
Adding the `-i` flag makes it case-insensitive.

### Q5: How do you find a file if you know its name but not its location?
**A:** I would use the `find` command. To search the entire filesystem for `database.yml`, I would run:
```bash
sudo find / -name "database.yml"
```
Alternatively, `locate database.yml` is much faster as it uses a pre-built index, but it relies on `updatedb` having been run recently.

### Q6: What is a tarball and how do you extract it?
**A:** A tarball is an archive of files grouped together, often compressed. To extract a `.tar.gz` file, use:
```bash
tar -xzf archive.tar.gz
```
(`x` = extract, `z` = decompress gzip, `f` = file).

### Q7: How do you run a process in the background?
**A:** You can append an ampersand `&` to the end of the command to run it in the background. If a process is already running in the foreground, press `Ctrl+Z` to suspend it, then type `bg` to resume it in the background.

---

## Intermediate

### Q8: What is `systemd` and how do you manage services with it?
**A:** `systemd` is the init system (PID 1) and service manager for most modern Linux distributions. It manages system startup and services. You use `systemctl` to interact with it:
- `systemctl status nginx` (check status)
- `systemctl start/stop/restart nginx` (manage state)
- `systemctl enable nginx` (ensure it starts on boot).

### Q9: What is the purpose of `set -euo pipefail` at the top of a bash script?
**A:** It enforces "strict mode" making automation scripts much safer:
- `-e`: Exits immediately if any command fails.
- `-u`: Exits immediately if an undefined variable is referenced.
- `-o pipefail`: Ensures that if a single command in a pipeline fails (e.g., `cmd1 | cmd2`), the whole pipeline reports failure.

### Q10: How do you check which process is listening on a specific network port?
**A:** The modern approach is to use `ss` (socket statistics):
```bash
ss -tulnp | grep :443
```
Alternatively, you can use `lsof` (List Open Files):
```bash
sudo lsof -i :443
```
Both will show the process ID (PID) and name bound to that port.

### Q11: What is the difference between a hard link and a symbolic (soft) link?
**A:**
- **Hard link:** Points directly to the same underlying physical data blocks (inode) as the original file. If the original is deleted, the data persists via the hard link. Cannot span filesystems.
- **Symbolic link:** Points to the path of the original file, acting like a shortcut. If the original is deleted, the symlink breaks ("dangles"). Can span filesystems and link directories.

### Q12: How do you schedule recurring background jobs without using cron?
**A:** You can use **systemd timers**. They are the modern replacement for cron, pairing a `.timer` unit file with a `.service` unit file. They offer better logging via `journalctl`, precise scheduling constraints (like running specific minutes after boot), and better handling of missed executions.

### Q13: What is the difference between `kill`, `kill -9`, and `killall`?
**A:**
- `kill <PID>`: Sends `SIGTERM` (15), politely asking the process to terminate and clean up.
- `kill -9 <PID>`: Sends `SIGKILL` (9), which the kernel executes immediately without letting the process clean up. Use only if a process is frozen.
- `killall <name>`: Sends a signal to all running instances of a given process name.

### Q14: How do you check current memory usage on a Linux system?
**A:** You use the `free -h` command to see total, used, and available RAM in a human-readable format. For real-time process-level memory monitoring, use `top` or `htop`.

### Q15: What is the difference between standard output (stdout) and standard error (stderr)?
**A:** 
- **stdout** (file descriptor 1) is used for normal output messages from a command.
- **stderr** (file descriptor 2) is used specifically for error messages. 
You can redirect them separately: `command > output.txt 2> error.txt`.

---

## Advanced

### Q16: How would you debug a failing bash script?
**A:** I would run the script with the `bash -x script.sh` flag. This enables execution tracing, printing every command to the terminal (preceded by a `+`) exactly as it is evaluated, after variable expansion. This makes it trivial to see exactly where and why a script fails.

### Q17: What are Linux namespaces and cgroups?
**A:** These are the foundational kernel technologies powering containers (like Docker). 
- **Namespaces** provide process isolation by giving a process its own independent view of the filesystem, network, and process IDs. 
- **Cgroups (Control Groups)** provide resource limitation, ensuring a process can only consume a specified amount of CPU, memory, or disk I/O.

### Q18: Explain logical volume management (LVM).
**A:** LVM abstracts physical storage devices into dynamic logical volumes. It allows you to group multiple physical disks into a Volume Group (VG), and then carve out flexible Logical Volumes (LVs). This allows sysadmins to resize partitions online, span file systems across multiple disks, and take storage snapshots without downtime.

### Q19: What is the difference between `awk` and `sed`?
**A:**
- **`sed` (Stream Editor):** Best for line-by-line text substitutions and transformations (e.g., `sed 's/old/new/g' file.txt`).
- **`awk`:** A full data extraction and reporting language. It is best used for processing column-based tabular data. For example, `awk '{print $2}'` extracts the second column from a text stream.

### Q20: How do you configure a persistent static IP on modern Ubuntu?
**A:** Modern Ubuntu uses **Netplan**. You define network configurations in a YAML file located at `/etc/netplan/`. After defining the static IP, gateway, and nameservers in the YAML file, you apply the configuration by running `sudo netplan apply`.

### Q21: What is swappiness in Linux kernel?
**A:** Swappiness is a kernel parameter (0 to 100) that controls how aggressively the kernel swaps memory pages out to the disk's swap space. A lower value (like 10) tells the kernel to prefer keeping data in RAM as much as possible, which is usually preferred for database servers to maintain performance.

### Q22: What is the purpose of SELinux or AppArmor?
**A:** They provide Mandatory Access Control (MAC) mechanisms to enhance system security. Unlike standard file permissions, they confine programs to a limited set of resources, mitigating the impact of vulnerabilities. If a web server is compromised, SELinux policies prevent the attacker from accessing files outside the web root, even if the service runs as root.

---

## Scenario-Based

### Q23: Scenario: A web application running on port 80 is unreachable from the browser. How do you troubleshoot?
**A:** 
1. `ss -tulnp | grep :80` to verify the web server process is running and bound to port 80.
2. `systemctl status nginx` to check if the service crashed.
3. `curl -I http://localhost` from the server itself. If it works locally, it's a network issue.
4. Check the firewall rules (`iptables -L` or `ufw status`) to ensure port 80 traffic is allowed ingress.
5. Check application logs (`tail /var/log/nginx/error.log`).

### Q24: Scenario: The server reports `No space left on device`, but `df -h` shows the disk is only 50% full. What is happening?
**A:** 
The server has likely run out of inodes. Every file and directory consumes an inode. If the system creates millions of tiny files (like session files or cache), it consumes all inodes before filling the disk capacity. Use `df -i` to verify inode exhaustion.

### Q25: Scenario: You delete a massive 50GB log file, but `df -h` shows the disk space hasn't been freed. Why?
**A:** 
The file is likely still held open by a running process (like the application writing the logs). In Linux, space isn't freed until the file is deleted *and* all file handles pointing to it are closed. I would use `lsof | grep deleted` to find the process holding it, and then restart or reload that service to release the file descriptor.

### Q26: Scenario: How would you write a bash script to parse a file of hostnames and check if port 22 is open on each?
**A:**
```bash
#!/bin/bash
set -euo pipefail
while IFS= read -r server; do
  if timeout 2 bash -c "echo > /dev/tcp/$server/22" 2>/dev/null; then
    echo "$server: OPEN"
  else
    echo "$server: CLOSED"
  fi
done < servers.txt
```
This uses bash's built-in pseudo-device `/dev/tcp` for efficient port checking without requiring external tools like `nc` or `nmap`.

### Q27: Scenario: Server CPU load is incredibly high. How do you trace the culprit?
**A:** 
First, I run `top` or `htop` and sort by CPU usage to identify the specific Process ID (PID) consuming resources. If it's an application I manage, I can use `strace -p <PID>` to see what system calls it's stuck on, or inspect its logs. If it's a generic process acting strangely, I'd check `dmesg` or `/var/log/syslog` for hardware or kernel-level errors causing high I/O wait.

### Q28: Scenario: You lose the root password and need to gain access to a physical Linux server.
**A:** 
I would reboot the server and interrupt the GRUB boot menu. I would edit the boot parameters by appending `init=/bin/bash` or `rd.break` to the kernel line. This boots the system into a single-user shell without requiring a password. I would then mount the root filesystem with write access (`mount -o remount,rw /`), run the `passwd` command to set a new root password, and reboot.
