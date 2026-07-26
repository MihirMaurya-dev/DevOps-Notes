# Gitleaks

[Gitleaks](https://github.com/gitleaks/gitleaks) is a fast, light-weight, portable, and open-source static analysis tool for detecting and preventing hardcoded secrets like passwords, API keys, and tokens in git repositories.

## Installation

You can install Gitleaks using various methods. Here are a few common ones:

**macOS (Homebrew):**
```bash
brew install gitleaks
```

**Windows (Scoop):**
```bash
scoop install gitleaks
```

**Docker:**
```bash
docker pull zricethezav/gitleaks:latest
```

## Simple Examples

### 1. Scan a local repository
To scan a repository that you have cloned locally, navigate to the repository directory (or specify its path) and run:

```bash
gitleaks detect --source . -v
```
- `--source .`: Specifies the current directory to scan.
- `-v`: Verbose mode (shows the leaks found in the terminal output).

### 2. Generate a JSON report
You can output the results to a file for later analysis or integration into other tools:

```bash
gitleaks detect --source . --report-path=leaks-report.json --report-format=json
```

### 3. Scan unstaged/uncommitted changes (Pre-commit)
If you want to check if the changes you are about to commit contain any secrets:

```bash
gitleaks protect -v --staged
```
*(This is commonly used in pre-commit hooks to prevent secrets from ever being committed).*

### 4. Scan a specific branch
If you want to scan a specific branch (e.g., `main`):

```bash
gitleaks detect --source . --log-opts="--all origin/main"
```

## How to Handle False Positives

Sometimes Gitleaks might flag something that isn't an actual secret (e.g., a dummy password in a test file). You can ignore these using a `.gitleaksignore` file in the root of your repository.

Example of a `.gitleaksignore` file:

```toml
[allowlist]
description = "Ignore dummy secrets in test files"
paths = [
    '''tests/.*''',
    '''mocks/.*'''
]
```

## Pre-commit Hook Setup (Recommended)
The most powerful use of Gitleaks is as a **pre-commit hook** — it stops secrets from ever being committed in the first place.

1. Install `pre-commit`: `pip install pre-commit`
2. Create a `.pre-commit-config.yaml` in your repo root:
```yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.4
    hooks:
      - id: gitleaks
```
3. Install the hook: `pre-commit install`

Now every `git commit` will automatically run Gitleaks before the commit is saved.

## Production Grade (CI/CD Integration)

### GitHub Actions Example
```yaml
name: Secret Scan

on: [push, pull_request]

jobs:
  gitleaks:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0  # Full history needed to scan all commits

      - name: Run Gitleaks
        uses: gitleaks/gitleaks-action@v2
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

### Azure DevOps Example
```yaml
steps:
  - script: |
      docker run --rm -v $(Build.SourcesDirectory):/repo \
        zricethezav/gitleaks:latest \
        detect --source /repo -v --exit-code 1
    displayName: 'Run Gitleaks Secret Scan'
```
> **Note:** `--exit-code 1` ensures the pipeline **fails** if secrets are detected.
