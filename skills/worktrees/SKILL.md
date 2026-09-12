---
name: worktrees
description: >-
  Isolated git worktrees for feature work. Use when starting work that needs
  isolation from the current workspace, when the tree is dirty or conflicts
  with the task, or before executing a multi-step implementation plan.
---

# Worktrees

Keep implementation off the user's active checkout when isolation helps.
Detect existing isolation first. Place new worktrees under
`D:/worktrees/<repo-name>/`. Prefer native harness worktree tools when they
can use that location; otherwise use `git worktree`.

## Step 0: Detect existing isolation

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

Submodule guard — `GIT_DIR != GIT_COMMON` is also true inside submodules:

```bash
git rev-parse --show-superproject-working-tree 2>/dev/null
```

| State | Action |
|-------|--------|
| Linked worktree (not submodule) | Use it. Do not nest another. |
| Submodule or normal checkout | Continue to create (with consent if needed) |
| User already declared preference | Honor it; don't re-ask |
| User declines isolation | Work in place |

Consent prompt when preference is unknown:

> Would you like an isolated worktree? It keeps your current branch untouched.

## Step 1: Create

### 1a. Native tool (preferred)

If the harness exposes worktree creation (`EnterWorktree`, `/worktree`,
`--worktree`, etc.) **and** can place the tree under
`D:/worktrees/<repo-name>/`, use it. Skipping a capable native tool creates
state the harness cannot manage. If it would put the tree somewhere else,
use the git fallback below.

### 1b. Git fallback

Only when no native tool exists.

Default location is **outside** the repo: `D:/worktrees/<repo-name>/<branch>`,
where `<repo-name>` is the lowercase basename of the git toplevel (Synapse →
`D:/worktrees/synapse`).

**Directory priority:** explicit user preference → `D:/worktrees/<repo-name>/`.

```bash
REPO_NAME=$(basename "$(git rev-parse --show-toplevel)" | tr '[:upper:]' '[:lower:]')
LOCATION="D:/worktrees/$REPO_NAME"
mkdir -p "$LOCATION"
path="$LOCATION/$BRANCH_NAME"
git worktree add "$path" -b "$BRANCH_NAME"
cd "$path"
```

The default path is not inside the working tree, so it does not need to be
gitignored. If the user prefers an in-repo directory, that path **must** be
gitignored before creating (`git check-ignore -q <dir>`); if not ignored, add
it to `.gitignore`, commit that change, then proceed.

Sandbox/permission failure → report it, work in place instead.

## Step 2: Setup + baseline

Run project setup if needed (`npm install`, `cargo build`, `pip install`,
`poetry install`, `go mod download`).

Run the project's normal test command once. Failures → report and ask whether
to proceed or investigate. Pass → ready.

```
Worktree ready at <path> on <branch>
Baseline: <pass | fail summary>
```

## Quick reference

| Situation | Action |
|-----------|--------|
| Already in linked worktree | Skip creation |
| Native tool can use `D:/worktrees/<repo-name>/` | Use it |
| No native tool | `git worktree add` under `D:/worktrees/<repo-name>/` |
| In-repo dir not ignored | Fix `.gitignore` first |
| Create blocked | Work in place |
| Baseline fails | Report + ask |
