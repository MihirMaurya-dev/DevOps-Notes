---
tags: [linux, sysadmin, systemd, services]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-14
---

# systemd and Service Management

`systemd` is the init system and system manager that has become the standard for almost all modern Linux distributions (Ubuntu, RHEL, CentOS, Debian). It is the first process to run (PID 1) and is responsible for bringing up the rest of the system.

## 1. Core `systemctl` Commands

`systemctl` is the primary command used to interact with `systemd`.

| Command | Action |
|---------|--------|
| `systemctl start <service>` | Starts the service immediately. |
| `systemctl stop <service>` | Stops the service immediately. |
| `systemctl restart <service>` | Stops and then starts the service. Causes brief downtime. |
| `systemctl reload <service>` | Reloads the configuration *without* stopping the service (graceful). Ideal for NGINX/Apache config changes. |
| `systemctl status <service>` | Shows if it's running, recent logs, and the exact path to the service file. |
| `systemctl enable <service>` | Configures the service to start automatically on system boot. |
| `systemctl disable <service>` | Prevents the service from starting on boot. |

## 2. Anatomy of a systemd Unit File

To run your own application (e.g., a Python Flask app or a Go binary) as a background service, you must create a `systemd` Unit file, typically placed in `/etc/systemd/system/`.

**Example: `/etc/systemd/system/myapp.service`**
```ini
[Unit]
Description=My Custom DevOps Python API
After=network.target postgresql.service # Don't start until network and DB are up

[Service]
User=appuser
Group=appgroup
WorkingDirectory=/opt/myapp
Environment="FLASK_ENV=production"
EnvironmentFile=/etc/myapp/.env

# The actual command to start the app
ExecStart=/opt/myapp/venv/bin/python /opt/myapp/app.py

# Restart policy (crucial for reliability)
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target # Starts during normal system boot
```

### Applying Changes
Whenever you create or modify a `.service` file, you MUST reload the systemd daemon before restarting the service:
```bash
sudo systemctl daemon-reload
sudo systemctl restart myapp.service
sudo systemctl enable myapp.service
```

## 3. Viewing Logs with `journalctl`

`systemd` captures standard output (`stdout`) and standard error (`stderr`) from all services automatically using its logging component, `journald`.

```bash
# View all logs for a specific service
journalctl -u myapp.service

# Follow logs in real-time (like tail -f)
journalctl -u myapp.service -f

# View logs only since the last system boot
journalctl -u myapp.service -b

# Time-based filtering (extremely useful during incidents)
journalctl -u nginx.service --since "2026-06-14 10:00:00" --until "11:00:00"
journalctl -u myapp.service --since "10 minutes ago"
```

## 4. `systemd` Timers (Cron Replacement)
Modern Linux uses `systemd` timers instead of `cron` for many scheduled tasks because timers provide better logging, dependency management, and can easily run tasks on a randomized delay to prevent CPU spikes.

To schedule a task, you create two files:
1. `backup.service` (defines what to run)
2. `backup.timer` (defines when to run it)
