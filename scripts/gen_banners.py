#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate animated hero banners (SMIL) for GitHub READMEs.

Usage:
    python gen_banners.py <RepoKey> [<RepoKey> ...]   -> prints each SVG to stdout
    python gen_banners.py                              -> prints all THEMES

To support a new repo, add an entry to the THEMES dict below (see
references/themes-and-adaptation.md). The banner is pure SVG + SMIL, so it
animates inside GitHub READMEs when referenced via <img src="banner.svg">.
"""
import os, sys, math, xml.dom.minidom as minidom

# Output dir defaults to ./banners next to this script; override with OUT env var.
OUT = os.environ.get("OUT", os.path.join(os.path.dirname(os.path.abspath(__file__)), "banners"))
os.makedirs(OUT, exist_ok=True)

W, H = 1280, 380

def esc(s): return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

# ---------- animated floating orbs ----------
def orbs(colors):
    parts = []
    # each orb: big blurred circle drifting + pulsing opacity
    specs = [
        (180, 120, 150, colors[0], 0.0, 40, 60),
        (1080, 90, 120, colors[1], 1.2, -30, 70),
        (980, 300, 170, colors[2], 0.6, 50, 55),
        (320, 320, 110, colors[1], 2.0, -25, 65),
    ]
    for i,(cx,cy,r,c,beg,dx,dur) in enumerate(specs):
        parts.append(f'''
  <circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" opacity="0.30">
    <animateTransform attributeName="transform" type="translate" values="0 0; {dx} {dx*0.4}; 0 0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1; 0.4 0 0.6 1" keyTimes="0;0.5;1"/>
    <animate attributeName="opacity" values="0.18;0.42;0.18" dur="{dur*0.8}s" begin="{beg}s" repeatCount="indefinite"/>
  </circle>''')
    return "\n".join(parts)

# ---------- moving light streaks ----------
def streaks(accent):
    return f'''
  <g opacity="0.12">
    <rect x="-300" y="150" width="300" height="3" fill="{accent}" transform="rotate(-18 0 150)">
      <animateTransform attributeName="transform" type="translate" values="-200 0; 1700 0" dur="9s" repeatCount="indefinite"/>
    </rect>
    <rect x="-300" y="250" width="220" height="2" fill="{accent}" transform="rotate(-18 0 250)">
      <animateTransform attributeName="transform" type="translate" values="-200 0; 1700 0" dur="13s" begin="2s" repeatCount="indefinite"/>
    </rect>
  </g>'''

# ---------- rotating faint ring behind title ----------
def ring(accent):
    return f'''
  <circle cx="320" cy="190" r="150" fill="none" stroke="{accent}" stroke-width="1.2" opacity="0.18" stroke-dasharray="6 14">
    <animateTransform attributeName="transform" type="rotate" from="0 320 190" to="360 320 190" dur="40s" repeatCount="indefinite"/>
  </circle>
  <circle cx="320" cy="190" r="110" fill="none" stroke="{accent}" stroke-width="1" opacity="0.12"/>'''

# ---------- animated underline (draw) ----------
def underline(grad_id):
    L = 360
    return f'''
  <line x1="80" y1="250" x2="{80+L}" y2="250" stroke="url(#{grad_id})" stroke-width="4" stroke-linecap="round" stroke-dasharray="{L}" stroke-dashoffset="{L}">
    <animate attributeName="stroke-dashoffset" values="{L};0;0" keyTimes="0;0.55;1" dur="1.8s" fill="freeze"/>
    <animate attributeName="opacity" values="0;1;1" keyTimes="0;0.2;1" dur="1.8s" fill="freeze"/>
  </line>'''

# ---------- title + subtitle ----------
def title_block(title, subtitle, grad_id, sub_color):
    # title slide-in + gentle float; subtitle fade-in
    return f'''
  <text x="80" y="200" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="66" font-weight="800" fill="url(#{grad_id})" letter-spacing="-1">
    <animateTransform attributeName="transform" type="translate" values="-40 12; 0 0; 0 0" keyTimes="0;0.5;1" dur="1.6s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1;0 0 1 1"/>
    <animate attributeName="opacity" values="0;1;1" keyTimes="0;0.5;1" dur="1.6s" fill="freeze"/>
    {esc(title)}
  </text>
  <text x="82" y="238" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" font-size="22" font-weight="500" fill="{sub_color}">
    <animate attributeName="opacity" values="0;0;1" keyTimes="0;0.5;1" dur="1.8s" fill="freeze"/>
    {esc(subtitle)}
  </text>'''

# ---------- motifs (right side) ----------
def motif_hex(accent, accent2=None):
    # 3 stacked hexagons
    cx, cy = 1040, 190
    s = 56
    def hexpts(cxx,cyy,rr):
        return " ".join(f"{cxx+rr*math.cos(math.radians(60*i-30)):.1f},{cyy+rr*math.sin(math.radians(60*i-30)):.1f}" for i in range(6))
    g = f'<g transform="translate({cx},{cy})">'
    for k,(rr,op) in enumerate([(s,0.9),(s*0.66,0.6),(s*0.32,0.4)]):
        g += f'<polygon points="{hexpts(0,0,rr)}" fill="none" stroke="{accent}" stroke-width="3" opacity="{op}"/>'
    g += f'''
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="36s" repeatCount="indefinite"/>
    <circle cx="{cx}" cy="{cy}" r="6" fill="{accent}"><animate attributeName="r" values="6;9;6" dur="3s" repeatCount="indefinite"/></circle>
  </g>'''
    return g

def motif_terminal(accent, accent2):
    cx, cy = 1050, 190
    g = f'''<g transform="translate({cx-130},{cy-70})">
    <rect x="0" y="0" width="260" height="140" rx="14" fill="#0b0f14" stroke="{accent}" stroke-width="2" opacity="0.95"/>
    <circle cx="20" cy="22" r="6" fill="#ef4444"/><circle cx="42" cy="22" r="6" fill="#f59e0b"/><circle cx="64" cy="22" r="6" fill="#22c55e"/>
    <text x="22" y="62" font-family="monospace" font-size="17" fill="{accent2}">$ train-guard</text>
    <text x="22" y="88" font-family="monospace" font-size="17" fill="#e5e7eb">run watch</text>
    <rect x="22" y="108" width="10" height="18" fill="{accent}"><animate attributeName="opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></rect>
  </g>'''
    return g

def motif_disc(accent, accent2):
    cx, cy = 1050, 190
    g = f'''<g transform="translate({cx},{cy})">
    <g>
      <ellipse cx="0" cy="0" rx="78" ry="30" fill="none" stroke="{accent}" stroke-width="10" opacity="0.95"/>
      <ellipse cx="0" cy="0" rx="78" ry="30" fill="none" stroke="{accent2}" stroke-width="3" opacity="0.7"/>
      <animateTransform attributeName="transform" type="rotate" from="-12 0 0" to="12 0 0" dur="2.4s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
    </g>
    <g stroke="{accent2}" stroke-width="3" opacity="0.6" stroke-linecap="round">
      <line x1="-110" y1="-40" x2="-150" y2="-55"><animate attributeName="opacity" values="0.1;0.7;0.1" dur="2s" repeatCount="indefinite"/></line>
      <line x1="110" y1="40" x2="150" y2="55"><animate attributeName="opacity" values="0.7;0.1;0.7" dur="2s" repeatCount="indefinite"/></line>
    </g>
  </g>'''
    return g

def motif_orbit(accent, accent2):
    cx, cy = 1050, 190
    g = f'''<g transform="translate({cx},{cy})">
    <circle cx="0" cy="0" r="40" fill="none" stroke="{accent}" stroke-width="3"/>
    <path d="M-12 -16 Q0 -28 12 -16 Q20 -2 12 14 Q0 26 -12 14 Q-20 -2 -12 -16 Z" fill="{accent2}" opacity="0.85"/>
    <g>
      <circle cx="120" cy="0" r="9" fill="{accent}"/>
      <circle cx="-120" cy="0" r="7" fill="{accent2}"/>
      <circle cx="0" cy="-120" r="6" fill="{accent}"/>
      <circle cx="0" cy="120" r="8" fill="{accent2}"/>
      <ellipse cx="0" cy="0" rx="120" ry="46" fill="none" stroke="{accent}" stroke-width="1.5" opacity="0.4"/>
      <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="30s" repeatCount="indefinite"/>
    </g>
  </g>'''
    return g

def motif_doc(accent, accent2):
    cx, cy = 1050, 190
    g = f'''<g transform="translate({cx-60},{cy-70})">
    <rect x="0" y="0" width="120" height="140" rx="12" fill="#0b1220" stroke="{accent}" stroke-width="3"/>
    <line x1="20" y1="34" x2="100" y2="34" stroke="{accent2}" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
    <line x1="20" y1="58" x2="100" y2="58" stroke="{accent2}" stroke-width="6" stroke-linecap="round" opacity="0.6"/>
    <line x1="20" y1="82" x2="76" y2="82" stroke="{accent2}" stroke-width="6" stroke-linecap="round" opacity="0.5"/>
    <g transform="translate(150,40)">
      <path d="M0 -22 L34 0 L0 22 L-12 10 L14 0 L-12 -10 Z" fill="{accent}">
        <animateTransform attributeName="transform" type="translate" values="0 0; 14 0; 0 0" dur="2.2s" repeatCount="indefinite"/>
      </path>
    </g>
    <rect x="150" y="60" width="60" height="76" rx="8" fill="#0b1220" stroke="{accent2}" stroke-width="3" opacity="0.9"/>
  </g>'''
    return g

def motif_shield(accent, accent2):
    cx, cy = 1050, 190
    path = "M0 -90 L70 -60 L70 20 Q70 80 0 100 Q-70 80 -70 20 L-70 -60 Z"
    g = f'''<g transform="translate({cx},{cy})">
    <path d="{path}" fill="#1c1917" stroke="{accent}" stroke-width="4" opacity="0.95"/>
    <path d="M0 -90 L70 -60 L70 20 Q70 80 0 100 Q-70 80 -70 20 L-70 -60 Z" fill="none" stroke="{accent2}" stroke-width="2" opacity="0.5">
      <animate attributeName="opacity" values="0.2;0.7;0.2" dur="3s" repeatCount="indefinite"/>
    </path>
    <path d="M-34 6 L-10 32 L40 -22" fill="none" stroke="{accent2}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round">
      <animate attributeName="stroke-dashoffset" values="120;0;0" keyTimes="0;0.6;1" dur="2.2s" fill="freeze"/>
      <animate attributeName="opacity" values="0;1;1" keyTimes="0;0.4;1" dur="2.2s" fill="freeze"/>
    </path>
  </g>'''
    return g

def motif_tomato(accent, accent2):
    # a friendly tomato: radial-gradient body, green calyx star, gentle sway + breathe
    cx, cy = 1050, 190
    g = f'''<g transform="translate({cx},{cy})">
    <defs>
      <radialGradient id="tom_body" cx="0.38" cy="0.30" r="0.92">
        <stop offset="0" stop-color="#fee2e2"/>
        <stop offset="0.42" stop-color="{accent}"/>
        <stop offset="1" stop-color="#991b1b"/>
      </radialGradient>
      <linearGradient id="tom_leaf" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#bbf7d0"/>
        <stop offset="1" stop-color="#15803d"/>
      </linearGradient>
    </defs>
    <circle cx="0" cy="0" r="98" fill="{accent}" opacity="0.10">
      <animate attributeName="r" values="90;104;90" dur="4.5s" repeatCount="indefinite"/>
    </circle>
    <g>
      <circle cx="80" cy="-58" r="5" fill="{accent2}" opacity="0.85">
        <animate attributeName="opacity" values="0.2;0.95;0.2" dur="2.4s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" values="0 0;5 -9;0 0" dur="3s" repeatCount="indefinite"/>
      </circle>
      <circle cx="-74" cy="52" r="4" fill="{accent2}" opacity="0.75">
        <animate attributeName="opacity" values="0.3;0.85;0.3" dur="3.1s" begin="0.6s" repeatCount="indefinite"/>
      </circle>
      <circle cx="0" cy="12" r="64" fill="url(#tom_body)"/>
      <ellipse cx="-20" cy="-12" rx="18" ry="11" fill="#ffffff" opacity="0.4"/>
      <path d="M0 -54 L13 -34 L34 -36 L21 -18 L33 2 L0 -6 L-33 2 L-21 -18 L-34 -36 L-13 -34 Z" fill="url(#tom_leaf)"/>
      <rect x="-3" y="-66" width="6" height="16" rx="3" fill="#166534"/>
      <animateTransform attributeName="transform" type="rotate" values="-5 0 32;5 0 32;-5 0 32" dur="3.6s" repeatCount="indefinite" calcMode="spline" keySplines="0.4 0 0.6 1;0.4 0 0.6 1" keyTimes="0;0.5;1"/>
      <animateTransform attributeName="transform" type="scale" values="1 1;1.035 1.035;1 1" dur="3.6s" repeatCount="indefinite" additive="sum"/>
    </g>
  </g>'''
    return g

def motif_token(accent, accent2):
    # glowing gold "token" coin with a descending savings arrow, orbiting coins + sparkles
    cx, cy = 1050, 190
    g = f'''<g transform="translate({cx},{cy})">
    <defs>
      <radialGradient id="coinGrad" cx="0.36" cy="0.30" r="0.9">
        <stop offset="0" stop-color="#fef9c3"/>
        <stop offset="0.5" stop-color="{accent2}"/>
        <stop offset="1" stop-color="#b45309"/>
      </radialGradient>
    </defs>
    <circle cx="0" cy="0" r="96" fill="{accent2}" opacity="0.10">
      <animate attributeName="r" values="86;104;86" dur="4.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" values="0.07;0.16;0.07" dur="4.2s" repeatCount="indefinite"/>
    </circle>
    <g>
      <circle cx="126" cy="-46" r="22" fill="url(#coinGrad)" stroke="{accent2}" stroke-width="2"/>
      <animateTransform attributeName="transform" type="rotate" from="0 0 0" to="360 0 0" dur="16s" repeatCount="indefinite"/>
    </g>
    <g>
      <circle cx="-128" cy="50" r="15" fill="{accent}" opacity="0.9"/>
      <animateTransform attributeName="transform" type="rotate" from="360 0 0" to="0 0 0" dur="20s" repeatCount="indefinite"/>
    </g>
    <g>
      <circle cx="0" cy="0" r="74" fill="url(#coinGrad)" stroke="{accent2}" stroke-width="3"/>
      <circle cx="0" cy="0" r="58" fill="none" stroke="{accent2}" stroke-width="1.5" opacity="0.55"/>
      <path d="M0 -32 L0 24 M-17 6 L0 28 L17 6" fill="none" stroke="{accent}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round">
        <animateTransform attributeName="transform" type="translate" values="0 -5;0 6;0 -5" dur="2.4s" repeatCount="indefinite"/>
      </path>
      <animateTransform attributeName="transform" type="scale" values="1 1;1.04 1.04;1 1" dur="3.4s" repeatCount="indefinite"/>
    </g>
    <circle cx="66" cy="-80" r="4" fill="{accent2}" opacity="0.85">
      <animate attributeName="opacity" values="0.2;0.95;0.2" dur="2.4s" repeatCount="indefinite"/>
    </circle>
    <circle cx="-72" cy="76" r="3" fill="{accent}" opacity="0.8">
      <animate attributeName="opacity" values="0.3;0.9;0.3" dur="3s" begin="0.5s" repeatCount="indefinite"/>
    </circle>
  </g>'''
    return g

MOTIFS = {
    "hex": motif_hex, "terminal": motif_terminal, "disc": motif_disc,
    "orbit": motif_orbit, "doc": motif_doc, "shield": motif_shield,
    "tomato": motif_tomato, "token": motif_token,
}

def banner(theme):
    name = theme["name"]
    title = theme["title"]; subtitle = theme["subtitle"]
    bg = theme["bg"]; orb = theme["orb"]; accent = theme["accent"]
    title_grad = theme["title_grad"]; sub = theme["sub"]; motif = theme["motif"]
    m2 = theme.get("accent2", accent)
    gid = f"g_{name}"
    # background gradient (vertical)
    bgstops = "".join(f'<stop offset="{i/(len(bg)-1):.2f}" stop-color="{c}"/>' for i,c in enumerate(bg))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="{esc(title)}">
  <defs>
    <linearGradient id="bg_{name}" x1="0" y1="0" x2="0.4" y2="1">
      {bgstops}
    </linearGradient>
    <linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{title_grad[0]}"/>
      <stop offset="0.5" stop-color="{title_grad[1]}"/>
      <stop offset="1" stop-color="{title_grad[2]}"/>
      <animate attributeName="x1" values="0;0.3;0" dur="8s" repeatCount="indefinite"/>
      <animate attributeName="x2" values="1;0.7;1" dur="8s" repeatCount="indefinite"/>
    </linearGradient>
    <filter id="blur_{name}" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="34"/>
    </filter>
    <clipPath id="clip_{name}"><rect x="0" y="0" width="{W}" height="{H}" rx="18"/></clipPath>
  </defs>
  <g clip-path="url(#clip_{name})">
    <rect x="0" y="0" width="{W}" height="{H}" fill="url(#bg_{name})"/>
    <g filter="url(#blur_{name})">
      {orbs(orb)}
    </g>
    {streaks(accent)}
    {ring(accent)}
    {MOTIFS[motif](accent, m2)}
    {underline(gid)}
    {title_block(title, subtitle, gid, sub)}
    <text x="{W-40}" y="{H-24}" text-anchor="end" font-family="'Segoe UI',Arial,sans-serif" font-size="14" fill="{sub}" opacity="0.55">made with &#10084; by Hyhyhyyy</text>
  </g>
</svg>'''
    return svg

# ----------------- themes -----------------
THEMES = {
 "ChainPass": dict(name="ChainPass", title="ChainPass", subtitle="跨境数字身份 · 合规支付 · 区块链信任层",
    bg=["#0b1220","#0f172a","#1e1b4b","#0c4a6e"], orb=["#22d3ee","#818cf8","#34d399"],
    accent="#22d3ee", accent2="#a5b4fc", title_grad=["#e0f2fe","#67e8f9","#a5b4fc"], sub="#cbd5e1", motif="hex"),
 "claude-code": dict(name="claude-code", title="claude-code", subtitle="An independent Python port of Claude Code",
    bg=["#070a0f","#0b0f14","#111827","#1f2937"], orb=["#f59e0b","#34d399","#fb923c"],
    accent="#fbbf24", accent2="#34d399", title_grad=["#fde68a","#fbbf24","#f59e0b"], sub="#d1d5db", motif="terminal"),
 "dlut-ultimate-website": dict(name="dlut", title="BLACK ANTS", subtitle="大连理工黑蚁极限飞盘队 · 官方网站",
    bg=["#052e16","#064e3b","#166534","#7c2d12"], orb=["#84cc16","#f97316","#fde047"],
    accent="#bef264", accent2="#fb923c", title_grad=["#ecfccb","#bef264","#fdba74"], sub="#dcfce7", motif="disc"),
 "KeLing2.0": dict(name="KeLing2", title="课灵 KeLing 2.0", subtitle="多端知识管理学习助手 · 培育你的知识星球",
    bg=["#1e0b3b","#2e1065","#4c1d95","#831843"], orb=["#c084fc","#f472b6","#a78bfa"],
    accent="#e9d5ff", accent2="#f472b6", title_grad=["#f5d0fe","#e9d5ff","#c4b5fd"], sub="#e9d5ff", motif="orbit"),
 "KeLing3.0": dict(name="KeLing3", title="课灵 KeLing 3.0", subtitle="多端知识管理学习助手 · 培育你的知识星球",
    bg=["#042f2e","#064e4a","#0f766e","#134e4a"], orb=["#2dd4bf","#5eead4","#34d399"],
    accent="#5eead4", accent2="#34d399", title_grad=["#ccfbf1","#99f6e4","#5eead4"], sub="#ccfbf1", motif="orbit"),
 "md-converter": dict(name="mdconv", title="md-converter", subtitle="Markdown → PDF / DOC · 一键优雅转换",
    bg=["#0c1f3f","#0f2557","#1e3a8a","#0e7490"], orb=["#38bdf8","#60a5fa","#a5f3fc"],
    accent="#7dd3fc", accent2="#a5f3fc", title_grad=["#e0f2fe","#bae6fd","#7dd3fc"], sub="#bfdbfe", motif="doc"),
 "train_guard": dict(name="train_guard", title="Train Guard", subtitle="LLM / VLM 训练守护 · 可靠观测与受控恢复",
    bg=["#1c1917","#292524","#7f1d1d","#451a03"], orb=["#f87171","#fbbf24","#fca5a5"],
    accent="#fca5a5", accent2="#fbbf24", title_grad=["#fee2e2","#fecaca","#fcd34d"], sub="#fecaca", motif="shield"),
 "TOMATOMATOO": dict(name="TOMATOMATOO", title="TOMATOMATOO", subtitle="一起养番茄 · 双人习惯养成小程序",
    bg=["#7f1d1d","#991b1b","#b91c1c","#c2410c"], orb=["#fca5a5","#fb923c","#f87171"],
    accent="#fca5a5", accent2="#fde68a", title_grad=["#fee2e2","#fecaca","#fca5a5"], sub="#fed7d7", motif="tomato"),
 "Token_Saver": dict(name="Token_Saver", title="SkillForge", subtitle="技能精炼台 · 让每一轮对话少花无效 Token",
    bg=["#0f172a","#134e4a","#064e3b","#1e293b"], orb=["#34d399","#fbbf24","#10b981"],
    accent="#34d399", accent2="#fbbf24", title_grad=["#a7f3d0","#6ee7b7","#fcd34d"], sub="#bbf7d0", motif="token"),
 "README-beautifier": dict(name="readmebeautifier", title="README Beautifier", subtitle="GitHub 仓库 README 一键美化 · 动画横幅 + 架构图 + 徽章",
    bg=["#1e1b4b","#312e81","#4338ca","#0e7490"], orb=["#a78bfa","#22d3ee","#f0abfc"],
    accent="#a78bfa", accent2="#22d3ee", title_grad=["#ede9fe","#c4b5fd","#67e8f9"], sub="#ddd6fe", motif="doc"),
}

if __name__ == "__main__":
    # usage: python gen_banners.py <RepoKey>   -> prints one SVG to stdout
    import sys
    names = sys.argv[1:] or list(THEMES.keys())
    for key in names:
        th = THEMES[key]
        svg = banner(th)
        minidom.parseString(svg)  # validate
        sys.stdout.write(svg)
