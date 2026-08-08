#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate static architecture/workflow SVG diagrams for GitHub READMEs."""
import sys, math, xml.dom.minidom as minidom

W, H = 920, 560

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def defs():
    return f'''<defs>
    <filter id="sh" x="-8%" y="-8%" width="116%" height="116%">
      <feDropShadow dx="1" dy="2" stdDeviation="3" flood-opacity="0.10"/>
    </filter>
    <marker id="arr" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/>
    </marker>
    <marker id="arr-dk" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
      <polygon points="0 0, 10 3.5, 0 7" fill="#334155"/>
    </marker>
    <style>.t{{font-family:'Segoe UI','Helvetica Neue',Arial,sans-serif}} .lb{{font-size:12px;fill:#475569;font-weight:600}}</style>
  </defs>'''

def box(x,y,w,h,label,fill,stroke,text_color="#fff",fs=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="{fill}" stroke="{stroke}" stroke-width="1.5" filter="url(#sh)"/>\n<text x="{x+w/2}" y="{y+h/2+6}" text-anchor="middle" class="t" font-size="{fs}" font-weight="700" fill="{text_color}">{esc(label)}</text>'

def arrow(x1,y1,x2,y2,color="#64748b",mk="arr"):
    return f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="2" marker-end="url(#{mk})"/>'

def label(x,y,t):
    return f'<text x="{x}" y="{y}" class="lb">{esc(t)}</text>'

# ---------- ChainPass ----------
def chainpass():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    # bg
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#f8fafc"/>')
    # title
    parts.append(f'<text x="{W//2}" y="38" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#0f172a">ChainPass 系统架构</text>')
    # layers
    ly = [80, 210, 360]
    lh = [110, 130, 140]
    lnames = ["用户界面层", "服务层", "数据层"]
    lcolors = ["#e0f2fe","#fef3c7","#dcfce7"]
    llabels = [["Vue 3 Web App","Mobile App (预留)","开放 API"],["DID 服务","VC 服务","支付服务","KYC 服务"],["MySQL 8.0","Redis 7.0","模拟区块链"]]
    lfills = ["#0ea5e9","#d97706","#059669"]

    for i,(y,h,n,c,ls,fc) in enumerate(zip(ly,lh,lnames,lcolors,llabels,lfills)):
        parts.append(f'<rect x="30" y="{y}" width="{W-60}" height="{h}" rx="12" fill="{c}" stroke="#cbd5e1" stroke-dasharray="6 4" opacity="0.6"/>')
        parts.append(label(42, y+18, n))
        bw, bh = 150, 46
        gap = 18
        cols = len(ls)
        start_x = (W - 60 - cols*bw - (cols-1)*gap)//2 + 30
        for j,lbl in enumerate(ls):
            bx = start_x + j*(bw+gap)
            by = y + 36
            parts.append(box(bx,by,bw,bh,lbl,fc,"#fff" if fc in ["#0ea5e9","#059669"] else "#78350f", fs=13))
        if i < len(ly)-1:
            ny = y+h+4
            for j in range(cols):
                sx = start_x + j*(bw+gap)+bw//2
                ex = sx
                parts.append(arrow(sx, by+bh, ex, ny))
    parts.append('</svg>')
    return "\n".join(parts)

# ---------- KeLing multi-end ----------
def keling(ver):
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#f8fafc"/>')
    parts.append(f'<text x="{W//2}" y="36" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#0f172a">课灵 KeLing {ver} 多端架构</text>')
    # three main boxes
    boxes = [
        (40, 90, 240, 180, "Android 移动端\nKotlin · Jetpack Compose\nMaterial Design 3", "#7c3aed"),
        (340, 90, 240, 180, "后端服务器\nNode.js · Express · Prisma\nSQLite · JWT", "#0891b2"),
        (640, 90, 240, 180, "Web 网页端\nReact 18 · TypeScript\nVite · Zustand", "#059669"),
    ]
    for x,y,w,h,t,c in boxes:
        parts.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{c}" filter="url(#sh)"/>')
        lines = t.split("\n")
        ty = y + 45
        parts.append(f'<text x="{x+w//2}" y="{ty}" text-anchor="middle" class="t" font-size="17" font-weight="800" fill="#fff">{esc(lines[0])}</text>')
        for ln in lines[1:]:
            ty += 26
            parts.append(f'<text x="{x+w//2}" y="{ty}" text-anchor="middle" class="t" font-size="12" fill="#e2e8f0">{esc(ln)}</text>')
    # shared types at bottom
    sy = 320
    parts.append(box(W//2-120, sy, 240, 52, "shared 共享类型定义", "#64748b", "#334155", fs=14))
    # arrows
    cx1, cy1 = 160, 270; cx2, cy2 = 460, 270; cx3, cy3 = 760, 270
    mx, my = W//2, sy
    parts.append(arrow(cx1, cy1, 380, my-10))
    parts.append(arrow(cx3, cy1, 540, my-10))
    parts.append(arrow(cx2, cy2, cx2, sy-4))
    parts.append(arrow(mx-120, sy+52, cx1, cy1+20, mk="arr-dk"))
    parts.append(arrow(mx+120, sy+52, cx3, cy1+20, mk="arr-dk"))
    # features list
    fy = 410
    feats = [("✅ JWT 认证同步", 60), ("✅ 课程管理", 220), ("✅ 任务系统", 380), ("✅ 笔记同步", 540), ("✅ 签到记录", 700)]
    for txt,fx in feats:
        parts.append(label(fx, fy, txt))
    parts.append(label(60, 450, "🔄 数据实时同步"))
    parts.append('</svg>')
    return "\n".join(parts)

# ---------- train_guard workflow ----------
def train_guard():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#f8fafc"/>')
    parts.append(f'<text x="{W//2}" y="34" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#0f172a">Train Guard 工作流</text>')
    # flow steps
    steps = [
        ("init", "初始化配置", "#3b82f6"),
        ("doctor", "环境检查", "#8b5cf6"),
        ("data-check", "数据校验", "#ec4899"),
        ("watch", "训练观测", "#f59e0b"),
        ("check", "输出检查", "#ef4444"),
        ("manifest", "生成清单", "#10b981"),
    ]
    sw, sh = 130, 56
    gap = 24
    total_w = len(steps)*sw + (len(steps)-1)*gap
    sx = (W - total_w)//2
    sy = 70
    for i,(key, lbl, col) in enumerate(steps):
        x = sx + i*(sw+gap)
        parts.append(box(x,sy,sw,sh,lbl,col,"#fff",fs=13))
        parts.append(label(x+sw//2, sy+sh+16, key))
        if i < len(steps)-1:
            nx = x+sw+4
            parts.append(arrow(x+sw, sy+sh//2, nx, sy+sh//2, "#94a3b8"))
    # interfaces sidebar
    ix = 50; iy = 190
    iface = [
        ("CLI 命令行", "主要交互界面"),
        ("Python API", "程序化调用"),
        ("HF Callback", "Hugging Face 集成"),
        ("Web Dashboard", "Loopback 可视化"),
        ("SSH TUI", "远程终端面板"),
    ]
    parts.append(box(ix,iy,260,200,"接口 Interfaces","#1e293b","#e2e8f0",fs=15))
    ty = iy+35
    for nm,desc in iface:
        parts.append(f'<text x="{ix+18}" y="{ty}" class="t" font-size="13" font-weight="700" fill="#f1f5f9">{esc(nm)}</text>')
        ty += 22
        parts.append(f'<text x="{ix+18}" y="{ty}" class="t" font-size="11" fill="#94a3b8">{esc(desc)}</text>')
        ty += 28
    # safety boundary box
    sbx = 340; sby = 190
    parts.append(box(sbx,sby,530,200,"安全边界 Safety Boundary","#fef2f2","#991b1b",fs=15))
    safe_items = [
        "• 路径脱敏 — 不暴露绝对路径",
        "• 无遥测 — 默认不安装/上传",
        "• 不修改训练数据 — 只读观测",
        "• 受控恢复 — 仅显式 argv 重启",
        "• 本地优先 — Loopback 仅限本机",
    ]
    ty = sby+38
    for item in safe_items:
        parts.append(f'<text x="{sbx+20}" y="{ty}" class="t" font-size="12" fill="#7f1d1d">{esc(item)}</text>')
        ty += 26
    # exit codes
    ey = 430
    codes = ["0 PASS","1 WARN","2 FAIL","3 USAGE","4 CONFIG","5 RUNTIME","6 REFUSE"]
    cx_start = 60
    for i,cd in enumerate(codes):
        _c = "#10b981" if cd.startswith("0") else "#f59e0b" if cd.startswith("1") else "#ef4444"
        parts.append(box(cx_start+i*122,ey,112,36,cd,_c,"#fff",fs=11))
    parts.append('</svg>')
    return "\n".join(parts)

# ---------- md-converter flow ----------
def md_converter():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#f8fafc"/>')
    parts.append(f'<text x="{W//2}" y="38" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#0f172a">md-converter 转换流程</text>')
    # flow: input -> parse -> render -> outputs
    nodes = [
        (70, 160, 170, 100, "📄 Markdown\n输入文件", "#1e40af"),
        (290, 160, 170, 100, "🔍 解析器\nParser", "#7c3aed"),
        (510, 160, 170, 100, "⚙️ 渲染引擎\nRenderer", "#0891b2"),
        (730, 100, 150, 75, "📕 PDF\n文档", "#dc2626"),
        (730, 205, 150, 75, "📘 DOC\n文档", "#2563eb"),
    ]
    for x,y,w,h,t,c in nodes:
        parts.append(box(x,y,w,h,t,c,"#fff",fs=14))
    # arrows
    parts.append(arrow(240,210,290,210))
    parts.append(arrow(460,210,510,210))
    parts.append(arrow(680,185,730,137))
    parts.append(arrow(680,235,730,242))
    # features
    fy = 330
    feats = [
        ("✨ 纯前端实现 — 无需后端服务器", 60),
        ("🌐 浏览器内转换 — 数据不上传云端", 300),
        ("🎨 样式保留 — 支持 Markdown 扩展语法", 540),
        ("⚡ 即时预览 — 所见即所得编辑体验", 60, 365),
        ("📋 一键复制 — 转换结果快速导出", 300, 365),
        ("🤖 开源免费 — MIT License", 540, 365),
    ]
    for txt,fx,*extra in feats:
        yy = extra[0] if extra else fy
        parts.append(label(fx,yy,txt))
    parts.append('</svg>')
    return "\n".join(parts)

# ---------- TOMATOMATOO ----------
def tomatomaa():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#fef6f6"/>')
    parts.append(f'<text x="{W//2}" y="36" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#991b1b">TOMATOMATOO · 架构总览</text>')
    px = [30, 335, 640]; pw = 250; py = 64; ph = 322
    panels = [
        ("微信小程序前端", "#ef4444", [
            "pages/ · 9 个页面",
            "components/ · 自定义组件",
            "TDesign 组件库",
            "utils/ · 请求·状态·日期",
            "Skyline 番茄园生长动画",
        ]),
        ("云函数层 (CloudBase)", "#f97316", [
            "initUser · bond · plan",
            "reflection · calendar",
            "leave · report",
            "scheduledReminder",
            "统一授权校验 · 内容安全",
        ]),
        ("微信云开发底座", "#b91c1c", [
            "云数据库 · 文档集合",
            "users / bonds / plans",
            "tomatoes / reflections",
            "云存储 · 图片素材",
            "订阅消息 · 内容安全",
        ]),
    ]
    for x,(title,c,items) in zip(px, panels):
        parts.append(f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{c}" filter="url(#sh)" opacity="0.96"/>')
        parts.append(f'<text x="{x+pw//2}" y="{py+30}" text-anchor="middle" class="t" font-size="15" font-weight="800" fill="#fff">{esc(title)}</text>')
        ty = py+58
        for it in items:
            parts.append(f'<text x="{x+18}" y="{ty}" class="t" font-size="12" fill="#fff">{esc("• "+it)}</text>')
            ty += 24
    mid_y = py + ph//2
    parts.append(arrow(px[0]+pw, mid_y, px[1], mid_y, "#16a34a"))
    parts.append(label((px[0]+pw+px[1])//2-46, mid_y-10, "callFunction"))
    parts.append(arrow(px[1]+pw, mid_y, px[2], mid_y, "#16a34a"))
    parts.append(label((px[1]+pw+px[2])//2-34, mid_y-10, "读写·存储"))
    # timer trigger
    tb = (W//2-150, py+ph+24, 300, 54, "⏰ 定时触发器 · 每日 20:00 推送提醒", "#16a34a")
    parts.append(box(*tb, "#16a34a", "#14532d", fs=13))
    parts.append(arrow(W//2, tb[1], W//2, py+ph, "#16a34a", "arr-dk"))
    parts.append(label(W//2+10, (tb[1]+py+ph)//2, "触发"))
    parts.append(f'<text x="{W//2}" y="520" text-anchor="middle" class="t" font-size="13" font-weight="700" fill="#7f1d1d">约定计划 → 完成打卡 → 合种番茄 → 解锁番茄图鉴</text>')
    parts.append('</svg>')
    return "\n".join(parts)

# ---------- Token_Saver (SkillForge) ----------
def tokensaver():
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#f0fdfa"/>')
    parts.append(f'<text x="{W//2}" y="36" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#065f46">SkillForge · 系统架构</text>')
    px = [30, 335, 640]; pw = 250; py = 64; ph = 330
    panels = [
        ("浏览器工作台 · Frontend", "#0d9488", [
            "index.html 工作台界面",
            "style.css 样式（零依赖）",
            "app.js 交互与 HTTP 请求",
            "原生实现 · 零构建部署",
        ]),
        ("SkillForge 后端流水线", "#059669", [
            "① 解析 skill_parser",
            "② 校验 validator · 三轴",
            "③ 清洗 cleaner · 规则+LLM",
            "④ 计量 tokenizer + scorer",
            "⑤ 追踪 tracker · SQLite",
        ]),
        ("存储与外部依赖", "#047857", [
            "SQLite 数据看板 DATA_DIR",
            "技能目录 SKILLS_DIRS 扫描",
            "可选 LLM API 语义重写",
        ]),
    ]
    for x,(title,c,items) in zip(px, panels):
        parts.append(f'<rect x="{x}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{c}" filter="url(#sh)" opacity="0.96"/>')
        parts.append(f'<text x="{x+pw//2}" y="{py+30}" text-anchor="middle" class="t" font-size="15" font-weight="800" fill="#fff">{esc(title)}</text>')
        ty = py+58
        for it in items:
            parts.append(f'<text x="{x+18}" y="{ty}" class="t" font-size="12.5" fill="#fff">{esc("• "+it)}</text>')
            ty += 24
    mid_y = py + ph//2
    parts.append(arrow(px[0]+pw, mid_y, px[1], mid_y, "#0d9488"))
    parts.append(label((px[0]+pw+px[1])//2-44, mid_y-10, "HTTP / REST"))
    parts.append(arrow(px[1]+pw, mid_y, px[2], mid_y, "#0d9488"))
    parts.append(label((px[1]+pw+px[2])//2-52, mid_y-10, "读写·扫描·调用"))
    fb = (W//2-300, py+ph+24, 600, 54, "量化节省 ≈ Σ(各技能 description 清洗后减少的 token) × 会话轮次", "#0d9488")
    parts.append(box(*fb, "#0d9488", "#065f46", fs=13))
    parts.append(f'<text x="{W//2}" y="540" text-anchor="middle" class="t" font-size="12.5" font-weight="700" fill="#065f46">示例：20 个技能各压缩 30 token → 每轮省 600 · 千轮会话省约 60 万 token</text>')
    parts.append('</svg>')
    return "\n".join(parts)

def skill_pipeline():
    """README-beautifier 自身的工作流：三个数据驱动生成器 → 推送 GitHub。"""
    parts = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}">', defs()]
    parts.append(f'<rect width="{W}" height="{H}" rx="16" fill="#faf5ff"/>')
    parts.append(f'<text x="{W//2}" y="38" text-anchor="middle" class="t" font-size="22" font-weight="800" fill="#4c1d95">README Beautifier · 工作流</text>')

    # three generator stages (top row)
    stages = [
        ("gen_banners.py", "THEMES 字典", "1280×380\nSMIL 动画横幅", "#7c3aed"),
        ("gen_diagrams.py", "DIAGRAMS 字典", "架构 / 流程图\n静态 SVG", "#0891b2"),
        ("gen_readmes.py", "BUILDERS 字典", "徽章 + 特性表\n重组 README", "#db2777"),
    ]
    bw, bh = 230, 120
    gap = 40
    total = len(stages)*bw + (len(stages)-1)*gap
    start_x = (W - total)//2
    y = 90
    for i,(fn,dictn,desc,c) in enumerate(stages):
        x = start_x + i*(bw+gap)
        parts.append(box(x, y, bw, bh, fn, c, "#fff", fs=15))
        parts.append(label(x+12, y+44, dictn))
        for k,line in enumerate(desc.split("\n")):
            parts.append(f'<text x="{x+bw/2}" y="{y+66+k*18}" text-anchor="middle" class="t" font-size="12" fill="#475569">{esc(line)}</text>')
        if i < len(stages)-1:
            ax = x+bw+6
            parts.append(arrow(ax, y+bh/2, ax+gap-6, y+bh/2, "#7c3aed", "arr-dk"))

    # middle: data-driven note
    parts.append(box(W//2-180, 244, 360, 40, "数据驱动：增改字典即可支持新仓库", "#ede9fe", "#7c3aed", fs=13))
    parts.append(arrow(W//2, y+bh+4, W//2, 240, "#64748b"))

    # bottom: push + output
    parts.append(box(120, 330, 300, 70, "git clone → commit → push", "#0f766e", "#fff", fs=14))
    parts.append(box(W-420, 330, 300, 70, "GitHub README\n动画横幅在线播放", "#0f172a", "#fff", fs=14))
    parts.append(arrow(420, 365, W-420, 365, "#0f766e", "arr-dk"))
    parts.append(label((420+W-420)//2-30, 358, "推送"))

    # footer: SMIL note
    parts.append(f'<text x="{W//2}" y="450" text-anchor="middle" class="t" font-size="13" font-weight="700" fill="#4c1d95">GitHub 清洗内联 &lt;style&gt;/&lt;script&gt;，但保留 &lt;img src=\"banner.svg\"&gt; 并渲染 SMIL 动画</text>')
    parts.append(f'<text x="{W//2}" y="476" text-anchor="middle" class="t" font-size="12" fill="#64748b">因此横幅必须是独立 .svg 文件，零前端 JS 即可在 README 中动起来</text>')

    # stat strip
    fb = (W//2-260, 500, 520, 40, "已美化 9 个仓库 · 8 种 motif · 7 套架构图模板 · 全仓库视觉一致", "#7c3aed")
    parts.append(box(*fb, "#7c3aed", "#fff", fs=13))
    parts.append('</svg>')
    return "\n".join(parts)

DIAGRAMS = {
    "ChainPass": chainpass,
    "KeLing2.0": lambda: keling("2.0"),
    "KeLing3.0": lambda: keling("3.0"),
    "train_guard": train_guard,
    "md-converter": md_converter,
    "TOMATOMATOO": tomatomaa,
    "Token_Saver": tokensaver,
    "README-beautifier": skill_pipeline,
}

if __name__ == "__main__":
    name = sys.argv[1]
    fn = DIAGRAMS.get(name)
    if not fn:
        print(f"Unknown: {name}. Available: {list(DIAGRAMS.keys())}", file=sys.stderr)
        sys.exit(1)
    svg = fn()
    minidom.parseString(svg)
    sys.stdout.write(svg)
