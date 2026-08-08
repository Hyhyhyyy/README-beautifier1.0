---
name: github-readme-beautify
description: "Beautify one or more GitHub repository READMEs with an animated hero banner (a standalone SVG using SMIL animation that plays inline in GitHub), architecture or flow diagrams, badges, and structured feature tables, then push those assets to GitHub. Trigger phrases include 美化 GitHub README, 给仓库加动画横幅, beautify my repos, add a banner to my README, GitHub 仓库 README 配图, or any request to standardize or polish multiple repo landing pages."
agent_created: true
---

# GitHub README Beautify

Generate a consistent, animated, on-brand README for one or many GitHub repos and
push it. The visual centerpiece is a **1280×380 hero banner as a standalone SVG using
SMIL animation** — GitHub strips inline `<style>`/`<script>` but keeps `<img
src="banner.svg">` and renders its SMIL animations, so the banner moves inside the
README with zero JS.

## When to use
- "美化我的 GitHub README / 给每个仓库加动画横幅"
- Standardize the look of several repos at once
- Add architecture/flow diagrams and feature tables to a repo landing page

## Prerequisites
- `gh` authenticated (`gh auth status`).
- System Python 3.12 at `/c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe`
  (the managed 3.13 writes to an invisible sandbox — see gotchas).
- `git` and network access to GitHub.

## Workflow

### Step 1 — Inventory and scope
List the target repos and **exclude the profile repo** (`OWNER` itself). Inspect each
repo's real tree and default branch before generating, because content may live in a
subdirectory (e.g. `KeLing2.0` → `Desktop/KeLing/`, branch `master`):

```bash
gh api repos/OWNER/REPO/contents/ --jq '.[].name'
gh api repos/OWNER/REPO --jq '.default_branch'
```
 Record, per repo: default branch, target path for `README.md` + `banner.svg`
(+ `diagrams/` if a diagram applies).

### Step 2 — Generate animated banners
Each repo needs one entry in the `THEMES` dict in `scripts/gen_banners.py`
(see `references/themes-and-adaptation.md` for the field schema and the 8 built-in
MOTIFS: hex, terminal, disc, orbit, doc, shield, tomato, token). Add/adjust entries, then:

```bash
python scripts/gen_banners.py RepoKey > banner.svg
```
 The output is a self-contained SMIL SVG (floating orbs, moving streaks, rotating
ring, title slide-in, underline draw). A sample is in `assets/sample-banner.svg`.

### Step 3 — Generate architecture / flow diagrams (optional but recommended)
For technical repos, add a function to the `DIAGRAMS` dict in
`scripts/gen_diagrams.py` (start from the shipped `chainpass` / `keling` /
`train_guard` / `md_converter` / `tomatomaa` / `tokensaver` templates) and run:

```bash
python scripts/gen_diagrams.py RepoKey > diagrams/RepoKey.svg
```

### Step 4 — Build the enhanced README
Add a builder to `BUILDERS` in `scripts/gen_readmes.py`. Each builder composes
`banner_img()` + `badge_row()` + `feature_table()` and re-embeds the **original**
README body (its first `# Title` is stripped to avoid duplication). Place original
READMEs as `<BASE>/<RepoName>.md` (`BASE` = cwd, or set `README_BASE`):

```bash
python scripts/gen_readmes.py RepoName > README.md
```

### Step 5 — Push
Prefer the git-clone-then-commit method (robust for multiple files; avoids API
path/sandbox issues). See `references/verification.md` for the exact commands and the
note about subdirectory repos. If `git clone` returns HTTP 403 "repository is
disabled" / "Repository has been locked", **stop** — the repo is locked (the `disabled`
API flag lies). Keep assets local and push after the lock is lifted.

### Step 6 — Verify remotely
Confirm the **remote** banner still contains SMIL (GitHub keeps it, but verify) and
that the README references it:

```bash
gh api repos/OWNER/REPO/contents/banner.svg --jq '.content' \
  | /c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe \
      -c "import base64,sys; print(base64.b64decode(sys.stdin.read()).decode())" \
  | grep -c -E '<animate|<animateTransform|<animateMotion'
```
 Expect a positive count (reference banners carry 19–38 SMIL tags). Details in
`references/verification.md`.

## Critical environment rules (read before executing)
All are in `references/environment-gotchas.md`. The most common failures:
1. **Git Bash has no `base64`** → decode with system Python (pattern above).
2. **Managed Python 3.13 writes to an invisible sandbox** → use system Python 3.12 and
   the "Python stdout → Bash `>` redirect" pattern.
3. **Never pass `/c/...` to Windows Python `open()`** (FileNotFoundError).
4. **Avoid `rm -rf`** (sandbox safe-delete fails) — clone to a fresh dir name instead.
5. **GitHub keeps SMIL in `<img src="*.svg">` but strips inline `<style>`/`<script>`** —
   always commit a separate `banner.svg`, never inline it.
6. **`gh api .disabled` is unreliable** — a real write attempt is the only truth for locks.

## References
- `references/environment-gotchas.md` — Windows/Git Bash/GitHub pitfalls, with commands.
- `references/themes-and-adaptation.md` — THEMES/MOTIFS/BUILDERS/DIAGRAMS schema + how to add a repo.
- `references/verification.md` — validate SVG, confirm remote SMIL, push commands, QA render.

## Scripts
- `scripts/gen_banners.py` — animated SMIL hero banner generator (data-driven via THEMES).
- `scripts/gen_diagrams.py` — static architecture/flow SVG diagrams (data-driven via DIAGRAMS).
- `scripts/gen_readmes.py` — enhanced README builder (data-driven via BUILDERS).
- `scripts/render_qa.js` — optional static-frame PNG render via `@resvg/resvg-js` (layout QA only; no SMIL).

## Success criteria
- Every targeted repo's README opens with the animated `banner.svg`.
- Technical repos include a `diagrams/*.svg` reference where applicable.
- Remote `banner.svg` retains SMIL animation tags (verified in Step 6).
- Consistent visual language across all repos (shared banner anatomy, per-repo palette).
