# TruffleHog

[TruffleHog](https://github.com/trufflesecurity/trufflehog) is a secret scanner that not only finds hardcoded secrets in your codebase but actually **verifies** them by making API calls to the respective providers to see if they are active.

## Key Features
- Secret Verification (checks if the AWS key or GitHub token is actually valid).
- Scans Git history, not just the current state.
- Scans S3 buckets, Docker images, and Syslog.

## Installation
```bash
# macOS
brew install trufflehog

# Windows (Scoop)
scoop bucket add trufflehog https://github.com/trufflesecurity/scoop-trufflehog
scoop install trufflehog

# Docker
docker pull trufflesecurity/trufflehog:latest
```

## Usage

### 1. Scan a Git Repository
```bash
trufflehog git https://github.com/user/repo.git
```

### 2. Scan Local Directory (and verify secrets)
```bash
trufflehog filesystem .
```

### 3. Scan without verification (Faster)
```bash
trufflehog filesystem --no-verification .
```

## Difference between TruffleHog and Gitleaks
- **Gitleaks:** Very fast, uses regex and entropy, great for pre-commit hooks, static analysis.
- **TruffleHog:** Actively verifies secrets against APIs, great for CI pipelines or auditing to know if a leaked secret is an immediate threat.
