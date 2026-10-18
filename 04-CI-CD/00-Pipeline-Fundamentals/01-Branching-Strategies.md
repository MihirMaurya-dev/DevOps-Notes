---
tags: [git, ci-cd, branching, code-management]
source: devopsinsiders/batch-18
created: 2026-06-08
updated: 2026-06-20
---

# 🌿 Git Branching Strategies — Complete Guide in Simple Language

---

## 🤔 What is a Branching Strategy?

Think of Git like a river. The main river is your `main` branch — the production-ready code. When developers want to add a new feature, they "branch off" into a small stream (a feature branch), do their work, and then merge back into the main river.

A **branching strategy** is the set of rules your team follows about:
- How many branches to have
- How long branches live
- Who can merge into which branches
- When and how to release code

**Why does it matter?** Choose the wrong strategy and you'll spend more time fighting merge conflicts and broken builds than actually building features. Choose the right one and code flows smoothly from developer laptops to production.

---

## 📊 The 3 Main Strategies — At a Glance

| Strategy | Branches | Complexity | Best For |
|----------|----------|------------|---------|
| **Trunk-Based Development** | 1 main + short-lived features | Low | CI/CD, Terraform, modern DevOps |
| **GitHub Flow** | 1 main + feature branches | Low-Medium | Web apps, open source |
| **GitFlow** | 5+ permanent branch types | High | Software with version releases |

---

## 🛤️ Strategy 1: Trunk-Based Development (TBD) — The Modern Way

> 🏆 **This is the recommended strategy for DevOps, Terraform, and Kubernetes environments.**

### The Concept

Everyone works on one central branch (`main` or `trunk`). Developers create tiny, short-lived feature branches that live for **hours or a day at most**, then merge back to `main`.

```
main ──────────────────────────────────────────────────────────►
        │     │     │     │     │     │     │
       feat  feat  feat  feat  feat  feat  feat
      (2hrs) (4hrs)(1hr)(6hrs)(2hrs)(3hrs)(5hrs)
```

**The key rule:** Feature branches must be **short-lived**. A branch that lives more than 2 days is a problem. More than a week is a crisis.

### Why Short Branches?
- The longer a branch lives, the further it drifts from `main`
- More drift = more merge conflicts = "merge hell"
- Short branches force you to break work into small pieces (good practice!)
- Small PRs are easier to review (a 50-line change gets reviewed in 10 minutes; a 5,000-line change gets rubber-stamped)

### Feature Flags — How to Deploy Unfinished Features

"But what if my feature takes 2 weeks to build? Can't I keep the branch open?"

**No.** Use **Feature Flags** instead. Merge the incomplete code to `main`, but hide it behind a toggle:

```python
# Feature flag in code
if feature_flags.is_enabled("new-checkout-flow", user_id=user.id):
    return new_checkout_flow(cart)  # New (hidden from most users)
else:
    return old_checkout_flow(cart)  # Old (visible to everyone)
```

```yaml
# Feature flag service (e.g., Azure App Configuration)
# John and the dev team see the new feature: flag enabled
# Everyone else: flag disabled
feature_flags:
  new-checkout-flow:
    enabled: true
    user_rollout_percentage: 5  # Only 5% of users see it
```

This lets you merge to `main` continuously while controlling who sees what. When the feature is complete and tested, flip the flag to 100%.

### Example Workflow (TBD)

```bash
# Developer Alice works on "add-payment-validation" feature

# 1. Start fresh from latest main
git checkout main
git pull origin main

# 2. Create short-lived feature branch
git checkout -b feat/add-payment-validation

# 3. Make small, focused changes
# ... write code ...
git add .
git commit -m "feat: add card number Luhn check"
# ... more small commits ...

# 4. Open a Pull Request within hours (not days!)
# PR description: "Adds Luhn algorithm validation for credit card numbers"
# Reviewer approves, CI pipeline passes

# 5. Merge to main (squash merge for clean history)
git checkout main
git merge --squash feat/add-payment-validation
git push origin main

# 6. Branch is deleted immediately after merge
git branch -d feat/add-payment-validation

# CI/CD automatically deploys to production! 🚀
```

### Benefits of TBD
- ✅ **Zero merge hell** — branches are too young to drift far from main
- ✅ **Continuous integration** — every merge triggers CI/CD
- ✅ **Fast feedback** — you know if your code breaks something within minutes, not weeks
- ✅ **Simple to understand** — one main branch, keep it deployable

### Required Safety Net
TBD only works if you have **excellent automated testing**. If someone merges broken code to `main`, it blocks everyone. You need:
- Unit tests (fast, run on every commit)
- Integration tests (run on PR)
- Required PR approvals (at least 1 reviewer)
- Branch protection rules (can't force-push to main, can't merge without passing CI)

---

## 🌊 Strategy 2: GitHub Flow — The Lightweight Choice

### The Concept

GitHub Flow has one golden rule: **`main` must always be deployable.** That's it.

```
main ──────────────────────────────────────────────────────────►
       │──────────────────│         │──────│
       feat/login-redesign│         feat/  │
           (PR review +   │         email  │
            CI tests)     │         notif  │
                          ▼         (3 days)
                         merge        ▼
                        + deploy    merge
                                   + deploy
```

### The Workflow

```
1. Create branch from main (give it a descriptive name)
2. Commit changes to the branch
3. Open a Pull Request (PR) — this starts conversation and CI
4. Review and discuss the PR
5. (Optional) Deploy the branch to a staging environment for testing
6. Merge to main
7. Deploy main to production immediately after merge
```

### Difference from TBD

| | Trunk-Based Development | GitHub Flow |
|-|------------------------|-------------|
| **Branch lifetime** | Hours | Days (but not weeks) |
| **Feature flags** | Heavy use | Optional |
| **Deploy timing** | Every merge, immediate | Every merge, immediate |
| **Strictness** | More strict (daily merges) | More flexible |

**GitHub Flow is a relaxed version of TBD** — you still have short-lived branches and `main` is always deployable, but it doesn't force you to merge daily.

### Best for
- Web applications with continuous deployment
- Open source projects (contributors work at their own pace)
- Small-to-medium teams

---

## 🏛️ Strategy 3: GitFlow — The Traditional (Heavy) Model

### The Concept

GitFlow was published in 2010 by Vincent Driessen. It was designed for teams releasing **versioned software** (like a mobile app or a game) that has scheduled release cycles.

It has **5 types of branches**, each with strict rules:

```
                    GITFLOW BRANCH STRUCTURE
─────────────────────────────────────────────────────────────
main   ●─────────────────────────────────────────● v2.0
       │                                         │
hotfix │                    ●────── ─────────────●
       │                    │ v1.1               │
develop●─────●──────────────●────────────────────●──────►
             │              │
             │  ●─────────●  ●─────────────────●
             │  feature/A │  release/2.0       │
             │            │                    │
             │  ●─────────●  Tests, bugfixes   │
             │  feature/B                      │
─────────────────────────────────────────────────────────────
```

### The 5 Branch Types

| Branch | Purpose | Lifetime | Branched From | Merges Into |
|--------|---------|----------|---------------|-------------|
| `main` | Stores official releases. Always stable. | Permanent | — | — |
| `develop` | Integration branch. All features merge here. | Permanent | `main` | — |
| `feature/xyz` | Individual features | Weeks-Months | `develop` | `develop` |
| `release/x.y` | Release preparation (bug fixes, version bump) | Days | `develop` | `main` + `develop` |
| `hotfix/xyz` | Emergency fixes for production bugs | Hours | `main` | `main` + `develop` |

### A Feature's Journey in GitFlow

```bash
# 1. Start a new feature
git checkout develop
git checkout -b feature/user-authentication

# Work for 2-3 weeks...
git commit -m "feat: add user registration"
git commit -m "feat: add JWT token generation"
git commit -m "feat: add password hashing"

# 2. Feature complete — merge to develop
git checkout develop
git merge --no-ff feature/user-authentication
git branch -d feature/user-authentication

# 3. When enough features are ready, create a release branch
git checkout develop
git checkout -b release/1.2
# Fix any release-specific bugs, update version numbers
git commit -m "bump version to 1.2"

# 4. Release is ready — merge to main AND back to develop
git checkout main
git merge --no-ff release/1.2
git tag -a v1.2 -m "Version 1.2"

git checkout develop
git merge --no-ff release/1.2
git branch -d release/1.2

# 5. Emergency bug in production — use hotfix
git checkout main
git checkout -b hotfix/critical-login-bug
# Fix the bug
git checkout main
git merge --no-ff hotfix/critical-login-bug
git tag -a v1.2.1
git checkout develop
git merge --no-ff hotfix/critical-login-bug
```

### GitFlow: The Honest Assessment

**GitFlow was great in 2010.** Today:

- ✅ **Good for:** Mobile apps, firmware, desktop software, video games — anything with versioned, scheduled releases
- ❌ **Bad for:** Web apps, APIs, infrastructure (Terraform), microservices — anything that deploys continuously

**Why GitFlow is painful for modern DevOps:**
- Feature branches live for weeks → massive merge conflicts
- You can't practice "Continuous Deployment" with GitFlow (releases are batched)
- Teams spend more time managing branches than writing code
- Hotfixes must be merged to BOTH main AND develop — easy to forget, causes bugs

> 💡 **Vincent Driessen (the creator of GitFlow) himself added a note to his original article in 2020:**
> "If your team is doing continuous delivery of software, I would suggest to adopt a much simpler workflow (like GitHub flow) instead of trying to shoehorn git-flow into your team."

---

## 🏗️ Branching Strategy for Terraform/IaC

For infrastructure code (Terraform, Bicep), the recommendation is clear:

**Use Trunk-Based Development or GitHub Flow.** Here's why:

1. **Infrastructure is always "deployed" to a real environment** — unlike application code, you can't keep it in staging indefinitely. The sooner you merge and apply, the sooner you know if it works.

2. **Long-lived infrastructure branches create drift** — if your `feature/add-new-vnet` branch lives for 2 weeks while other changes merge to `main`, the Terraform state will be out of sync by the time you merge.

3. **Terraform workspaces handle environments** — you don't need `develop/staging/prod` branches. Use Terraform workspaces or separate state files for dev/staging/prod.

**Recommended pattern:**
```
main ──────────────────────────────────────────────►
  │  All infra changes flow through PRs
  │  
  ├── feat/add-vnet (lives < 2 days)
  ├── fix/adjust-nsg-rules (lives < 1 day)  
  └── feat/new-aks-node-pool (lives < 2 days)

On merge to main:
→ Pipeline runs terraform plan (for review)
→ After approval: terraform apply to dev
→ After validation: terraform apply to staging  
→ After approval gate: terraform apply to prod
```

---

## 📋 Branch Protection Rules — Non-Negotiable

Whatever strategy you choose, **always protect your main branch** with these rules:

```
GitHub: Settings → Branches → Add Rule

Branch name pattern: main

✅ Require a pull request before merging
  ✅ Require approvals: 1 (minimum)
  ✅ Dismiss stale pull request approvals when new commits are pushed

✅ Require status checks to pass before merging
  ✅ (Add your CI pipeline jobs here)
  ✅ Require branches to be up to date before merging

✅ Require conversation resolution before merging

✅ Do not allow bypassing the above settings
```

In Azure DevOps, these are called **Branch Policies** (under Repos → Branches → Branch Policies).

---

## 🎯 Quick Decision Guide

Answer these questions to pick your strategy:

```
Do you release software on a fixed schedule (monthly, quarterly)?
  → YES: GitFlow
  → NO: Continue...

Do you deploy to production multiple times per day?
  → YES: Trunk-Based Development
  → NO: Continue...

Is your team small (<10 devs) or open source?  
  → YES: GitHub Flow
  → NO: Trunk-Based Development (with feature flags)
```

---

## 🎯 Key Takeaways

1. **Trunk-Based Development is the gold standard for modern DevOps** — short-lived branches, CI/CD on every merge
2. **GitHub Flow is a good middle ground** — simpler, `main` always deployable
3. **GitFlow is for versioned software** — not for infrastructure, web apps, or anything continuously deployed
4. **Feature flags > long-lived branches** — merge early, hide with flags, release safely
5. **For Terraform/IaC: always use TBD or GitHub Flow** — infrastructure must flow continuously
6. **Always protect `main`** — require PRs, require CI to pass, require approvals
7. **Short PRs get reviewed. Long PRs get rubber-stamped.** Break work into small pieces.
