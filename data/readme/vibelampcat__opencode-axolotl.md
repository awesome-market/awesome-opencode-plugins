# 🦎 OpenCode — ArgonBug Edition (Native Desktop Axolotl Mascot)

> [!IMPORTANT]
> ### 💖 Credits & Attribution
> This project is an unofficial, community-driven modified fork of **[OpenCode](https://github.com/anomalyco/opencode)** developed by **AnomalyCo**.  
> Huge thanks and sincere appreciation to the original authors and the open-source community behind OpenCode for creating such an exceptional, lightning-fast AI coding agent.  
> This build extends their open-source foundation under the **MIT License** by integrating a native 8-bit desktop Axolotl companion pet (**ArgonBug**).

A custom fork of [OpenCode](https://github.com/anomalyco/opencode) featuring a native 8-bit Minecraft-inspired Axolotl desktop pet that lives on top of your windows and reacts to every step of your AI coding agent in real time.

---

## ✨ Why This Exists

While Claude Code has its famous terminal crab, OpenCode officially decided not to add a built-in mascot. So we built our own — and made it even better.

Instead of being trapped inside a scrolling terminal line, **ArgonBug** is a lightweight, transparent desktop overlay (Always on Top) wired directly into the OpenCode core via local UDP sockets. You can drag him anywhere on your screen, minimize your terminal, watch YouTube, and still see at a glance whether your agent is thinking, writing code, running tests, or hitting rate limits.

---

## 🚀 Key Features

* 📦 **Single Portable Executable (`opencode.exe`):** No Python, Qt, or external dependencies required. Just download one `.exe` from Releases and run it.
* ⚡ **Real-Time Core Sync (`UDP:51515`):** Directly hooked into OpenCode's internal lifecycle events.
* 🎨 **5 Animated States:**
  * **IDLE:** Chills with a steaming cup of pixel tea (*"Пью чай, не отвлекай"* / *"Waiting for boss's specs"*).
  * **THINKING:** Glowing cyan gill tips pulse while the model plans (*"Argon думает, тихо..."*).
  * **WORKING:** Fast pixel foot-tapping with flying yellow sparks while editing files (*"Flash пилит код!"*).
  * **TESTING:** Puts on protective cyan goggles when running builds or test suites.
  * **LIMIT:** Takes a nap with floating *z Z z* particles when API rate limits are hit.
* 🖱️ **Full Tray & Drag Control:** Drag and drop the mascot anywhere on your desktop. Right-click the custom system tray icon to check UDP connection status, toggle auto-sync, or manually preview any animation state. Survives even if you close the CLI window!
* 🤖 **Model-Agnostic (Fun Easter Egg):** Because ArgonBug listens to OpenCode's core events rather than a specific API, he works with Gemini, Claude, GPT, Qwen, DeepSeek, or local Ollama models. *(Note: Even if you run Claude Sonnet under the hood, ArgonBug will still claim that "Argon is thinking" and "Flash is coding" — it's not a bug, it's a signature Easter egg!)*

---

## 📥 Quick Start (Windows x64)

1. Go to the **Releases** page of this repository.
2. Download the standalone `opencode.exe`.
3. Double-click `opencode.exe` (or drop it into a folder in your PATH, such as `%APPDATA%\npm`, to replace the standard `opencode` command globally).
4. Start coding — your pixel Axolotl will automatically pop up on screen!

---

## 🛠️ Building from Source

If you want to customize the phrases (`argon_bug/config.py`) or pixel sprite (`argon_bug/renderer.py`):

1. **Install Python dependencies:**
   ```bash
   pip install -r argon_bug/requirements.txt
   ```
2. **Compile the mascot widget into a standalone binary:**
   ```cmd
   build_monolith.bat
   ```
   *(or manually via Nuitka)*:
   ```bash
   python -m nuitka --onefile --windows-console-mode=disable --enable-plugin=pyside6 argon_bug/main.py -o dist/argon_bug.exe
   ```
3. **Bundle into OpenCode CLI using Bun:**
   ```bash
   bun install
   bun run build
   ```

---

## 🇷🇺 О проекте (Кратко на русском)

**OpenCode — ArgonBug Edition** — это модифицированная сборка OpenCode со встроенным 8-битным десктоп-маскотом (пиксельным аксолотлем), который живёт поверх всех окон, перетаскивается мышкой, сворачивается в системный трей и в реальном времени показывает, чем занят ваш ИИ-агент (думает, пишет код, гоняет тесты или ждёт сброса лимитов).

* **Установка в один клик:** скачайте готовый автономный `opencode.exe` из раздела Releases — установка Python и библиотек не требуется.
* **Работает с любыми моделями:** Gemini, Claude, Qwen, DeepSeek или локальные модели через Ollama (при этом Аргончик по пасхалке всё равно будет думать, что за рулём сидят Argon и Flash).

---

## ⚠️ Disclaimer & Credits

* **Upstream Project:** Based on [OpenCode](https://github.com/anomalyco/opencode) by AnomalyCo, licensed under the MIT License.
* **Fan-Made Status:** This is an unofficial, completely non-commercial, open-source fan project created for educational and personal use.
* **Trademarks:** The pixel mascot design is inspired by the Axolotl from **Minecraft** (a trademark of Mojang Studios / Microsoft) and built with **Gemini** workflows in mind (a trademark of Google LLC). This project is not affiliated with, endorsed, or sponsored by Mojang Studios, Microsoft, Google, or AnomalyCo.
