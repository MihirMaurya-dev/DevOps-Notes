# Trivy

[Trivy](https://github.com/aquasecurity/trivy) is a comprehensive and versatile security scanner. It scans container images, file systems, Git repositories, and Kubernetes for vulnerabilities, misconfigurations (IaC), and secrets.
Trivy has absorbed `tfsec` for its IaC scanning engine.

## Key Features
- All-in-one scanner (IaC, OS packages, Language dependencies, Container Images).
- Fast and stateless.
- Detects CVEs (Common Vulnerabilities and Exposures).

## Installation
```bash
# macOS
brew install aquasecurity/trivy/trivy

# Windows
choco install trivy
```

## Usage

### 1. IaC Scanning (Alternative to tfsec)
```bash
trivy config .
```

### 2. Container Image Scanning
```bash
trivy image nginx:latest
```

### 3. File System Vulnerability Scanning
```bash
trivy fs .
```

### 4. Secrets Scanning
Trivy can also detect hardcoded secrets (API keys, passwords) in your codebase:
```bash
# Scan for secrets in the filesystem
trivy fs --scanners secret .

# Scan a container image for secrets
trivy image --scanners secret nginx:latest
```

## Production Grade (CI/CD Integration)
Run a combined scan — check IaC misconfigs AND secrets — and fail on CRITICAL:
```bash
# Fail pipeline if any CRITICAL misconfig or secret is found
trivy config --severity CRITICAL --exit-code 1 .
trivy fs --scanners secret --exit-code 1 .
```

### GitHub Actions Example
```yaml
- name: Run Trivy IaC Scan
  uses: aquasecurity/trivy-action@master
  with:
    scan-type: 'config'
    scan-ref: '.'
    severity: 'CRITICAL,HIGH'
    exit-code: '1'
```
