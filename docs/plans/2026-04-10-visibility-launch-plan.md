# Visibility Launch Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Repackage RepoScale for public alpha visibility with a clearer README, repo-native visuals, and reusable launch copy.

**Architecture:** Keep the work repo-native and low-risk. Use Markdown and SVG so assets are versioned, lightweight, and editable without external design tooling. Add a launch kit document instead of scattering copy across issues or PR comments.

**Tech Stack:** Markdown, SVG, GitHub repository metadata conventions

---

### Task 1: Reframe the README hero and structure

**Files:**
- Modify: `README.md`

**Step 1: Rewrite the top section**

Replace the current abstract opening with a direct alpha-facing headline, supporting line, and proof-point block.

**Step 2: Add a "What you get today" section**

Include concise proof points for corpus size, tracks, CLI pipeline, and judge stability.

**Step 3: Simplify quickstart**

Reduce the quickstart to the minimal path that proves the project works.

**Step 4: Add alpha caveats**

Explicitly state the limits: alpha status, expanding corpus, and evolving methodology.

**Step 5: Verify**

Run: `sed -n '1,220p' README.md`
Expected: fast-scan structure with stronger launch framing.

### Task 2: Add repo-native visual assets

**Files:**
- Create: `docs/assets/readme-overview.svg`
- Create: `docs/assets/social-preview.svg`

**Step 1: Create README visual**

Build an SVG with pipeline flow and alpha proof points.

**Step 2: Create social preview visual**

Build an SVG optimized for GitHub sharing with title, subtitle, and benchmark stats.

**Step 3: Embed README visual**

Reference the README asset from `README.md`.

**Step 4: Verify**

Run: `find docs/assets -maxdepth 1 -type f | sort`
Expected: both SVG files exist.

### Task 3: Add launch kit and metadata guidance

**Files:**
- Create: `docs/launch-kit.md`
- Modify: `README.md`

**Step 1: Add launch kit**

Include GitHub release copy, X copy, LinkedIn copy, topic list, and public launch checklist.

**Step 2: Link the launch kit from README**

Make it discoverable for maintainers.

**Step 3: Verify**

Run: `sed -n '1,240p' docs/launch-kit.md`
Expected: reusable copy and actionable metadata guidance.

### Task 4: Final verification

**Files:**
- Modify: `README.md`
- Modify: `docs/assets/readme-overview.svg`
- Modify: `docs/assets/social-preview.svg`
- Modify: `docs/launch-kit.md`

**Step 1: Check repo status**

Run: `git status --short`
Expected: only intended files changed.

**Step 2: Smoke-test docs references**

Run: `rg -n "launch-kit|readme-overview.svg|social-preview.svg" README.md docs`
Expected: links resolve to the new assets/docs.

**Step 3: Commit**

```bash
git add README.md docs/assets/readme-overview.svg docs/assets/social-preview.svg docs/launch-kit.md docs/plans/2026-04-10-visibility-launch-design.md docs/plans/2026-04-10-visibility-launch-plan.md
git commit -m "docs: package alpha launch visuals and repo messaging"
```
