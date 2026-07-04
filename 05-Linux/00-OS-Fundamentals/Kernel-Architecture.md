---
tags: [linux, os, kernel, architecture]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# Linux Kernel Architecture

The Linux operating system is built on a monolithic kernel architecture. The kernel is the core interface between a computer's hardware and its processes.

## The Three Layers of Linux

1. **Hardware Layer:** The physical components (CPU, RAM, Disks, Network Interface Cards).
2. **Kernel Space:** The core of the operating system. It operates with unrestricted access to the hardware.
   - **System Call Interface (SCI):** The gateway that allows user-space applications to request services from the kernel.
   - **Process Management:** CPU scheduling and context switching.
   - **Memory Management:** Allocating RAM and managing swap space.
   - **Virtual File System (VFS):** Provides a common interface for different filesystems (ext4, xfs, fat32).
   - **Device Drivers:** Code that allows the kernel to control hardware.
3. **User Space:** Where all applications and user processes run. These processes have restricted access and must use system calls to interact with the hardware.
   - **Shells:** Bash, Zsh.
   - **Applications:** Nginx, SSH daemon, databases.

## Why is it Monolithic?
Linux is a monolithic kernel because all OS services (memory management, file systems, device drivers) run in the same privileged memory space (Kernel Space). 
- **Pro:** High performance, as there is little overhead in communication between OS components.
- **Con:** A bug in a single device driver can potentially crash the entire system (Kernel Panic).

*Contrast this with a Microkernel (like MINIX or macOS's XNU hybrid), where only essential services run in kernel space, and other services run as user-space processes.*
