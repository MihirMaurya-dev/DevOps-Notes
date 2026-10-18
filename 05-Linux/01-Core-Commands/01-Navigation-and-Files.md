---
tags: [linux, commands, navigation, files]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# Core Linux Commands: Navigation and Files

Proficiency with the command line is non-negotiable for DevOps Engineers.

## Navigation Commands

| Command | Description             | Example / Note                                                                                                           |
| ------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `pwd`   | Print Working Directory | Tells you where you are.                                                                                                 |
| `cd`    | Change Directory        | `cd /var/log` (Absolute path). `cd ../` (Go up one level). `cd ~` (Go to home directory).                                |
| `ls`    | List Directory Contents | `ls -la` (Lists all files, including hidden ones starting with `.`, in a long format showing permissions and ownership). |

## File & Directory Operations

| Command | Description | Example / Note |
|---|---|---|
| `touch` | Create an empty file or update timestamp | `touch newfile.txt` |
| `mkdir` | Make Directory | `mkdir -p /app/config/prod` (The `-p` flag creates parent directories if they don't exist). |
| `rm` | Remove files or directories | `rm file.txt`. Use `rm -rf /folder` to forcefully and recursively delete a folder. **Dangerous!** |
| `cp` | Copy files or directories | `cp source.txt dest.txt`. Use `cp -r /dir1 /dir2` for directories. |
| `mv` | Move or Rename files | `mv oldname.txt newname.txt` (Rename). `mv file.txt /tmp/` (Move). |

## Viewing File Content

| Command | Description | Example / Note |
|---|---|---|
| `cat` | Concatenate and print files | `cat file.txt` (Dumps the whole file to the screen. Not good for huge files). |
| `less` | View file with pagination | `less file.txt` (Allows scrolling up and down. Press `q` to quit). |
| `head` | Output the first part of a file | `head -n 20 file.txt` (Shows the first 20 lines). |
| `tail` | Output the last part of a file | `tail -n 20 file.txt` (Shows the last 20 lines). |
| `tail -f` | Follow file output continuously | `tail -f /var/log/syslog` (Crucial for watching logs in real-time as an application runs). |
