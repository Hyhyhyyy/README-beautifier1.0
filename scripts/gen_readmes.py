#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate enhanced README.md for each repo: banner + badges + features + preserved body.

Usage:
    python gen_readmes.py <RepoName>   -> prints the enhanced README to stdout

The builder reads the original README from <BASE>/<RepoName>.md (BASE defaults to
the current working directory; override with the README_BASE env var). Add/modify
per-repo builders in the BUILDERS dict (see references/themes-and-adaptation.md).
"""
import sys, os

BASE = os.environ.get("README_BASE", os.getcwd())

def read_orig(name):
    p = os.path.join(BASE, f"{name}.md")
    if os.path.exists(p):
        return open(p,"r",encoding="utf-8").read()
    return ""

def esc(s): return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

# ---------- shared helpers ----------
def banner_img(alt="project banner"):
    return f'''<p align="center">
  <img src="banner.svg" alt="{esc(alt)}" width="100%">
</p>'''

def badge_row(badges):
    """badges = list of (label, color, value, url_or_None)"""
    parts = []
    for label, color, value, url in badges:
        u = f"-{url}" if url else ""
        parts.append(f'![{label}](https://img.shields.io/badge/{value}-{color}{u})')
    return "\n".join(parts)

def feature_table(rows):
    """rows = list of (icon_title, description)"""
    lines = ["| 特性 | 说明 |", "|------|------|"]
    for t,d in rows:
        lines.append(f"| {t} | {d} |")
    return "\n".join(lines)

def divider(): return "\n---\n"

# ================================================================
# PER-REPO BUILDERS
# ================================================================

def build_chainpass(orig):
    bgs = [
        ("Version","blue","version-2.0.0",None),
        ("Java","orange","Java-17",None),
        ("Spring Boot","green","Spring%20Boot-3.4.3",None),
        ("Vue","brightgreen","Vue-3.5",None),
        ("License","blue","license-MIT",None),
    ]
    feats = [
        ("🆔 **DID身份系统**", "W3C标准去中心化身份，用户完全掌控数字身份"),
        ("📜 **可验证凭证VC**", "密码学证明的身份属性，一次认证多平台复用"),
        ("💳 **跨境支付**", "多币种钱包、实时汇率、合规风控"),
        ("✅ **KYC自动合规**", "身份认证通过后自动签发VC，无缝衔接"),
        ("🔐 **多元登录**", "账密、OAuth、零知识证明多种认证方式"),
    ]
    tech = [
        ("Backend","Java 17 / Spring Boot 3.4"),
        ("Frontend","Vue 3.5 / Vite / Pinia"),
        ("Database","MySQL 8.0 / Redis 7.0"),
        ("Deploy","Docker Compose / Swagger UI"),
    ]
    # strip original first heading line(s) to avoid duplicate title
    body = orig
    for prefix in ["# ChainPass","# ChainPass -"]:
        if body.startswith(prefix):
            idx = body.find("\n")
            body = body[idx+1:].lstrip("\n")
            break
    # replace ASCII architecture block with diagram reference
    import re
    body = re.sub(r'```[\s\S]*?系统架构[\s\S]*?```', f'<p align="center"><img src="diagrams/ChainPass.svg" alt="ChainPass System Architecture" width="90%"></p>', body, count=1)

    return f"""{banner_img("ChainPass Blockchain Identity & Payment")}

<div align="center">

{badge_row(bgs)}

**W3C DID 标准 · 可验证凭证 · 跨境支付 · 合规认证**

[🌐 在线演示](#) · [📖 API文档](docs/API_DOCUMENTATION.md) · [🚀 使用指南](docs/PROJECT_GUIDE.md) · [🏆 大创材料](docs/INNOVATION_PROJECT.md)

</div>

{divider()}

## ✨ 核心特性

{feature_table(feats)}

## 🛠 技术栈

| 层面 | 技术 |
|------|------|
{''.join(f'| {k} | {v} |\n' for k,v in tech)}{divider()}

## 📊 系统架构

<p align="center">
  <img src="diagrams/ChainPass.svg" alt="ChainPass System Architecture" width="90%">
</p>

{body}

---

<div align="center">

**Made with ❤️ by ChainPass Team**

</div>
"""

def build_claudecode(orig):
    bgs = [
        ("Python","3776AB","Python-blue",None),
        ("License","blue","License-MIT",None),
        ("Educational","green","Purpose-Educational",None),
    ]
    feats = [
        ("🐍 **Python First**", "完整的 Python 移植工作区，替代原始 TypeScript 快照"),
        ("🔧 **CLI 入口点**", "`python3 -m src.main` 支持 summary / manifest / subsystems"),
        ("✅ **验证套件**", "`unittest discover` 持续验证当前工作区状态"),
        ("🤖 **AI 辅助开发**", "基于 oh-my-codex (OmX) 的团队协作与代码审查"),
    ]
    # strip first heading
    body = orig
    for prefix in ["# Claude Code","# Claude Code Python Porting Workspace"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    return f"""{banner_img("claude-code Python Port")}

<div align="center">

{badge_row(bgs)}

**An independent Python port of Claude Code — Educational Purpose Only**

[📄 Related Essay](https://writings.hongminhee.org/2026/03/legal-vs-legitimate/) · [🛠️ oh-my-codex](https://github.com/Yeachan-Heo/oh-my-codex)

</div>

{divider()}

## ✨ 核心能力

{feature_table(feats)}

{divider()}

## 📦 Repository Layout & Workspace

{body}

---

<div align="center">

> ⚠️ **Ownership Disclaimer**
>
> This repository does **not** claim ownership of the original Claude Code source material.
> This repository is **not affiliated with, endorsed by, or maintained by Anthropic**.

</div>
"""

def build_dlut(orig):
    bgs = [
        ("JavaScript","yellow","JavaScript",None),
        ("CloudBase","00A4FF","CloudBase-blue",None),
        ("License","blue","License-MIT",None),
    ]
    feats = [
        ("👥 **成员审核系统**", "匿名登录提交资料，管理员审核后公开显示"),
        ("📸 **照片图库**", "队友日常照片上传与发布流程"),
        ("🏆 **首次比赛登记**", "公开成员登记正式比赛经历"),
        ("📱 **二维码管理**", "官网、后台、照片页主题海报二维码生成"),
        ("☁️ **CloudBase 托管**", "腾讯云 CloudBase 公开网站托管与数据持久化"),
    ]
    body = orig
    for prefix in ["# BLACK ANTS","# BLACK ANTS 飞盘队网站"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    return f"""{banner_img("BLACK ANTS Ultimate Frisbee Team")}

<div align="center">

{badge_row(bgs)}

**大连理工大学开发区校区黑蚁极限飞盘队 · 官方网站**

[🌐 官网](https://dutultimate.club/) · [📋 项目状态](PROJECT_STATUS.md) · [📖 部署文档](docs/CLOUDBASE_DEPLOYMENT.md)

</div>

{divider()}

## ✨ 功能亮点

{feature_table(feats)}

{divider()}

{body}

---

<div align="center">

**Made with ❤️ by BLACK ANTS**

</div>
"""

def build_keling(ver, orig):
    bgs = [
        ("Kotlin","7F52FF","Kotlin-7F52FF",None),
        ("React","61DAFB","React-61DAFB",None),
        ("Node.js","339933","Node.js-339933",None),
        ("Android","3DDC84","Android-3DDC84",None),
        ("License","blue","License-MIT",None),
    ]
    feats = [
        ("📱 **Android 移动端**", "Kotlin + Jetpack Compose + Material Design 3 + MVVM"),
        ("🌐 **Web 网页端**", "React 18 + TypeScript + Vite + Zustand + Framer Motion"),
        ("⚙️ **后端服务**", "Node.js + Express + Prisma ORM + SQLite + JWT"),
        ("🔄 **数据同步**", "多端共享同一后端 API，用户数据实时同步"),
        ("✅ **核心功能**", "用户认证、课程管理、任务系统、笔记同步、每日签到"),
    ]
    body = orig
    for prefix in ["# 课灵 KeLing"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    diag_ref = f'<p align="center"><img src="diagrams/KeLing{ver}.svg" alt="KeLing {ver} Multi-end Architecture" width="85%"></p>'
    return f"""{banner_img(f"课灵 KeLing {ver}")}

<div align="center">

{badge_row(bgs)}

**🌱 多端知识管理应用 · 培育你的知识星球**

</div>

{divider()}

## ✨ 核心功能

{feature_table(feats)}

## 🏗 多端架构

{diag_ref}

{divider()}

{body}

---

<div align="center">

**Made with ❤️ by Hyhyhyyy**

</div>
"""

def build_mdconverter():
    bgs = [
        ("HTML5","E34F26","HTML5-E34F26",None),
        ("CSS3","1572B6","CSS3-1572B6",None),
        ("JavaScript","F7DF1E","JavaScript-F7DF1E",None),
        ("Markdown","white","Markdown-black",None),
        ("License","blue","License-MIT",None),
    ]
    feats = [
        ("✨ **纯前端实现**", "无需后端服务器，浏览器内完成全部转换"),
        ("🌐 **隐私优先**", "数据不上传云端，本地完成解析与渲染"),
        ("🎨 **样式保留**", "支持 Markdown 扩展语法，保留格式与排版"),
        ("⚡ **即时预览**", "所见即所得的编辑体验，实时查看效果"),
        ("📋 **一键导出**", "支持 PDF 和 DOC 格式快速导出"),
        ("🤖 **开源免费**", "MIT License，自由使用与修改"),
    ]
    diag_ref = '<p align="center"><img src="diagrams/md-converter.svg" alt="md-converter Conversion Flow" width="80%"></p>'
    return f"""{banner_img("md-converter Markdown Converter")}

<div align="center">

{badge_row(bgs)}

**Markdown → PDF / DOC · 一键优雅转换**

</div>

{divider()}

## ✨ 功能特性

{feature_table(feats)}

## 🔧 转换流程

{diag_ref}

{divider()}

## 🚀 使用方法

### 本地运行

```bash
# 克隆项目
git clone https://github.com/Hyhyhyyy/md-converter.git
cd md-converter

# 安装依赖（可选）
npm install

# 启动本地预览
npm run dev
# 或直接在浏览器中打开 index.html
```

### 在线使用

直接在浏览器中打开 `index.html`，粘贴或输入 Markdown 内容，选择输出格式（PDF / DOC），点击转换即可。

{divider()}

## 📁 项目结构

```
md-converter/
├── index.html      # 主页面
├── script.js       # 核心转换逻辑
├── styles.css      # 样式表
└── README.md       # 项目说明
```

{divider()}

## 📄 License

MIT License

---

<div align="center">

**Made with ❤️ by Hyhyhyyy**

</div>
"""

def build_trainguard(orig):
    bgs = [
        ("CI","success","CI-success","https://github.com/Hyhyhyyy/train_guard/actions/workflows/ci.yml"),
        ("Python","blue","python-3.10--3.14-blue","https://www.python.org/"),
        ("License","blue","License-Apache--2.0-blue","LICENSE"),
    ]
    feats = [
        ("🔍 **训练前检查**", "环境、GPU、依赖、模型路径、数据集、媒体文件全面检查"),
        ("👁️ **训练中观测**", "生命周期、日志、Loss、GPU、磁盘、检查点、进程监控"),
        ("🛡️ **可靠性保障**", "结构化事件、去重告警、持久状态、有界恢复"),
        ("✅ **训练后校验**", "输出验收、运行对比、评估、SHA256 清单"),
        ("🖥️ **多端接口**", "CLI、Python API、HF Callback、Web Dashboard、SSH TUI"),
        ("📦 **零依赖核心**", "无必需依赖的单文件发布，checksum 校验"),
    ]
    body = orig
    for prefix in ["# Train Guard"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    diag_ref = '<p align="center"><img src="diagrams/train_guard.svg" alt="Train Guard Workflow" width="95%"></p>'
    return f"""{banner_img("Train Guard LLM/VLM Training Toolkit")}

<div align="center">

{badge_row(bgs)}

**LLM/VLM 训练守护 · 可靠观测与受控恢复**

[简体中文](README_zh-CN.md) · [CLI Reference](docs/CLI.md) · [Configuration](docs/CONFIGURATION.md) · [Reliability](docs/RELIABILITY.md) · [Architecture](ARCHITECTURE.md)

</div>

{divider()}

## ✨ Capabilities at a Glance

{feature_table(feats)}

## 🔄 工作流概览

{diag_ref}

{divider()}

{body}

---

<div align="center">

Licensed under the Apache License 2.0 · see [LICENSE](LICENSE)

</div>
"""

def build_tomatomaa(orig):
    bgs = [
        ("WeChat MP","07C160","WeChat%20MP-Native",None),
        ("CloudBase","0052D9","CloudBase-Serverless",None),
        ("JavaScript","F7DF1E","JavaScript-ES6",None),
        ("License","blue","License-MIT",None),
    ]
    body = orig
    # strip first heading (title) to avoid duplicate
    for prefix in ["# 一起养番茄","# 一起养番茄 · 双人习惯养成小程序"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    diag_section = """## 🏗 架构总览

<p align="center">
  <img src="diagrams/TOMATOMATOO.svg" alt="TOMATOMATOO 架构总览" width="92%">
</p>

"""
    # inject architecture diagram before the directory tree (after 技术栈) if present
    if "## 📁 目录结构" in body:
        body = body.replace("## 📁 目录结构", diag_section + "## 📁 目录结构", 1)
    else:
        body = diag_section + body
    return f"""{banner_img("TOMATOMATOO 双人习惯养成小程序")}

<div align="center">

{badge_row(bgs)}

**🍅 两个人绑定到一起，把坚持可视化成一片共享番茄园**

微信小程序原生 + 云开发 CloudBase · 零服务器 · 零域名 · 零支付

</div>

{divider()}

{body}

---

<div align="center">

**Made with ❤️ by Hyhyhyyy**

</div>
"""

def build_tokensaver(orig):
    bgs = [
        ("Python","3776AB","Python-3.12",None),
        ("FastAPI","009688","FastAPI-0.115",None),
        ("SQLite","1B6EC2","SQLite-DB",None),
        ("Docker","2496ED","Docker-Deploy",None),
    ]
    feats = [
        ("🔍 **统一格式校验**", "按《标准规范 v1.0》三轴（格式/语义/冗余）自动体检，给出健康度评分与修复建议"),
        ("🧹 **语义清洗**", "规则引擎归一化描述为标准模板，移除填充词与重复字段；可选 LLM 语义重写进一步压缩"),
        ("🗜️ **冗余压缩**", "以 Token 预算（目标 ≤40，硬上限 90）压减 description，前后对比量化节省"),
        ("📊 **调用效果追踪**", "SQLite 记录每次优化/应用事件，看板展示累计节省、每轮常驻节省与趋势排行"),
        ("🖥️ **零构建工作台**", "原生 HTML/CSS/JS 前端，Docker 或一键脚本即可本地部署"),
    ]
    body = orig
    for prefix in ["# SkillForge · 技能精炼台","# SkillForge"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    diag_section = """## 🏗 系统架构

<p align="center">
  <img src="diagrams/Token_Saver.svg" alt="SkillForge 系统架构" width="92%">
</p>

"""
    if "## 目录结构" in body:
        body = body.replace("## 目录结构", diag_section + "## 目录结构", 1)
    else:
        body = diag_section + body
    return f"""{banner_img("SkillForge 技能精炼台 · Token Saver")}

<div align="center">

{badge_row(bgs)}

**🍅 让每一轮对话少花无效 Token · AI 工作台 Skill 资产优化**

</div>

{divider()}

## ✨ 核心特性

{feature_table(feats)}

{divider()}

{body}

---

<div align="center">

**Made with ❤️ by Hyhyhyyy**

</div>
"""

def build_readmebeautifier(orig):
    bgs = [
        ("Skill","a855f7","github-readme-beautify",None),
        ("Animation","0ea5e9","Banner-SMIL",None),
        ("Python","3776AB","Python-3.12",None),
        ("License","blue","License-MIT",None),
    ]
    feats = [
        ("🎬 **SMIL 动画横幅**", "每个仓库生成 1280×380 的独立 SVG hero banner，GitHub 原生播放动画，零前端 JS"),
        ("🏗️ **架构 / 流程图**", "为技术仓库自动产出三层架构或工作流 SVG，注入到目录结构之前"),
        ("🏷️ **徽章 + 特性表**", "自动拼接 shields.io 状态徽章与核心特性对照表，视觉一致"),
        ("🧬 **数据驱动**", "THEMES / DIAGRAMS / BUILDERS 三个字典驱动，新增仓库只改字典不改逻辑"),
        ("🚀 **一键推送**", "克隆 → 提交 → 推送，并校验远程 SVG 仍保留 SMIL 动画"),
    ]
    body = orig
    for prefix in ["# README Beautifier","# README-beautifier"]:
        if body.startswith(prefix):
            idx = body.find("\n"); body = body[idx+1:].lstrip("\n"); break
    diag_section = """## 🔧 工作流

<p align="center">
  <img src="diagrams/README-beautifier.svg" alt="README Beautifier 工作流" width="92%">
</p>

"""
    if "## 📁 目录" in body:
        body = body.replace("## 📁 目录", diag_section + "## 📁 目录", 1)
    else:
        body = diag_section + body
    return f"""{banner_img("README Beautifier · GitHub README 一键美化")}

<div align="center">

{badge_row(bgs)}

**✨ 把任意 GitHub 仓库的 README 变成带动画横幅、架构图、徽章与特性表的精美 Landing Page**

数据驱动 · 保留原文 · 自动推送 · 视觉一致

</div>

{divider()}

## ✨ 核心特性

{feature_table(feats)}

{divider()}

{body}

---

<div align="center">

**Made with ❤️ by Hyhyhyyy**

</div>
"""

BUILDERS = {
    "ChainPass": lambda o: build_chainpass(o),
    "claude-code": lambda o: build_claudecode(o),
    "dlut-ultimate-website": lambda o: build_dlut(o),
    "KeLing2.0": lambda o: build_keling("2.0", o),
    "KeLing3.0": lambda o: build_keling("3.0", o),
    "md-converter": lambda o: build_mdconverter(),
    "train_guard": lambda o: build_trainguard(o),
    "TOMATOMATOO": lambda o: build_tomatomaa(o),
    "Token_Saver": lambda o: build_tokensaver(o),
    "README-beautifier": lambda o: build_readmebeautifier(o),
}

if __name__ == "__main__":
    name = sys.argv[1]
    fn = BUILDERS.get(name)
    if not fn:
        print(f"Unknown: {name}", file=sys.stderr); sys.exit(1)
    orig = read_orig(name)
    readme = fn(orig)
    sys.stdout.write(readme)
