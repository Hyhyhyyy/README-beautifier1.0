# Environment Gotchas (Windows / Git Bash / GitHub)

These are hard-won lessons from running this workflow on Windows + Git Bash.
Read this before executing any step — most failures here are environment, not logic.

## 1. Git Bash has no `base64`
`base64: command not found`. When you need to decode (e.g. `gh api` returns
base64 `content`), use system Python instead of the missing shell command:

```bash
gh api repos/OWNER/REPO/contents/banner.svg --jq '.content' \
  | /c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe \
      -c "import base64,sys; print(base64.b64decode(sys.stdin.read()).decode())"
```

## 2. Managed Python 3.13 writes into a sandbox invisible to Bash/Node
The WorkBuddy-managed Python (`~/.workbuddy/binaries/python/...`) writes files into
an isolated sandbox that Bash and Node **cannot see**. Use the **system** Python 3.12:

```
/c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe
```

And prefer the pattern **"Python prints to stdout → Bash `>` redirect"** to land
files on the real filesystem, rather than having Python write files directly.

## 3. Don't pass Bash `/c/...` paths into Windows Python `open()`
A path like `/c/Users/...` passed to Windows Python's `open()` raises
`FileNotFoundError` (Windows doesn't understand the `/c/` prefix). Either:
- Run Python from Git Bash and let it resolve `/c/...` → it usually works for reading,
  but for safety prefer generating via stdout + Bash redirect, or
- Pass Windows-style paths (`C:\Users\...`) when calling Windows Python directly.

## 4. Avoid `rm -rf` (sandbox safe-delete failure)
`rm -rf /tmp/...` triggers a sandbox safe-delete failure. Instead of deleting a stale
clone, just **clone into a fresh directory name** (e.g. `_clone/repo2`). Never force
`rm -rf` on personal/system directories.

## 5. GitHub README animation rule (CRITICAL)
GitHub **strips inline `<style>` and `<script>`** from READMEs (and most rendered
Markdown). BUT it **keeps `<img src="*.svg">`** and **renders SMIL animations**
(`<animate>`, `<animateTransform>`, `<animateMotion>`) inside that SVG.

✅ Correct: commit a `banner.svg` file and reference it:
```md
<p align="center"><img src="banner.svg" alt="..." width="100%"></p>
```
❌ Wrong: inline `<svg>...<style>...</style></svg>` directly in the README — styles
   are stripped, animation dies.

Verify the remote SVG still has animations after push (gotcha #1 + grep `<animate`).

## 6. `gh api` `disabled` field is unreliable
`gh api repos/OWNER/REPO --jq '.disabled'` may return `false` even when the repo is
actually **locked**. The authoritative signal is a real write attempt:
- `git clone` → `remote: Your repository is disabled.` / HTTP 403
- `gh api -X PUT .../contents/file` → `{"message":"Repository has been locked."}`

If you see either, the repo cannot be modified until the owner lifts the lock in
GitHub Settings or resolves a DMCA/ToS flag via Support. Prepare the assets locally
and push later.

## 7. Repo root ≠ repo content
Some repos keep code in a subdirectory (e.g. `KeLing2.0` lives under
`Desktop/KeLing/`, default branch `master`). The enhanced README + `banner.svg` must
go to that subpath, not the repo root. Always inspect the real tree:

```bash
gh api repos/OWNER/REPO/contents/ --jq '.[].name'
gh api repos/OWNER/REPO --jq '.default_branch'
```

## 8. Topics API works even when pushes don't
`gh api -X PUT /repos/OWNER/REPO/topics -f names[]=...` can succeed for a locked repo
where file writes fail. Use it to at least set topics.

## 9. SVG QA rendering
`resvg` (`@resvg/resvg-js`, installed under the managed Node workspace) rasterizes SVG
to PNG for local QA. It does **not** run SMIL (static frame), so it only checks layout,
not animation. Reference: `scripts/render_qa.js`.
