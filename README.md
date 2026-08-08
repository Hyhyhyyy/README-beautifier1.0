<p align="center">
  <img src="banner.svg" alt="README Beautifier · GitHub README 一键美化" width="100%">
</p>

<div align="center">

![Skill](https://img.shields.io/badge/github-readme-beautify-a855f7)
![Animation](https://img.shields.io/badge/Banner-SMIL-0ea5e9)
![Python](https://img.shields.io/badge/Python-3.12-3776AB)
![License](https://img.shields.io/badge/License-MIT-blue)

**✨ 把任意 GitHub 仓库的 README 变成带动画横幅、架构图、徽章与特性表的精美 Landing Page**

数据驱动 · 保留原文 · 自动推送 · 视觉一致

</div>


---


## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| 🎬 **SMIL 动画横幅** | 每个仓库生成 1280×380 的独立 SVG hero banner，GitHub 原生播放动画，零前端 JS |
| 🏗️ **架构 / 流程图** | 为技术仓库自动产出三层架构或工作流 SVG，注入到目录结构之前 |
| 🏷️ **徽章 + 特性表** | 自动拼接 shields.io 状态徽章与核心特性对照表，视觉一致 |
| 🧬 **数据驱动** | THEMES / DIAGRAMS / BUILDERS 三个字典驱动，新增仓库只改字典不改逻辑 |
| 🚀 **一键推送** | 克隆 → 提交 → 推送，并校验远程 SVG 仍保留 SMIL 动画 |


---


> 一键把任意 GitHub 仓库的 README 变成带动画横幅、架构图、徽章与特性表的精美 Landing Page，并自动推送。

## 它是怎么工作的

GitHub 会在渲染 README 时清洗内联 `<style>` / `<script>`，但**保留 `<img src="banner.svg">` 并渲染其中的 SMIL 动画**。所以横幅必须是一个独立的 `.svg` 文件——这正是本项目的关键洞察：用纯 SVG + SMIL 实现「零前端 JS 的 README 动效」。

整个流程由三个数据驱动的生成器组成：

| 生成器 | 数据字典 | 产出 |
|--------|----------|------|
| `gen_banners.py` | `THEMES` | 1280×380 SMIL 动画 hero 横幅 |
| `gen_diagrams.py` | `DIAGRAMS` | 架构 / 工作流静态 SVG |
| `gen_readmes.py` | `BUILDERS` | 重组后的增强 README（横幅 + 徽章 + 特性表 + 原文） |

## 快速开始

```bash
# 1) 在三个字典里为你的仓库添加一项（THEMES / DIAGRAMS / BUILDERS）
# 2) 把原始 README 放到 <BASE>/<RepoName>.md
# 3) 生成三项资产
python scripts/gen_banners.py YourRepo > banner.svg
python scripts/gen_diagrams.py YourRepo > diagrams/YourRepo.svg
python scripts/gen_readmes.py YourRepo > README.md
# 4) 克隆目标仓库，提交并推送
```

## 🔧 工作流

<p align="center">
  <img src="diagrams/README-beautifier.svg" alt="README Beautifier 工作流" width="92%">
</p>

## 📁 目录

```
github-readme-beautify/
├── SKILL.md                     # 技能定义（供 WorkBuddy / 同类 Agent 加载）
├── scripts/
│   ├── gen_banners.py          # 动画横幅生成器（数据驱动）
│   ├── gen_diagrams.py         # 架构 / 流程图生成器（数据驱动）
│   ├── gen_readmes.py          # 增强 README 生成器（数据驱动）
│   └── render_qa.js            # 静态帧 QA（resvg，仅供本地预览）
├── references/
│   ├── environment-gotchas.md  # Windows / Git Bash / GitHub 坑位清单
│   ├── themes-and-adaptation.md# 字典字段 schema 与适配指南
│   └── verification.md         # 校验与推送流程
└── assets/
    └── sample-banner.svg       # 示例横幅
```

## 环境变量

| 变量 | 作用 | 默认 |
|------|------|------|
| `OUT` | 横幅输出目录 | 脚本同级 `banners/` |
| `README_BASE` | 原始 README 所在目录 | 当前工作目录 |

## 适配新用户

1. 把 `THEMES` / `BUILDERS` / `DIAGRAMS` 换成你自己的仓库。
2. 用 `README_BASE` 指向原始 README 文件夹（或 cwd）。
3. 输出目录默认在脚本同级；可用 `OUT` / `README_BASE` 覆盖。
4. 生成器逻辑（orbs、streaks、motifs、徽章 / 表格辅助函数）可原样复用。

---

本项目本身是「自举」的：上面的横幅与架构图，正是由这套脚本为自己生成的。


---

<div align="center">

**Made with ❤️ by Hyhyhyyy**

</div>
