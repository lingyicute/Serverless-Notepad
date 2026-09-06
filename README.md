<div align="center">

# 📝 Serverless Notepad

**A zero-backend, single-file notepad that lives entirely in your browser.**

[English] · [简体中文](./README.zh-CN.md)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](./LICENSE)
[![Deploy to GitHub Pages](https://github.com/lingyicute/Serverless-Notepad/actions/workflows/static.yml/badge.svg)](https://github.com/lingyicute/Serverless-Notepad/actions/workflows/static.yml)
![Single File](https://img.shields.io/badge/size-1%20HTML%20file-success)
![No Backend](https://img.shields.io/badge/backend-none-success)

**[🌐Introduce Page](https://introduce.np.92li.uk)  ·  [🚀 Live Page](https://np.92li.uk)**

</div>

---

## ✨ What is this?

Serverless Notepad (小小记事本 Pro) is a minimalist note-taking page packed into **one `index.html` file**. There is no database, no API, no account, and nothing to install. Your notes are stored in your own browser, and sharing works by encoding the note *into the link itself*.

Drop the file on any static host (GitHub Pages, Vercel, Netlify, an S3 bucket, or even a USB stick) and it just works.

## 🎯 Features

| | Feature | Details |
|---|---|---|
| 💾 | **Auto-save** | Title and body are debounced (500 ms) and persisted to `localStorage`. Close the tab, come back later, everything is still there. |
| 🌗 | **Dark / Light theme** | Follows your system preference on first visit; a one-click toggle remembers your choice. |
| 🔗 | **Online share link** | Generates a normal URL (`?note=<base64>`) that anyone can click to open your note in the editor. |
| 📦 | **Offline snapshot** | Generates a self-contained `data:text/html` URL – a read-only, themed copy of your note that opens without any server at all. |
| 📋 | **One-click copy** | Clipboard API with a `execCommand` fallback for non-secure contexts. |
| 📱 | **Responsive** | Works on phones, tablets and desktops. |
| 🪶 | **Tiny** | ~20 KB of HTML, CSS and vanilla JavaScript. No build step, no framework. |

## 🚀 Quick Start

### Use it online

Open **<https://np.92li.uk>** and start typing.

### Run it locally

```bash
git clone https://github.com/lingyicute/Serverless-Notepad.git
cd Serverless-Notepad
# Simply open index.html in a browser, or serve the folder:
python3 -m http.server 8080
```
> [!tip]
> Tailwind CSS and Lucide icons are loaded from public CDNs, so an internet connection is required for styling and icons.

### Deploy your own copy

1. **Fork** this repository.
2. Go to **Settings → Pages** and set the source to **GitHub Actions**.
3. Push to `main` – the included workflow (`.github/workflows/static.yml`) publishes the site automatically.

The share links are generated from `window.location.origin + pathname`, so they will point to *your* deployment with no configuration needed.

## 🧭 How to Use

1. **Edit** – Click the heading to set a title, click the dashed area to write your note. Everything is saved automatically.
2. **Toggle theme** – Use the ☾ / ☀ button in the top-right corner.
3. **Share** – Click **Share** and choose one of two options:

   | Method | Pros | Cons |
   |---|---|---|
   | **Offline snapshot** (Data-URL) | Completely standalone, like a file. Opens offline, includes an "Open in editor" button. | Very long link; must be pasted into the **browser address bar** (most chat apps won't make it clickable). |
   | **Online link** (Redirect-URL) | A standard, clickable web link. Opens the note directly in the editor. | Depends on this site being reachable. |

4. **Open a shared note** – When a `?note=` link is opened, the note is decoded, loaded into the editor, saved to `localStorage`, and the URL is cleaned up.

## ⚙️ How It Works

```
┌────────────────────┐   input (debounced)    ┌──────────────────┐
│  contenteditable   │ ────────────────────▶ │   localStorage   │
│  title + content   │ ◀──────────────────── │  (auto-restore)  │
└─────────┬──────────┘        load            └──────────────────┘
          │  Share
          ▼
  title + "\n[---NOTE-SEPARATOR---]\n" + content
          │
          ├─▶ base64  ──▶  https://your.site/?note=<base64>        (online link)
          │
          └─▶ inline HTML snapshot ──▶ data:text/html;charset=utf-8,… (offline snapshot)
```

* **Encoding**: the note is joined with a separator, UTF-8 encoded, then base64-encoded (`btoa(unescape(encodeURIComponent(...)))`).
* **Snapshot**: a tiny read-only HTML page is generated on the fly, with the note injected via `JSON.stringify` to prevent script injection, plus its own theme toggle and a link back to the editor.
* **Size guard**: links longer than ~1.8 M characters are rejected with a friendly toast.

## 🛠️ Tech Stack

* Vanilla **HTML / CSS / JavaScript** (ES2015+), IIFE-scoped, no globals
* [Tailwind CSS](https://tailwindcss.com/) via CDN, with CSS variables for theming
* [Lucide](https://lucide.dev/) icons via CDN
* GitHub Actions → GitHub Pages for deployment

## ⚠️ Limitations & Privacy

* Notes are stored **only in your browser's `localStorage`** – clearing site data will delete them. Nothing is ever sent to a server.
* Share links contain the **entire note in plain (base64) text**. Anyone with the link can read it. Do not share sensitive information this way.
* Very large notes may exceed browser URL length limits, especially for the Data-URL snapshot.
* Only one note is kept at a time; opening a shared link replaces the current note.

## 🤗 Contributing

Issues and pull requests are welcome! Since the whole project is a single file, the barrier to entry is intentionally low – just edit `index.html`.

## 📄 License

This project is licensed under the **GNU Affero General Public License v3.0**. See [LICENSE](./LICENSE) for details.
