---
category: Git
tags: [git, github, cli, commands, reference, workflow, branch, merge, rebase, stash, pr, gh-cli]
type: reference
status: active
level: beginner-to-intermediate
created: 2026-08-09
updated: 2026-08-09
---

# 🐙 Git & GitHub — Complete Commands Reference

> Every Git and GitHub CLI command you will use as a DevOps engineer — what it does, its effect, what comes before and after, and common mistakes.

---

## 📖 Before You Read

- You know what Git and GitHub are → [[02-Introduction|01-Introduction]]
- You know the basic PR workflow → [[05-Core-Workflow|03-Core-Workflow]]
- This note is a **hands-on command reference** — not a concepts guide

---

## 🗺️ Command Flow Overview

```text
┌─────────────────────────────────────────────┐
│  SETUP (one time)                           │
│  git config                                 │
│  git clone / git init                       │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  DAILY WORKFLOW                             │
│  git checkout -b feature/xyz               │
│       ↓                                     │
│  [make changes]                             │
│       ↓                                     │
│  git status → git add → git commit          │
│       ↓                                     │
│  git push                                   │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  COLLABORATION                              │
│  git pull / git fetch                       │
│  git merge / git rebase                     │
│  gh pr create → gh pr merge                 │
└──────────────┬──────────────────────────────┘
               ↓
┌─────────────────────────────────────────────┐
│  HISTORY & RECOVERY                         │
│  git log / git diff / git show              │
│  git stash / git reset / git revert         │
└─────────────────────────────────────────────┘
```

---

## ⚙️ Group 1 — Configuration Commands

### `git config`

```bash
# Set identity (required before first commit)
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Set default branch name
git config --global init.defaultBranch main

# Set default editor
git config --global core.editor "code --wait"   # VS Code
git config --global core.editor "vim"

# Set default merge strategy
git config --global pull.rebase false    # merge (default)
git config --global pull.rebase true     # rebase on pull

# View all config
git config --list

# View a specific value
git config user.email
```

**Scope levels:**

| Flag | Scope | Config file location |
|------|-------|---------------------|
| `--global` | Current user (all repos) | `~/.gitconfig` |
| `--local` | Current repo only | `.git/config` |
| `--system` | All users on the machine | `/etc/gitconfig` |

**Effect:** Configures Git behaviour — no repo changes.
**Before it:** Must be done before your first `git commit`.

---

## 📁 Group 2 — Repository Commands

### `git init`

```bash
git init
git init my-project    # Creates a new folder and initializes it
```

**What it does:** Initializes a brand new Git repository in the current directory. Creates a hidden `.git/` folder.

**Effect:** Creates `.git/` directory locally. Nothing on GitHub yet.

**After it:** `git remote add origin <url>` → `git push`

---

### `git clone`

```bash
# Clone via HTTPS
git clone https://github.com/org/repo.git

# Clone into a specific folder name
git clone https://github.com/org/repo.git my-folder

# Clone via SSH
git clone git@github.com:org/repo.git

# Clone only the latest commit (shallow clone — faster)
git clone --depth 1 https://github.com/org/repo.git

# Clone a specific branch
git clone --branch feature/xyz https://github.com/org/repo.git
```

**What it does:** Downloads a full copy of the remote repository to your local machine. Sets up `origin` remote automatically.

**Effect:** Creates a local folder with the full repo history.

**After it:** `cd <folder>` → `git checkout -b feature/your-branch`

---

### `git remote`

```bash
# View remotes
git remote -v

# Add a remote
git remote add origin https://github.com/org/repo.git

# Change remote URL
git remote set-url origin https://github.com/org/new-repo.git

# Remove a remote
git remote remove origin

# Rename a remote
git remote rename origin upstream
```

**What it does:** Manages connections to remote repositories (GitHub, Azure Repos, etc.).

**Effect:** Updates local Git config — no effect on remote.

---

## 🌿 Group 3 — Branch Commands

### `git branch`

```bash
# List local branches
git branch

# List all branches (local + remote)
git branch -a

# List remote branches only
git branch -r

# Create a new branch (does NOT switch to it)
git branch feature/add-vnet

# Delete a branch (safe — only if merged)
git branch -d feature/add-vnet

# Force delete (even if not merged)
git branch -D feature/add-vnet

# Rename current branch
git branch -m new-name
```

**What it does:** Creates, lists, or deletes branches locally.

**Effect:** Local branch pointer changes — remote is unaffected until you push.

---

### `git checkout`

```bash
# Switch to an existing branch
git checkout main

# Create AND switch to a new branch
git checkout -b feature/add-nsg

# Create branch from a specific commit/tag
git checkout -b hotfix/bug123 v1.2.0

# Discard all uncommitted changes in a file (DESTRUCTIVE)
git checkout -- variables.tf

# Switch to previous branch
git checkout -
```

**Effect:** Changes HEAD pointer. Modifying files with `--` cannot be undone.

> ⚠️ `git checkout --` on a file **permanently discards** your uncommitted changes. There is no undo.

---

### `git switch` *(modern alternative to checkout)*

```bash
# Switch to existing branch
git switch main

# Create and switch
git switch -c feature/add-nsg

# Switch to previous branch
git switch -
```

`git switch` is the cleaner, modern replacement for `git checkout` when working with branches only.

---

## 📸 Group 4 — Staging & Committing

### `git status`

```bash
git status
git status -s    # Short format
```

**What it does:** Shows the current state of the working directory and staging area.

**Output legend:**

```
?? untracked file
A  newly added to staging
M  modified
D  deleted
R  renamed
```

**Effect:** Read-only — nothing changes.
**When to use:** Before every `git add` and `git commit` to confirm what you are about to stage.

---

### `git add`

```bash
# Stage a specific file
git add main.tf

# Stage multiple files
git add main.tf variables.tf outputs.tf

# Stage all changes in current directory (tracked + untracked)
git add .

# Stage all changes across the whole repo
git add -A

# Stage parts of a file interactively (chunk by chunk)
git add -p main.tf

# Stage only already-tracked files (skip untracked)
git add -u
```

**What it does:** Moves changes from the **working directory** to the **staging area** (index). Git will include staged changes in the next commit.

**Effect:** Staging area updated — no commit yet, no remote change.

**After it:** `git commit`

**Common mistake:**
- ❌ `git add .` from the wrong directory — stages files you did not intend to commit. Always run `git status` first.

---

### `git commit`

```bash
# Commit with a message
git commit -m "feat: add resource group module"

# Stage all tracked files AND commit in one step
git commit -am "fix: correct location variable"

# Open editor to write a detailed multi-line message
git commit

# Amend the last commit (message or content) — before pushing
git commit --amend -m "feat: add resource group and vnet modules"

# Amend without changing the message
git commit --amend --no-edit
```

**What it does:** Creates a permanent snapshot (commit) of all staged changes in the local repository.

**Effect:** New commit added to local history. Remote is unchanged until you push.

**Conventional Commits standard:**

| Prefix | Use |
|--------|-----|
| `feat:` | New feature |
| `fix:` | Bug fix |
| `docs:` | Documentation only |
| `chore:` | Maintenance (deps, config) |
| `refactor:` | Code restructure, no behaviour change |
| `ci:` | CI/CD pipeline changes |
| `test:` | Adding or fixing tests |

> ⚠️ Never `git commit --amend` a commit that has already been pushed to a shared branch — it rewrites history and causes problems for other developers.

---

## 🔄 Group 5 — Sync Commands

### `git fetch`

```bash
# Fetch all changes from all remotes (does NOT merge)
git fetch origin

# Fetch a specific branch
git fetch origin main

# Fetch and prune deleted remote branches
git fetch --prune
```

**What it does:** Downloads changes from the remote but **does not apply them** to your local branch. Puts them in `origin/<branch>` refs.

**Effect:** Remote-tracking refs updated. Your local branch and working directory are unchanged.

**After it:** `git merge origin/main` or `git rebase origin/main`

> 💡 Use `git fetch` + `git log origin/main` to see what changed on remote before merging it.

---

### `git pull`

```bash
# Pull latest changes (fetch + merge)
git pull origin main

# Pull with rebase instead of merge
git pull --rebase origin main

# Pull current branch's upstream
git pull
```

**What it does:** `git fetch` + `git merge` in a single command. Downloads remote changes and applies them to your current branch.

**Effect:** Your local branch is updated with remote changes. A merge commit may be created (unless `--rebase` is used).

**Before it:** Commit or stash any local changes first.

**Common mistake:**
- ❌ Pulling without committing local changes — can cause conflicts or overwrite work. Always `git status` first.

---

### `git push`

```bash
# Push a branch to remote
git push origin feature/add-vnet

# Push and set upstream tracking
git push -u origin feature/add-vnet    # After this, just 'git push' works

# Push all branches
git push --all origin

# Push tags
git push --tags

# Force push (rewrites remote history — DANGEROUS on shared branches)
git push --force

# Safer force push — fails if someone else pushed in between
git push --force-with-lease

# Delete a remote branch
git push origin --delete feature/old-branch
```

**What it does:** Uploads your local commits to the remote repository (GitHub).

**Effect:** Remote branch is updated with your commits.

> ⚠️ `git push --force` on `main` or any shared branch can destroy other people's work. Use `--force-with-lease` instead — it only forces if no one else has pushed since your last fetch.

---

## 🔀 Group 6 — Merge & Rebase

### `git merge`

```bash
# Merge a branch into the current branch
git checkout main
git merge feature/add-vnet

# Merge and always create a merge commit (even for fast-forward)
git merge --no-ff feature/add-vnet

# Squash all commits from the branch into one (staged, not committed)
git merge --squash feature/add-vnet
git commit -m "feat: add vnet module"

# Abort a merge in progress (if there are conflicts)
git merge --abort
```

**What it does:** Combines the history of two branches. Creates a "merge commit" that has two parent commits.

**Effect:** A new merge commit appears in history. The feature branch is preserved.

**After a conflict:** Edit the conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`), then `git add` the resolved files, then `git commit`.

---

### `git rebase`

```bash
# Rebase current branch onto main
git rebase main

# Interactive rebase — rewrite last N commits
git rebase -i HEAD~3

# Abort a rebase in progress
git rebase --abort

# Continue after resolving a conflict
git rebase --continue

# Skip a conflicting commit
git rebase --skip
```

**What it does:** Moves your branch's commits to start from the tip of another branch. Creates a **linear history** (no merge commits).

**Effect:** Commits are rewritten with new SHAs. History looks like you branched off the latest code.

**Before it:** Only rebase commits that have **not been pushed** to a shared branch.

> ⚠️ Never rebase a public/shared branch. Rewriting pushed commits forces everyone else to `git pull --force` and causes confusion.

**Interactive rebase actions:**

| Action | What it does |
|--------|-------------|
| `pick` | Keep the commit as-is |
| `reword` | Keep but edit the commit message |
| `edit` | Pause and amend the commit |
| `squash` | Merge into the previous commit (keep both messages) |
| `fixup` | Merge into the previous commit (discard this message) |
| `drop` | Delete the commit entirely |

---

## 💾 Group 7 — Stash Commands

### `git stash`

```bash
# Stash current uncommitted changes (tracked files only)
git stash

# Stash with a descriptive name
git stash push -m "WIP: half-done NSG rules"

# Also stash untracked files
git stash -u

# Also stash ignored files
git stash -a

# View all stashes
git stash list
# Output: stash@{0}: WIP on feature/add-nsg: abc1234 feat: add subnet

# Apply the most recent stash (keeps it in stash list)
git stash apply

# Apply and remove from stash list
git stash pop

# Apply a specific stash
git stash apply stash@{2}

# Delete a specific stash
git stash drop stash@{0}

# Delete ALL stashes
git stash clear

# Create a branch from a stash
git stash branch feature/recovered stash@{0}
```

**What it does:** Temporarily saves your uncommitted changes and reverts the working directory to a clean state. Useful for switching branches mid-work.

**Effect:** Working directory is clean. Changes are saved in a stack.

**Common use case:**
```bash
# You're in the middle of work and urgently need to fix a bug on main
git stash
git checkout main
git checkout -b hotfix/critical-bug
# ... fix bug ...
git checkout feature/add-nsg
git stash pop
# Continue where you left off
```

---

## 🕵️ Group 8 — History & Inspection

### `git log`

```bash
# Full commit history
git log

# Condensed one-line format
git log --oneline

# Show last N commits
git log -5

# Graphical branch view
git log --oneline --graph --all --decorate

# Log for a specific file
git log -- variables.tf

# Log between two commits
git log abc123..def456

# Search commit messages
git log --grep="feat:"

# Show commits by a specific author
git log --author="John"

# Show commits since a date
git log --since="2026-01-01"
```

**Effect:** Read-only — nothing changes.

---

### `git diff`

```bash
# Changes in working directory (not staged)
git diff

# Changes in staging area (staged, not committed)
git diff --staged
git diff --cached    # Same thing

# Compare two branches
git diff main feature/add-vnet

# Compare two commits
git diff abc123 def456

# Compare a specific file
git diff HEAD -- main.tf

# Summary of what files changed (no line details)
git diff --stat
```

---

### `git show`

```bash
# Show details of the last commit
git show

# Show details of a specific commit
git show abc1234

# Show a specific file at a specific commit
git show abc1234:main.tf
```

---

### `git blame`

```bash
# Show who last modified each line of a file
git blame main.tf

# Show blame for specific lines
git blame -L 10,25 main.tf
```

**Use case:** Finding out who introduced a specific line — useful for code review and debugging.

---

## ↩️ Group 9 — Undo & Recovery

### `git reset`

```bash
# Unstage a file (keep changes in working directory)
git reset HEAD main.tf
git restore --staged main.tf   # Modern equivalent

# Move HEAD back N commits (keep changes staged)
git reset --soft HEAD~1

# Move HEAD back N commits (keep changes in working directory, unstaged)
git reset --mixed HEAD~1   # Default

# Move HEAD back N commits (DISCARD all changes — DESTRUCTIVE)
git reset --hard HEAD~1

# Reset to match remote (discard all local commits and changes)
git reset --hard origin/main
```

**Effect comparison:**

| Flag | HEAD | Staging Area | Working Directory |
|------|------|-------------|-------------------|
| `--soft` | ✅ Moved | Unchanged | Unchanged |
| `--mixed` | ✅ Moved | ✅ Cleared | Unchanged |
| `--hard` | ✅ Moved | ✅ Cleared | ✅ Cleared |

> ⚠️ `git reset --hard` permanently discards uncommitted changes. There is no undo.

---

### `git revert`

```bash
# Create a new commit that undoes a specific commit (safe)
git revert abc1234

# Revert without opening the editor
git revert abc1234 --no-edit

# Revert a merge commit (specify parent)
git revert -m 1 abc1234
```

**What it does:** Creates a **new commit** that reverses the changes of a previous commit — without rewriting history.

**When to use vs `reset`:**
- `git revert` — safe for shared/production branches (adds a new "undo" commit)
- `git reset` — only for local commits that have not been pushed

---

### `git restore`

```bash
# Discard changes in a file (working directory)
git restore main.tf

# Discard all uncommitted changes
git restore .

# Unstage a file (remove from staging area)
git restore --staged main.tf

# Restore a file to its state at a specific commit
git restore --source=abc1234 main.tf
```

Modern replacement for `git checkout --` (for files) and `git reset HEAD` (for unstaging).

---

## 🏷️ Group 10 — Tags

```bash
# Create a lightweight tag
git tag v1.0.0

# Create an annotated tag (with message — preferred)
git tag -a v1.0.0 -m "Release version 1.0.0"

# Tag a specific commit
git tag -a v1.0.0 abc1234 -m "Release v1.0.0"

# List all tags
git tag

# Show tag details
git show v1.0.0

# Push a tag to remote
git push origin v1.0.0

# Push all tags
git push --tags

# Delete a local tag
git tag -d v1.0.0

# Delete a remote tag
git push origin --delete v1.0.0
```

**Use case:** Marking release points (e.g., `v1.0.0`, `v2.3.1`). Tags trigger release pipelines in GitHub Actions.

---

## 🔧 Group 11 — Advanced Commands

### `git cherry-pick`

```bash
# Apply a specific commit from another branch to current branch
git cherry-pick abc1234

# Cherry-pick multiple commits
git cherry-pick abc1234 def5678

# Cherry-pick a range
git cherry-pick abc1234^..def5678

# Cherry-pick without committing (stage only)
git cherry-pick --no-commit abc1234
```

**Use case:** Applying a specific bug fix commit from a feature branch to main without merging the whole branch.

---

### `git bisect`

```bash
# Start bisect session
git bisect start

# Mark current commit as bad (bug exists here)
git bisect bad

# Mark a known good commit
git bisect good v1.0.0

# Git checks out the midpoint — you test and mark:
git bisect good    # or
git bisect bad

# Git narrows down until it finds the commit that introduced the bug
# When done:
git bisect reset
```

**Use case:** Binary search through commit history to find which commit introduced a bug.

---

### `git reflog`

```bash
# Show all recent HEAD movements (even after reset)
git reflog

# Recover a commit that was "lost" by a hard reset
git reflog
# Find the commit SHA
git checkout -b recovery-branch abc1234    # Recover it
```

**Use case:** Last resort recovery tool. Reflog records every position HEAD has been at for the last 90 days — even commits deleted by `git reset --hard`.

---

## 🐙 Group 12 — GitHub CLI (`gh`) Commands

> The `gh` CLI lets you interact with GitHub directly from the terminal — no browser needed.
> Install: `winget install GitHub.cli` (Windows) or `brew install gh` (macOS/Linux)
> Authenticate: `gh auth login`

### Repository Management

```bash
# Create a new repo on GitHub (and locally)
gh repo create my-repo --public
gh repo create my-repo --private --clone

# Clone a repo
gh repo clone org/repo

# View repo info
gh repo view

# View in browser
gh repo view --web

# Fork a repo
gh repo fork org/repo --clone
```

---

### Pull Requests

```bash
# Create a PR (prompts for details)
gh pr create

# Create PR with title, body, and target branch
gh pr create \
  --title "feat: add VNet module" \
  --body "Adds Virtual Network and Subnet modules for hub network" \
  --base main \
  --head feature/add-vnet

# Create a draft PR
gh pr create --draft

# List open PRs
gh pr list

# View a specific PR
gh pr view 42

# View PR in browser
gh pr view 42 --web

# Check out a PR locally (to test it)
gh pr checkout 42

# Review a PR
gh pr review 42 --approve
gh pr review 42 --request-changes --body "Please fix the NSG rules"
gh pr review 42 --comment --body "LGTM, one small suggestion"

# Merge a PR
gh pr merge 42
gh pr merge 42 --squash --delete-branch
gh pr merge 42 --rebase
gh pr merge 42 --merge

# Close a PR without merging
gh pr close 42

# Check PR status and CI checks
gh pr checks 42

# View diff of a PR
gh pr diff 42
```

---

### Issues

```bash
# Create an issue
gh issue create --title "Bug: VNet deploy fails" --body "Steps to reproduce..."

# List issues
gh issue list
gh issue list --label "bug"
gh issue list --assignee "@me"

# View an issue
gh issue view 10

# Close an issue
gh issue close 10

# Reopen an issue
gh issue reopen 10

# Comment on an issue
gh issue comment 10 --body "Investigating this now"
```

---

### GitHub Actions (via `gh`)

```bash
# List workflow runs
gh run list

# View a specific run
gh run view 12345678

# Watch a run in real time
gh run watch 12345678

# View logs of a run
gh run view 12345678 --log

# Re-run a failed workflow
gh run rerun 12345678

# Manually trigger a workflow
gh workflow run terraform.yml
gh workflow run terraform.yml --ref feature/add-vnet
gh workflow run terraform.yml -f environment=prod

# List workflows
gh workflow list

# Enable/disable a workflow
gh workflow enable terraform.yml
gh workflow disable terraform.yml

# View workflow file
gh workflow view terraform.yml
```

---

### Releases

```bash
# Create a release
gh release create v1.0.0 --title "v1.0.0" --notes "Initial release"

# Create a release from a tag
gh release create v1.0.0 --generate-notes

# Upload assets to a release
gh release upload v1.0.0 ./dist/app.zip

# List releases
gh release list

# View a release
gh release view v1.0.0

# Delete a release
gh release delete v1.0.0
```

---

### Secrets & Variables

```bash
# Set a repository secret
gh secret set AZURE_CLIENT_ID

# Set secret from a value
echo "my-secret-value" | gh secret set MY_SECRET

# List secrets (names only — values are hidden)
gh secret list

# Delete a secret
gh secret delete MY_SECRET

# Set a repository variable
gh variable set ENVIRONMENT_NAME --body "production"

# List variables
gh variable list
```

---

### Gist

```bash
# Create a public gist from a file
gh gist create main.tf --public --desc "Terraform resource group example"

# Create a private gist
gh gist create main.tf

# List your gists
gh gist list

# View a gist
gh gist view <gist-id>

# Edit a gist
gh gist edit <gist-id>
```

---

## 📋 Quick Reference Table — Most Used Commands

### Git Commands

| Command | What it does | Affects Azure/Remote? |
|---------|-------------|----------------------|
| `git clone` | Download repo | ❌ No |
| `git status` | Show current state | ❌ No |
| `git add .` | Stage all changes | ❌ No |
| `git commit -m ""` | Save snapshot locally | ❌ No |
| `git push` | Upload to GitHub | ✅ Yes |
| `git pull` | Download + merge | Local only |
| `git fetch` | Download (no merge) | Local only |
| `git checkout -b` | Create + switch branch | ❌ No |
| `git merge` | Merge branch | ❌ No |
| `git rebase` | Rewrite branch history | ❌ No |
| `git stash` | Shelve changes | ❌ No |
| `git stash pop` | Restore shelved changes | ❌ No |
| `git reset --hard` | Discard all changes | ❌ No (DESTRUCTIVE locally) |
| `git revert` | Undo a commit safely | ❌ No |
| `git log --oneline` | View history | ❌ No |
| `git diff --staged` | View staged changes | ❌ No |
| `git tag -a` | Create a release tag | ❌ No |
| `git push --tags` | Push tags to GitHub | ✅ Yes |
| `git cherry-pick` | Apply specific commit | ❌ No |
| `git reflog` | Emergency recovery | ❌ No |

### GitHub CLI (`gh`) Commands

| Command | What it does |
|---------|-------------|
| `gh repo create` | Create a new GitHub repo |
| `gh repo clone` | Clone a repo |
| `gh pr create` | Open a new Pull Request |
| `gh pr list` | List open PRs |
| `gh pr checkout` | Check out a PR branch locally |
| `gh pr review --approve` | Approve a PR |
| `gh pr merge --squash` | Merge a PR with squash |
| `gh pr checks` | View CI status of a PR |
| `gh run list` | List pipeline runs |
| `gh run watch` | Watch a run live |
| `gh run rerun` | Re-run a failed pipeline |
| `gh workflow run` | Manually trigger a workflow |
| `gh secret set` | Set a repository secret |
| `gh variable set` | Set a repository variable |
| `gh issue create` | Create a GitHub issue |
| `gh release create` | Create a GitHub release |

---

## 🔁 Full Real-World Flow

```bash
# ─── SETUP (first time) ───
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
git clone https://github.com/org/repo.git
cd repo

# ─── START FEATURE ───
git checkout main
git pull origin main
git checkout -b feature/add-vnet

# ─── MAKE CHANGES ───
# ... edit files ...
git status
git add .
git status             # confirm what's staged
git commit -m "feat: add virtual network module"

# ─── PUSH ───
git push -u origin feature/add-vnet

# ─── OPEN PR ───
gh pr create \
  --title "feat: add VNet module" \
  --body "Adds hub VNet and spoke subnets" \
  --base main

# ─── MONITOR CI ───
gh pr checks

# ─── REVIEW FEEDBACK — add more commits ───
git add .
git commit -m "fix: correct address space for spoke subnet"
git push

# ─── MERGE ───
gh pr merge --squash --delete-branch

# ─── SYNC LOCAL ───
git checkout main
git pull origin main
git branch -d feature/add-vnet    # clean up local branch
```

---

## 🎤 Interview Answers

**Q: What is the difference between `git merge` and `git rebase`?**
> *"`git merge` combines two branches by creating a new merge commit that has two parents, preserving the full history of both branches. `git rebase` moves the commits of a branch onto the tip of another branch, rewriting those commits with new SHAs and creating a linear history without merge commits. Rebase is preferred for feature branches before opening a PR (cleaner history), while merge is safer for integrating completed work on shared branches since it does not rewrite history."*

**Q: What is the difference between `git reset` and `git revert`?**
> *"`git reset` moves the HEAD pointer back and optionally discards changes — it rewrites history. It should only be used on local commits that have not been pushed. `git revert` creates a new commit that reverses a previous commit, leaving history intact. It is safe to use on shared branches because it does not rewrite any existing commits."*

**Q: What does `git stash` do?**
> *"It temporarily saves your uncommitted changes (both staged and unstaged) and reverts the working directory to a clean state, matching the last commit. This lets you switch branches or pull updates without committing unfinished work. You can restore the stashed changes later with `git stash pop`."*

**Q: What is `git cherry-pick` used for?**
> *"It applies a specific commit from one branch onto the current branch without merging the entire branch. A common use case is backporting a bug fix — if a fix was committed on a feature branch, you can cherry-pick just that commit onto the main or hotfix branch without pulling in all the unfinished feature work."*

**Q: How do you recover from an accidental `git reset --hard`?**
> *"Using `git reflog`. The reflog records every position HEAD has been at for the past 90 days, including commits that appear to be deleted after a hard reset. You find the commit SHA in `git reflog`, then create a new branch from that SHA: `git checkout -b recovery-branch <sha>`."*

---

## 🔗 Related Notes

- [[02-Introduction|01-Introduction]] — Git vs GitHub vs Azure Repos
- [[02-Repository-Setup]] — Repo creation, .gitignore, branch protection
- [[05-Core-Workflow|03-Core-Workflow]] — PR workflow, code review checklist
- [[03-GitHub-Actions-Commands-Reference|GitHub-Actions-Commands-Reference]] — GitHub Actions pipeline syntax reference
- [[06-GitHub-Actions-Terraform-OIDC|GitHub-Actions-Terraform-OIDC]] — Full CI/CD flow using Git + GitHub Actions
