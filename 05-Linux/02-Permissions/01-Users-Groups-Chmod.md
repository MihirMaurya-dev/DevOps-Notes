---
tags: [linux, permissions, users, chmod, chown]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# Linux Users, Groups, and Permissions

Security in Linux starts at the file system level. Understanding who owns a file and who can access it is fundamental.

## Users and Groups
- Every process runs as a specific **User**.
- Every file is owned by a **User** and a **Group**.
- The `root` user (UID 0) is the superuser and has unrestricted access to the entire system.

### Management Commands
- `useradd <username>`: Creates a new user.
- `usermod -aG sudo <username>`: Adds a user to a group (e.g., adding them to the `sudo` group grants them admin privileges).
- `passwd <username>`: Sets or changes a user's password.
- `id <username>`: Shows the user's UID and the groups they belong to.

## File Permissions
When you run `ls -l`, you see a 10-character string like `-rwxr-xr--`.

1. The first character is the type (`-` for file, `d` for directory, `l` for symlink).
2. The next 3 characters are the **User (Owner)** permissions (`rwx`).
3. The next 3 characters are the **Group** permissions (`r-x`).
4. The last 3 characters are the **Others (Everyone else)** permissions (`r--`).

### Permission Types
- **r (Read):** Value = 4. View file contents, or list directory contents.
- **w (Write):** Value = 2. Modify file contents, or add/delete files in a directory.
- **x (Execute):** Value = 1. Run a script/binary, or enter/`cd` into a directory.

## Managing Permissions

### `chmod` (Change Mode)
Changes the read/write/execute permissions. Usually done using the numeric (octal) method by adding the values together.

- `chmod 777 file.txt`: (4+2+1, 4+2+1, 4+2+1) = Everyone can read, write, and execute. **Very insecure. Never do this in production.**
- `chmod 644 file.txt`: (4+2, 4, 4) = Owner can read/write, Group and Others can only read. (Standard for files).
- `chmod 755 script.sh`: (4+2+1, 4+1, 4+1) = Owner can read/write/execute, Group and Others can read/execute. (Standard for scripts and directories).
- `chmod 400 key.pem`: (4, 0, 0) = Only the owner can read. (Mandatory for SSH private keys).

### `chown` (Change Owner)
Changes the user and/or group ownership of a file.

- `chown nginx file.txt`: Changes owner to the user `nginx`.
- `chown nginx:www-data file.txt`: Changes owner to `nginx` and group to `www-data`.
- `chown -R nginx:www-data /var/www/html`: The `-R` flag changes ownership recursively for all files and folders inside the directory.
