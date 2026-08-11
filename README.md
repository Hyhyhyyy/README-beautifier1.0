<p align="center">
  <img src="banner.svg" alt="README-beautifier1.0 hero banner">

</p>

<p align="center">
  <img src="https://img.shields.io/badge/license-MIT-green" alt="license">
  <img src="https://img.shields.io/badge/Banner-SMIL-0ea5e9" alt="banner">
  <img src="https://img.shields.io/badge/Python-3.12-3776AB" alt="python">
  <img src="https://img.shields.io/badge/platform-any--agent-8b5cf6" alt="platform">
</p>

# README-beautifier1.0
> ℹ️ 本仓库为 **1.0 历史版本**；当前维护线为 [`README-beautifier2.0`](https://github.com/Hyhyhyyy/README-beautifier2.0)。

**把任意 GitHub 仓库的 README 变成带动画横幅、架构图、徽章与特性表的精美 Landing Page——纯 SMIL 动画，零前端 JS。**

一款 **WorkBuddy 技能（skill）**，但方法**平台无关**：任何能产出矢量 / 插画资源并读写 GitHub 的 Agent、助手或工具都可以复用（详见「适用范围」）。

## 适用范围 / Scope & portability

本技能以 WorkBuddy skill 形式打包，但**核心技术是平台无关的**，适用于任何满足以下条件的 agent / 工具：

- 能产出矢量或插画资源（手绘 SVG，或将生成图转为 SVG）；
- 能读写 GitHub 仓库（`gh`、Git 协议或 REST API 均可）。

为什么能迁移到别处：

- **核心技巧是 GitHub 平台约束，不是 WorkBuddy 特性**：GitHub 会剥离 README 内联 `<style>`/`<script>`，但保留 `<img src="banner.svg">` 引用的独立 SVG 里的 SMIL 动画。所以横幅在**任何** agent 产出的 README 上都能动。
- **设计规则是方法论而非工具**：内容驱动选母题、零预设手绘、两条必备动效层、唯一性闸门、徽章安全——换平台照手写或移植生成器即可。
- **QA 校验器 `scripts/validate_banner.py` 是纯 Python 3**，任何 agent 本地都能跑，无需 WorkBuddy 运行时。

仅 WorkBuddy 特有的（且易于别处重实现）：`SKILL.md` frontmatter / 触发词、生成器脚本（便利助手）、`gh` 推送（任何 Git 客户端或 REST API 等效）。

> 一句话：在 WorkBuddy 里直接用本技能，或把「方法 + 校验器」搬到任何能绘图并推送到 GitHub 的 agent / 平台。唯一硬依赖是 GitHub 的 README 清洗行为——动画必须放在独立 `banner.svg`，绝不停留在内联。

## 🚫 零预设——核心铁律

本技能**没有任何母题函数、动画预设字典、THEMES 数据文件或共享配色预设**。每个横幅都是对该仓库**从空白画布手绘**的一次性作品。唯一共用工具是 QA 校验器（`scripts/validate_banner.py`），它只做正确性检查与防抄袭，从不提供可复用的形状。

## 产出

- `banner.svg`（1280×380）：手绘的动画 Hero 横幅，在目标仓库 README 顶部引用：`<img src="banner.svg">`
- 增强版 README（可选）：顶部横幅 + 安全的 shields.io 徽章 + 原文内容（逐字保留）

## 视觉风格（当前默认：科幻 / 核心概念）

- **深空暗底**：近黑、按仓库色相微调的多段渐变背景
- **霓虹辉光**：`feGaussianBlur` 合并滤镜营造发光
- **遍布横幅的粒子场**：约 60 颗粒子散布全幅，各自闪烁 + 轻微漂移（本技能的招牌科幻元素）
- **独特手绘概念物**：每个仓库一个霓虹线框签名物体（stroke-width 6–12），带生命动画（嵌套在 inner `<g>`，避免 Rule 3 变换擦除）
- **无圆形边框**、不堆叠元素、留白充足

### 两条必备动效层（Rule 7）

1. **全幅扫描**：水平行程 ≥ 600px 的动画（如斜向扫光光束、横跨的粒子流）
2. **标题区动画**：标题文字周围的动画（下划线 draw-on、辉光脉冲、轨道粒子等）

## 工作流

1. **读完整 README**（含 description + topics）——从「项目实际做什么」综合视觉概念，禁止按仓库名字面画。
2. **手绘空白 1280×380 画布**——零预设复用，每个横幅一套新鲜配色 + 独特签名物体 + 专属动效。
3. **推送前校验**：

   ```bash
   python scripts/validate_banner.py --gate banners/ banner.svg   # Rule 1-4 + 6 + 7
   python scripts/validate_banner.py --all  banners/               # Rule 1-4 + 6（唯一性）
   ```

   - **Rule 6（唯一性闸门）**：与 `banners/` 基线比对——换色克隆或挪用母题图形 → FAIL。
   - **Rule 3（变换擦除）**：勿把 `rotate`/`scale` 的 `<animateTransform>` 放在带基础 `translate()` 的同一 `<g>`；改用 inner `<g>`。
4. **可靠推送**：经 `gh api -X PUT repos/<owner>/<repo>/contents/banner.svg`（REST 写出口，带 base64 内容 + 现有 blob sha，PUT 后立刻 GET 复核 SHA-256）。⚠️ 注意：本环境下 `git push` 经镜像代理常为「幻影成功」（本地报成功、远端未变），故以 `gh api` PUT 为准。

## 仓库结构

```
SKILL.md                       # 技能定义（WorkBuddy 读取）
scripts/validate_banner.py     # 静态 QA 校验器（Rule 1-4, 5, 6, 7）
scripts/gen_scifi.py           # 科幻横幅生成器（每仓独特的手绘母题函数）
references/principles.md       # 手绘设计原则
assets/sample-banner.svg       # 单个示例横幅
banners/                       # 已交付的横幅示例（唯一性基线）
```

## 示例横幅（banners/）

TOMATOMATOO、MyBlog、README-beautifier、Token_Saver、train_guard、md-converter、KeLing1.0 / 2.0 / 3.0、dlut-ultimate-website、ChainPass、claude-code、MLP-2048、Qwen3-VL-Med。

## 仓库描述规范（About）

每个被美化的仓库都会用统一的 📌 中文风格设置 GitHub 描述：

```
📌<项目名/定位><1–2 emoji>。<技术栈 / 核心功能 / 适用场景 / 定位，分号列举，结尾。>
```

当仓库本身就是本技能（方法型工具）时，正文须声明**平台无关、可被任何能绘图的 agent 复用**（详见 SKILL.md Step 4.6）。

## 安装（WorkBuddy）

```bash
# 用户级（所有项目）
cp -r README-beautifier1.0 ~/.workbuddy/skills/

# 或项目级
cp -r README-beautifier1.0 <your-project>/.workbuddy/skills/
```

然后在 WorkBuddy 对话中调用该技能即可。若迁移到其他平台，按「适用范围」把方法 + 校验器搬过去即可。

---

**Made with ❤️ by Hyhyhyyy**
