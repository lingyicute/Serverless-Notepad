<div align="center">

# 📝 小小记事本 Pro

**一个零后端、单文件、完全运行在浏览器里的在线记事本。**

[English](./README.md) · [简体中文]

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)
[![Deploy to GitHub Pages](https://github.com/lingyicute/Serverless-Notepad/actions/workflows/static.yml/badge.svg)](https://github.com/lingyicute/Serverless-Notepad/actions/workflows/static.yml)
![Single File](https://img.shields.io/badge/size-1%20HTML%20file-success)
![No Backend](https://img.shields.io/badge/backend-none-success)

**[🌐介绍站点](https://introduce.np.92li.uk)  ·  [🚀 在线体验](https://np.92li.uk)**

</div>

---

## ✨ 这是什么？

小小记事本 Pro 是一个极简的记事本网页，整个项目只有 **一个 `index.html` 文件**。没有数据库、没有接口、不需要注册账号、不需要安装任何东西。你的笔记保存在自己的浏览器里，分享时则把笔记内容 **直接编码进链接本身**。

把这个文件丢到任意静态托管平台（GitHub Pages、Vercel、Netlify、对象存储，甚至一个 U 盘），它就能直接运行。

## 🎯 功能特性

| | 功能 | 说明 |
|---|---|---|
| 💾 | **自动保存** | 标题和正文在输入后防抖 500 ms 自动写入 `localStorage`。关掉标签页再回来，内容依然在。 |
| 🌗 | **深色 / 浅色主题** | 首次访问跟随系统偏好，一键切换后会记住你的选择。 |
| 🔗 | **在线分享链接** | 生成标准网址（`?note=<base64>`），任何人点开即可在编辑器中查看和编辑该笔记。 |
| 📦 | **离线快照** | 生成一个自包含的 `data:text/html` 链接——只读、带主题切换，无需任何服务器即可打开。 |
| 📋 | **一键复制** | 使用 Clipboard API，非安全上下文下自动回退到 `execCommand`。 |
| 📱 | **响应式布局** | 手机、平板、桌面端均可良好使用。 |
| 🪶 | **极致轻量** | 约 20 KB 的 HTML + CSS + 原生 JavaScript，无构建步骤、无框架。 |

## 🚀 快速开始

### 在线使用

打开 **<https://np.92li.uk>**，直接开始记录。

### 本地运行

```bash
git clone https://github.com/lingyicute/Serverless-Notepad.git
cd Serverless-Notepad
# 直接用浏览器打开 index.html 即可，或者启动一个静态服务器：
python3 -m http.server 8080
```
> [!tip]
> Tailwind CSS 与 Lucide 图标通过公共 CDN 加载，因此样式和图标需要联网才能显示。

### 部署你自己的版本

1. **Fork** 本仓库。
2. 进入 **Settings → Pages**，将 Source 设置为 **GitHub Actions**。
3. 推送到 `main` 分支——仓库内置的工作流（`.github/workflows/static.yml`）会自动发布站点。

分享链接是根据 `window.location.origin + pathname` 动态生成的，因此会自动指向 **你自己的部署地址**，无需任何配置。

## 🧭 使用说明

1. **编辑** —— 点击顶部标题区域输入标题，点击虚线框区域输入正文，所有内容自动保存。
2. **切换主题** —— 点击右上角的 ☾ / ☀ 按钮。
3. **分享** —— 点击 **分享** 按钮，二选一：

   | 方式 | 优点 | 缺点 |
   |---|---|---|
   | **方式一：离线快照**（Data-URL） | 完全独立，像一个文件；可离线打开，内含「在编辑器中打开」按钮。 | 链接非常长，必须粘贴到 **浏览器地址栏** 才能打开（大多数聊天软件不会将其识别为可点击链接）。 |
   | **方式二：在线链接**（Redirect-URL） | 标准网页链接，可直接发给他人点击，打开后即进入编辑器。 | 依赖本站可访问，需要网络连接。 |

4. **打开别人分享的笔记** —— 访问带 `?note=` 参数的链接时，笔记会被解码并载入编辑器，同时写入 `localStorage`，然后地址栏会自动清理掉参数。

## ⚙️ 工作原理

```
┌────────────────────┐    input（防抖）      ┌──────────────────┐
│  contenteditable   │ ────────────────────▶ │   localStorage   │
│    标题 + 正文      │ ◀──────────────────── │   （自动恢复）    │
└─────────┬──────────┘        load           └──────────────────┘
          │  分享
          ▼
  标题 + "\n[---NOTE-SEPARATOR---]\n" + 正文
          │
          ├─▶ base64  ──▶  https://你的站点/?note=<base64>          （在线链接）
          │
          └─▶ 内联 HTML 快照 ──▶ data:text/html;charset=utf-8,…   （离线快照）
```

* **编码方式**：标题与正文用分隔符拼接，先 UTF-8 编码再 base64（`btoa(unescape(encodeURIComponent(...)))`）。
* **快照生成**：即时生成一个极小的只读 HTML 页面，笔记内容通过 `JSON.stringify` 注入以防止脚本注入，自带主题切换按钮和返回编辑器的链接。
* **长度保护**：当生成的链接超过约 180 万字符时会拒绝生成并弹出提示。

## 🛠️ 技术栈

* 原生 **HTML / CSS / JavaScript**（ES2015+），IIFE 作用域封装，不污染全局
* [Tailwind CSS](https://tailwindcss.com/)（CDN），配合 CSS 变量实现主题
* [Lucide](https://lucide.dev/) 图标（CDN）
* GitHub Actions → GitHub Pages 自动部署

## ⚠️ 限制与隐私说明

* 笔记 **仅保存在你浏览器的 `localStorage` 中**，清除站点数据会导致笔记丢失；任何内容都不会上传到服务器。
* 分享链接中包含 **完整的笔记内容（仅 base64 编码，并非加密）**，拿到链接的任何人都能读取。请勿用此方式分享敏感信息。
* 笔记过长时可能超出浏览器 URL 长度限制，尤其是 Data-URL 离线快照。
* 同一时间只保留一篇笔记；打开他人的分享链接会覆盖当前笔记。

## 🤗 参与贡献

欢迎提交 Issue 和 Pull Request！整个项目就是一个文件，参与门槛很低——直接修改 `index.html` 即可。

## 📄 开源协议

本项目基于 **GNU Affero General Public License v3.0** 开源，详见 [LICENSE](./LICENSE)。
