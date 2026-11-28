# 🦀 Tauri 2 Subagents Pack

> Ten specialized AI coding roles for Tauri 2 + Rust: clearer task boundaries, focused implementation, and structured reviews.

[English](#english) · [العربية](#العربية) · [Harness guide](docs/MULTI-HARNESS.md) · [Contributing](CONTRIBUTING.md) · [MIT license](LICENSE)

Architecture → IPC contracts → Implementation → Security review → Testing → Release preparation

This is a suggested workflow, not an automatically executed pipeline.

<a id="english"></a>
## English

### Built for practical development

Tauri 2 Subagents Pack contains ten role definitions, shared coordination rules, harness-specific profiles, and installation tools for AI-assisted desktop development. The development guidance focuses on Tauri 2 + Rust applications targeting Windows 11 / MSVC. Installer entry points also exist for macOS and Linux.

The maintainer reports using the pack to build applications and testing it in multiple coding environments. This is first-hand maintainer experience, not independent certification or a version-by-version compatibility matrix.

This pack is not an AI model or a standalone agent runtime. It uses the model, tools, permissions, and delegation features available in your coding environment.

### Why use it?

- Separate architecture and contract review from implementation.
- Assign bounded tasks with explicit file ownership.
- Keep security, testing, performance, and packaging responsibilities visible.
- Reuse the role set across multiple harness formats.
- Use installation preview, backup, and restoration tooling.

### The ten roles

| Agent | Responsibility | Intended mode |
| --- | --- | --- |
| `tauri-architect` | Architecture, boundaries, planning, file ownership | Review / read-only |
| `tauri-ipc` | Command, event, channel, serialization, and error contracts | Review / read-only |
| `tauri-rust` | Rust commands, services, state, validation, concurrency | Implementation |
| `tauri-frontend` | Webview UI, typed IPC integration, frontend checks | Implementation |
| `tauri-security` | Capabilities, scopes, CSP, paths, and security findings | Review / read-only |
| `tauri-windows` | WebView2 and Windows desktop integration | Implementation |
| `tauri-plugins` | Plugin integration, dependencies, permissions | Implementation |
| `tauri-test` | Focused regression and integration-test work | Implementation |
| `tauri-perf` | Startup, memory, IPC, and binary-size investigations | Implementation |
| `tauri-release` | NSIS/MSI, signing, updater, release preflight | Implementation |

Read-only describes the intended role boundary. Technical enforcement varies by harness and live-session permissions; see the [harness guide](docs/MULTI-HARNESS.md).

### Harness profiles and integration

| Harness | Default role location | Integration notes |
| --- | --- | --- |
| ZCode | `~/.zcode/agents/*.md` | Agent definitions |
| Claude Code | `~/.claude/agents/*.md` | Agent definitions |
| Cursor | `~/.cursor/agents/*.md` | Agent definitions plus coordination guide |
| OpenAI Codex | `~/.codex/agents/*.toml` | TOML profiles |
| Gemini CLI | `~/.gemini/agents/*.md` | Local agent definitions |
| GitHub Copilot / VS Code | `~/.copilot/agents/*.agent.md` | Custom-agent profiles |
| OpenCode | `~/.config/opencode/agents/*.md` | Separate v1 and v2 permission formats |
| Hermes | `~/.hermes/tauri-pack/roles/*.md` | Delegated role-prompt library, not named-agent registration |

These are eight harness families, not a claim that every version has been runtime-tested. Choose one OpenCode format per destination. Antigravity and other unlisted harnesses have no verified automatic adapter in this pack. Installation success does not prove that agents loaded or that all tools are available.

### Quick start

Get the repository:

```bash
git clone https://github.com/H0777/tauri2-subagents-pack.git
cd tauri2-subagents-pack
```

Review the scripts before running them: installation writes agent and instruction files into local harness configuration.

#### Windows

Use `Install.cmd` for the interactive entry point, or run from the repository root:

```powershell
# Check package structure and PowerShell syntax.
powershell -ExecutionPolicy Bypass -File .\scripts\validate.ps1

# Inspect detected targets and preview installation.
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1 -List
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1 -WhatIf

# Install into detected supported environments.
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1
```

To choose one target explicitly:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1 -Targets claude
```

Detection checks local installation signals, not account features or runtime compatibility.

#### macOS / Linux

```bash
bash Install.sh
```

This launcher invokes `scripts/install.sh`. Windows-focused development guidance should not be interpreted as equal coverage of every desktop target.

### Your first task

Start a new session inside a Tauri project. Select or delegate to the role using your harness's supported mechanism; invocation syntax differs between tools.

```text
Use tauri-architect to inspect this project.
Identify the Tauri version, Rust/frontend boundaries, and configuration files.
Propose a file-ownership plan. Do not modify files.
```

Then try a bounded implementation task, after agreeing on the relevant contracts:

```text
Use tauri-rust for the agreed backend task.
Allowed file: src-tauri/src/download.rs.
Do not change dependencies or shared configuration without approval.
Report changed files, checks run, checks not run, and remaining issues.
```

These are example prompts, not executed demonstrations. Choose files that actually exist in your project. Hermes users must pass the role instructions through their delegation workflow. Follow the [smoke tests](docs/SMOKE-TESTS.md) to verify loading and behavior. Avoid parallel edits to the same shared file.

### Evidence and verification boundaries

The checked-in [PowerShell 5 report](reports/TEST-PS5.log) and [PowerShell 7 report](reports/TEST-PS7.log) each record 57 passing package checks. They cover scenarios such as fresh installation, repeated installation, restoration, backup corruption, and failure handling.

These are stored reports, not a live CI status or a fresh run of the current checkout. Package checks do not prove agent loading in every harness, application correctness, or model quality. Maintainer use and package tests are complementary evidence, not universal compatibility guarantees.

### Backups and restoration

Use the actual backup directory produced for your target:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\restore.ps1 -BackupPath 'C:\path\to\backup-directory'
```

SHA-256 hashes verify integrity; they do not encrypt backups. Keep backups until installation is verified. Multi-target installation is not one transaction: successful targets can remain installed when another target fails. Review installer output before retrying.

### Repository map

| Path | Purpose |
| --- | --- |
| `agents/` | Ten canonical role definitions |
| `profiles/` | Generated harness-specific profiles |
| `AGENTS.md` | Shared coordination and development rules |
| `scripts/` | Installation, generation, validation, restoration |
| `installers/` | Additional platform entry points |
| `docs/` | Technical guides and changelog |
| `reports/` | Stored validation and package-test evidence |

### Documentation and community

- [Harness formats, activation, and limitations](docs/MULTI-HARNESS.md)
- [Post-installation smoke tests](docs/SMOKE-TESTS.md)
- [Validation notes](docs/VALIDATION.md)
- [Changelog](docs/CHANGELOG.md)
- [Contribution guide](CONTRIBUTING.md)
- [Report a problem or share your experience](https://github.com/H0777/tauri2-subagents-pack/issues/new/choose)

Commands here use the repository-root layout; older notes may omit the `scripts/` prefix. Use the actual paths in this checkout.

If the pack helps your Tauri workflow, consider starring the repository. Bug reports, reproducible experience reports, and improvements are equally welcome.

---

<a id="العربية"></a>
## العربية

### حزمة نابعة من الاستخدام العملي

عشرة أدوار متخصصة لتطوير تطبيقات Tauri 2 + Rust بمساعدة الذكاء الاصطناعي، مع قواعد لتوزيع المسؤوليات وملفات تكامل لعدة بيئات. تركّز تعليمات التطوير على Windows 11 / MSVC، وتوجد نقاط دخول للتثبيت على macOS وLinux أيضاً.

بحسب تجربة صاحب المشروع، استُخدمت الحزمة في بناء تطبيقات وجُرّبت في عدة بيئات برمجة. هذه تجربة استخدام من صاحب المشروع، وليست اعتماداً مستقلاً أو إثباتاً لتوافق جميع الإصدارات.

الحزمة ليست نموذجاً مستقلاً ولا تشغّل جميع الوكلاء تلقائياً؛ تعتمد على النموذج والأدوات والصلاحيات وآلية التفويض داخل بيئتك.

### ماذا تضيف إلى طريقة عملك؟

- فصل مراجعة المعمارية وعقود IPC عن التنفيذ.
- تحديد الملفات والمسؤوليات قبل توزيع المهام.
- تخصيص أدوار للأمان والاختبارات والأداء وتجهيز الإصدار.
- إعادة استخدام الأدوار عبر ملفات توافق لعدة بيئات.
- معاينة التثبيت واستخدام أدوات النسخ الاحتياطي والاسترجاع.

الأدوار هي: `tauri-architect` و`tauri-ipc` و`tauri-rust` و`tauri-frontend` و`tauri-security` و`tauri-windows` و`tauri-plugins` و`tauri-test` و`tauri-perf` و`tauri-release`. يوضح الجدول الإنجليزي أعلاه مسؤولية كل دور. المعمارية وIPC والأمان أدوار مراجعة مقصودة للقراءة فقط؛ قوة المنع الفعلي تختلف حسب البرنامج وصلاحيات الجلسة.

### التثبيت والتجربة

نزّل المشروع أو استنسخه، ثم راجع السكربتات قبل تشغيلها. على Windows استخدم `Install.cmd`، أو نفّذ من مجلد المشروع الرئيسي:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\validate.ps1
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1 -List
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1 -WhatIf
powershell -ExecutionPolicy Bypass -File .\scripts\install-all.ps1
```

على macOS وLinux:

```bash
bash Install.sh
```

بعد التثبيت افتح جلسة جديدة داخل مشروع Tauri، واختر الوكيل بالطريقة التي تدعمها بيئتك. ابدأ بطلب مراجعة فقط:

```text
استخدم tauri-architect لفحص المشروع وتحديد إصدار Tauri وحدود Rust والواجهة.
اقترح توزيع مسؤوليات الملفات، دون تعديل الملفات.
```

هذا مثال مقترح، وليس نتيجة تجربة منشورة. بعد المراجعة اتفق على عقود IPC، وحدد ملفات التنفيذ ومعايير القبول، ثم اطلب مراجعة الأمان والاختبارات. لا تكلف وكيلين بتعديل الملف نفسه بالتوازي.

### التوافق والاختبارات

توجد ملفات تكامل لـZCode وClaude Code وCursor وCodex وGemini CLI وGitHub Copilot وOpenCode، ومكتبة تعليمات للتفويض في Hermes. لا يعني وجود الملفات اختبار كل إصدار فعلياً. في Hermes لا تُسجّل الأدوار كوكلاء مسمّاة؛ يجب تمرير تعليماتها عند التفويض. لا تثبّت صيغتي OpenCode في المسار نفسه.

يسجل كل من [تقرير PowerShell 5](reports/TEST-PS5.log) و[تقرير PowerShell 7](reports/TEST-PS7.log) نجاح 57 فحصاً للحزمة. هذه تقارير محفوظة لا حالة CI حية، ولا تثبت صحة التطبيق الناتج أو تحميل الوكلاء داخل كل بيئة. نفّذ [اختبارات التشغيل](docs/SMOKE-TESTS.md) في بيئتك وراجع [حدود التوافق](docs/MULTI-HARNESS.md).

### النسخ الاحتياطي

بصمات SHA-256 للتحقق من سلامة المحتوى وليست تشفيراً. للاسترجاع استخدم `scripts/restore.ps1` مع مسار النسخة الفعلي كما في المثال الإنجليزي. احتفظ بالنسخة حتى تتأكد من نجاح التثبيت، واقرأ مخرجات المثبت لأن تثبيت عدة بيئات قد ينجح جزئياً.

### شارك تجربتك

استخدم [نماذج Issues](https://github.com/H0777/tauri2-subagents-pack/issues/new/choose) للإبلاغ عن مشكلة أو مشاركة تجربة فعلية، مع اسم البيئة وإصدارها ونظام التشغيل وما نجح وما تعذّر. راجع [دليل المساهمة](CONTRIBUTING.md)، ولا تنشر مفاتيح API أو بيانات مشاريع خاصة.

إذا أفادتك الحزمة، يمكنك دعمها بنجمة. التجارب الموثقة والإصلاحات والملاحظات مرحب بها بالقدر نفسه.

## License / الترخيص

[MIT](LICENSE).
