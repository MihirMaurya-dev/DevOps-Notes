---
tags: [linux, cron, automation, scheduling]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# Cron Jobs

`cron` is a time-based job scheduler in Unix-like operating systems. It is used to set up commands or scripts to run automatically at specified times or intervals.

## Usage
Every user on a Linux system can have their own `crontab` (cron table).
- `crontab -e`: Edit your current crontab file (opens in your default text editor).
- `crontab -l`: List the contents of your crontab.
- `sudo crontab -e`: Edit the `root` user's crontab (required if the script needs admin privileges, like restarting a system service).

## Cron Syntax
A cron expression consists of 5 time fields followed by the command to execute.

```text
* * * * * command_to_execute
- - - - -
| | | | |
| | | | +----- day of week (0 - 6) (Sunday=0)
| | | +------- month (1 - 12)
| | +--------- day of month (1 - 31)
| +----------- hour (0 - 23)
+------------- minute (0 - 59)
```

### Examples
- `* * * * * /path/to/script.sh`: Runs **every minute**.
- `0 * * * * /path/to/script.sh`: Runs at the **top of every hour** (e.g., 1:00, 2:00).
- `0 0 * * * /path/to/script.sh`: Runs **once a day at midnight**.
- `0 2 * * 0 /path/to/script.sh`: Runs at **2:00 AM every Sunday**.
- `*/5 * * * * /path/to/script.sh`: Runs **every 5 minutes**.

## Best Practices & Gotchas
1. **Absolute Paths:** Cron executes in a very limited environment. It does *not* load your `.bashrc`. Therefore, **always use absolute paths** for commands and scripts. Do not write `python script.py`; write `/usr/bin/python3 /opt/app/script.py`.
2. **Output Redirection:** Cron tries to email the output of scripts to the user. This usually fails or fills up local mailboxes. You should manually redirect output to a log file or to `/dev/null`.
   - `0 0 * * * /opt/backup.sh >> /var/log/backup.log 2>&1` (Appends stdout and stderr to a log file).
3. **systemd Timers:** While cron is the classic tool, modern Linux distributions heavily prefer **systemd timers** for scheduling. They offer better logging (integrated with `journalctl`), dependency management (don't run the backup script until the network is up), and more complex scheduling constraints. However, cron is still widely used for simple tasks.
