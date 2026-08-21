---
name: git-broken-submodule-recovery
description: Diagnose and fix broken git submodules that prevent normal file operations — when a directory is tracked as a submodule in the index but has no .gitmodules entry, missing submodule repo, or causes "in submodule" errors.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [git, submodule, troubleshooting, repo-repair]
    category: github
    related_skills: [github-pr-workflow, github-repo-management]
triggers:
  - "git-broken-submodule-recovery"

---

# Git Broken Submodule Recovery

When git operations fail with "路徑規格 'X' 在子模組 'Y' 中" (pathspec is within submodule Y), or git add fails because a directory is treated as a submodule, use this skill to diagnose and fix.

## Diagnosis First

```bash
# Check if a path is tracked as a submodule in HEAD
git ls-tree HEAD <path>

# If mode is 160000 → it's a submodule commit in the index
# If mode is 100644 or 100755 → it's a regular file/directory

# Example output for submodule:
# 160000 commit abc1234  skills
#                    ↑ mode 160000 = submodule

# Check if .gitmodules has the submodule
git config --get-regexp "submodule\." 2>/dev/null

# Check if .git/modules/ exists (submodule working directory)
ls -la .git/modules/ 2>/dev/null || echo "no .git/modules"

# Check git index status for the path
git status --short <path>
```

## The Problem Pattern

You see errors like:
```
fatal: 路徑規格 'skills/hv-analysis' 在子模組 'skills' 中
fatal: 位於未簽出的子模組 'skills'
git ls-tree HEAD skills/ shows: 160000 commit <sha>  skills
But .gitmodules has NO entry for 'skills'
```

This means: the directory is registered as a submodule in git's index, but:
1. The submodule's repo doesn't exist or is empty
2. The .gitmodules file doesn't have an entry for it
3. `git submodule update --init` fails because there's no URL to clone

## Fix: Convert Submodule to Regular Directory

### Step 1: Remove submodule tracking from index

```bash
git rm --cached <path>
# Example: git rm --cached skills

# This removes the submodule index entry without deleting local files
```

### Step 2: Verify files still exist locally

```bash
ls <path>
# Files should still be there
```

### Step 3: Re-add as regular directory

```bash
git add <path>/
# The trailing slash forces git to add contents as regular files
```

### Step 4: Commit and push

```bash
git status --short
git commit -m "refactor: convert <path>/ from broken submodule to regular directory"
git push origin <branch>
```

## Variant: Submodule Entry in .gitmodules But Broken

If `.gitmodules` has the entry but submodule is broken:

```bash
# Option A: Re-initialize the submodule
git submodule init
git submodule update --init --recursive

# Option B: Remove the .gitmodules entry and index entry
git submodule deinit <path>
git rm --cached <path>
git rm .gitmodules   # if this is the only submodule
git add . && git commit -m "remove broken submodule <path>"
```

## Variant: Nested Submodule Issue

If the error says "未簽出的子模組" (not checked out):

```bash
# Check which commit the submodule should be at
git ls-tree HEAD <path>

# Check current submodule state
git submodule status <path>

# Force checkout of the correct commit
cd <path>
git checkout <commit-sha-from-ls-tree>
cd ..
```

## Verification

After fixing, verify the directory is now a regular tracked directory:

```bash
git ls-tree HEAD <path>
# Should show regular files/dirs, NOT mode 160000

git status --short <path>
# Should show as untracked or staged files, not "位於子模組"

# Test that you can git add individual files
git add <path>/<file>
git status --short <path>
```

## Key Insight

`git ls-tree HEAD <path>` is the definitive diagnostic:
- **Mode 160000** = submodule (git link to another repo)
- **Mode 100644/100755** = regular file/directory

Even without a `.gitmodules` entry, git can still treat a directory as a submodule if it was added with `git submodule add` and then the `.gitmodules` was removed or the submodule repo became unavailable.

## References

- Git submodule docs: https://git-scm.com/book/en/v2/Git-Tools-Submodules
- `git ls-tree`: https://git-scm.com/docs/git-ls-tree
- `git rm --cached`: removes index entry without deleting working tree files
