# Verification & Push

After generating assets and before/after pushing, verify correctness. GitHub's
renderer silently drops animations if the SVG is malformed or if you inlined it.

## 1. Validate SVG well-formedness (local)
Each generator already calls `xml.dom.minidom.parseString(svg)` before output, so a
crash means malformed XML. For extra safety re-validate written files:

```bash
/c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe -c \
  "import xml.dom.minidom,sys; xml.dom.minidom.parse(sys.argv[1]); print('OK', sys.argv[1])" banner.svg
```

## 2. Confirm SMIL animations survived the push (remote)
GitHub keeps SMIL, but verify the **remote** file (not just local) contains animate
tags. Use `gh api` + Python decode (Git Bash has no `base64`):

```bash
gh api repos/OWNER/REPO/contents/banner.svg --jq '.content' \
  | /c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe \
      -c "import base64,sys; print(base64.b64decode(sys.stdin.read()).decode())" \
  | grep -c -E '<animate|<animateTransform|<animateMotion'
```
Expect a positive count (the reference banners carry 19–20 animate tags).

## 3. Confirm the README references the banner
```bash
gh api repos/OWNER/REPO/contents/README.md --jq '.content' \
  | /c/Users/lenovo/AppData/Local/Programs/Python/Python312/python.exe \
      -c "import base64,sys; print(base64.b64decode(sys.stdin.read()).decode())" \
  | grep -c 'banner.svg'
```

## 4. Push method (preferred over API upload)
Git-clone-then-commit is more robust than the Contents API for multi-file pushes and
avoids path/sandbox pitfalls:

```bash
git clone --depth 1 https://github.com/OWNER/REPO.git _clone/repo
cp README.md _clone/repo/[README.md]            # adjust path (repo may use subdir)
cp banner.svg _clone/repo/[banner.svg]
cp -r diagrams _clone/repo/[diagrams]            # if diagrams exist
cd _clone/repo
git add -A
git commit -m "docs: add animated banner + architecture diagrams"
git push
```
Notes:
- Some repos keep files in a subdirectory (e.g. `Desktop/KeLing/`); place assets there.
- If a clone fails because the repo is **locked** (HTTP 403 "repository is disabled" /
  "Repository has been locked"), stop — see environment-gotchas.md #6. Prepare assets
  locally and push after the lock is lifted.
- Avoid `rm -rf` on stale clones; clone to a fresh directory name instead.

## 5. Optional QA render (static frame only)
`scripts/render_qa.js` uses `@resvg/resvg-js` to rasterize a PNG for layout review.
It does NOT execute SMIL, so it only validates geometry, not motion.

```bash
NODE_PATH=/c/Users/lenovo/.workbuddy/binaries/node/workspace/node_modules \
  /c/Users/lenovo/.workbuddy/binaries/node/versions/22.22.2/node.exe \
  scripts/render_qa.js banner.svg banner_qa.png
```
