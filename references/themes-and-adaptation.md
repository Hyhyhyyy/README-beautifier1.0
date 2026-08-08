# Themes, Motifs & Adaptation Guide

The skill ships three generator scripts. Each is **data-driven**: you edit a dict to
add a repo, then run the script. No code logic changes needed for a new project.

## A. Banners — `scripts/gen_banners.py`

Add a repo to the `THEMES` dict. Each entry:

```python
"RepoKey": dict(
    name="RepoKey",            # used for SVG gradient ids (unique, no spaces)
    title="My Project",        # big hero text
    subtitle="One-line tagline",
    bg=["#0b1220","#0f172a","#1e1b4b","#0c4a6e"],  # 4-stop background gradient (top→bottom)
    orb=["#22d3ee","#818cf8","#34d399"],            # 3 floating orb colors
    accent="#22d3ee",          # streaks / ring / motif primary
    accent2="#a5b4fc",         # motif secondary
    title_grad=["#e0f2fe","#67e8f9","#a5b4fc"],     # 3-stop title text gradient
    sub="#cbd5e1",             # subtitle + footer text color
    motif="hex",               # one of: hex, terminal, disc, orbit, doc, shield, tomato, token
),
```

### Available MOTIFS (right-side graphic)
| motif | shape | best for |
|-------|-------|----------|
| `hex` | stacked hexagons, rotating | blockchain / identity / infra |
| `terminal` | terminal window w/ blinking cursor | CLI / dev tools |
| `disc` | vinyl disc, wobbling | media / music / content |
| `orbit` | planet + orbiting nodes | multi-platform / sync apps |
| `doc` | document + arrow | converters / docs / SaaS |
| `shield` | shield + check draw | security / guard / reliability |
| `tomato` | red tomato + green calyx, breathing | habit / health / food / playful |
| `token` | gold coin + downward savings arrow + orbiting coins | economy / cost-saving / token / finance |

To add a new motif: write a `motif_<name>(accent, accent2)` function returning an SVG
`<g>` and register it in `MOTIFS`.

Run: `python gen_banners.py RepoKey > banner.svg` (or omit arg to print all).

## B. Diagrams — `scripts/gen_diagrams.py`

Add a repo to the `DIAGRAMS` dict mapping a key to a function that returns an SVG
string. Ships with: `chainpass()` (3-layer architecture), `keling(ver)` (multi-end),
`train_guard()` (workflow + interfaces + safety boundary + exit codes),
`md_converter()` (conversion flow), `tomatomaa()` (3-layer WeChat Mini Program +
CloudBase), `tokensaver()` (3-column backend optimization pipeline).

For a new repo, copy the nearest existing function and edit boxes/labels. Keep
`W,H = 920,560` and the shared `defs()/box()/arrow()/label()` helpers.

Run: `python gen_diagrams.py RepoKey > diagrams/RepoKey.svg`

## C. READMEs — `scripts/gen_readmes.py`

Add a repo to the `BUILDERS` dict: `"RepoName": lambda o: build_xxx(o)`. Each builder:
1. Composes badge rows via `badge_row([(label, color, value, url_or_None), ...])`
   — color is a shields.io color name; `value` may contain `%20` for spaces.
2. Composes a feature table via `feature_table([(icon_title, desc), ...])`.
3. Reads the **original** README from `<BASE>/<RepoName>.md`, strips its first
   `# Title` heading (to avoid duplication under the banner), and embeds the
   preserved body.
4. Injects `banner_img(...)` at the top and a `diagrams/...svg` reference where useful.

`BASE` defaults to the current directory; set `README_BASE` env to point at a folder
of original READMEs.

Run: `python gen_readmes.py RepoName > README.md`

## D. Generalizing to a new user
1. Replace the `THEMES` / `BUILDERS` / `DIAGRAMS` dicts with your own repos.
2. Point `BASE`/`README_BASE` at your originals folder (or cwd).
3. Output dirs default next to the scripts; override with `OUT` / `README_BASE` env.
4. The generator logic (orbs, streaks, motifs, badge/table helpers) is reusable as-is.
