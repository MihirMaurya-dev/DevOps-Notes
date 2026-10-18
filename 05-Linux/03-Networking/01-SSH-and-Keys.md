---
tags: [linux, networking, ssh, security, ed25519]
source: devopsinsiders/batch-18
created: 2026-06-08
---

# SSH and Key Management

Secure Shell (SSH) is the cryptographic network protocol used to operate network services securely over an unsecured network. It is the primary way DevOps engineers access and manage Linux servers (Port 22).

## Password vs. Key-Based Authentication
- **Password Auth:** Vulnerable to brute-force attacks. Should be disabled on public-facing servers.
- **Key-Based Auth:** Uses asymmetric cryptography (a public and private key pair). Vastly more secure.

## The Key Pair
- **Private Key (`id_ed25519`):** Stays on your local laptop. Must be kept perfectly secret. If compromised, an attacker can access your servers. (Permissions MUST be `chmod 400`).
- **Public Key (`id_ed25519.pub`):** You place this on any server you want to access. It is safe to share.

## Best Practice: Ed25519 vs RSA
> [!important]
> **Always use Ed25519 instead of RSA.**
> RSA is older, slower, and requires very large keys (2048 or 4096 bits) to be secure. Ed25519 is a modern elliptic curve algorithm that is significantly faster, more secure, and uses much shorter keys.

**Generating a key:**
`ssh-keygen -t ed25519 -C "your_email@example.com"`

## Connecting to a Server

**Basic Connection:**
`ssh username@198.51.100.24`

**Connecting with a specific private key:**
`ssh -i ~/.ssh/my_custom_key.pem username@198.51.100.24`

## How Key-Based Auth Works on the Server
When you try to SSH into a server, the server's SSH daemon (`sshd`) checks the `~/.ssh/authorized_keys` file for the user you are trying to log in as.
- If it finds a public key that matches your private key (verified via a cryptographic challenge), it lets you in.
- To grant a coworker access to a server, they generate a key pair and send you their `.pub` file. You append the contents of their `.pub` file to the `~/.ssh/authorized_keys` file on the server.

## SSH Agent
If your private key has a passphrase (highly recommended), typing it every time is annoying. `ssh-agent` is a background program that holds your decrypted private key in memory so you only have to type the passphrase once per session.

Start it and add your key:
```bash
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```
