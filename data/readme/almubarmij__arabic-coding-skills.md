# Arabic Terminal RTL for OpenCode and Codex

Make Arabic replies readable in Windows Terminal and other command-line environments that do not reliably render RTL/BiDi text.

English | [العربية](#العربية)

## Why This Exists

Some terminals display Arabic text in the wrong visual order. This package gives OpenCode and Codex a consistent instruction set for terminal-safe Arabic output.

The transformation is intentionally simple:

1. Reverse the character order inside each Arabic-script word.
2. Reverse the word order of each Arabic prose segment.

Examples:

```text
Normal Arabic: الحمد لله
Terminal-safe output: هلل دمحلا

Normal Arabic: السلام عليكم ورحمة الله
Terminal-safe output: هللا ةمحرو مالسلا مكيلعو

Normal Arabic: لا إله إلا الله
Terminal-safe output: هللا ال هلإ ال
```

## Contents

```text
Arabic-Skills/
├─ .opencode/
│  ├─ plugin/
│  │  └─ arabic-terminal-rtl.ts
│  └─ skills/
│     ├─ arabic-terminal-rtl/
│     │  └─ SKILL.md
│     └─ arabic-reverse/
│        └─ SKILL.md
├─ AGENTS.md
├─ arabic-reverse-opencode-prompt.md
├─ codex-arabic-terminal-rtl-plugin.md
├─ codex-instructions.md
├─ opencode.json
└─ README.md
```

## Quick Start: OpenCode

### 1. Copy The Folder

Place `Arabic-Skills/` in your project root.

### 2. Add Or Update `opencode.json`

Create this file in your project root, or merge these fields into your existing `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["./Arabic-Skills/.opencode/plugin/arabic-terminal-rtl.ts"],
  "skills": {
    "paths": ["Arabic-Skills/.opencode/skills"]
  },
  "instructions": ["Arabic-Skills/AGENTS.md"]
}
```

If you run OpenCode from inside `Arabic-Skills/`, the included `opencode.json` is already configured:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["./.opencode/plugin/arabic-terminal-rtl.ts"],
  "skills": {
    "paths": [".opencode/skills"]
  }
}
```

### 3. Restart OpenCode

OpenCode loads config at startup. Restart after changing `opencode.json`, plugins, skills, or instruction files.

### 4. Test

Ask:

```text
اكتب: الحمد لله
```

Expected terminal-safe output:

```text
هلل دمحلا
```

Ask:

```text
اكتب: السلام عليكم ورحمة الله
```

Expected terminal-safe output:

```text
هللا ةمحرو مالسلا مكيلعو
```

## OpenCode Plugin

Plugin path:

```text
.opencode/plugin/arabic-terminal-rtl.ts
```

What it does:

- Injects a high-priority system instruction into OpenCode.
- Enables Arabic terminal RTL mode by default.
- Preserves code, commands, URLs, paths, JSON, YAML, TOML, identifiers, English text, numbers, and slash commands.

What it does not do:

- It does not post-process model output.
- It does not mutate code blocks or machine-readable content.
- It does not replace proper RTL support in applications, websites, or documents.

This design avoids corrupting code, shell commands, config files, URLs, or JSON payloads.

## OpenCode Skills

Primary skill path:

```text
.opencode/skills/arabic-terminal-rtl/SKILL.md
```

Compatibility skill path:

```text
.opencode/skills/arabic-reverse/SKILL.md
```

The skills document when to activate the behavior, examples, preservation rules, punctuation handling, and final self-checks.

## Codex Setup

Codex does not use OpenCode TypeScript plugins directly. Use one of the instruction files instead.

### Option A: Project Instructions

Copy the contents of:

```text
codex-instructions.md
```

into your Codex project instructions.

### Option B: Shared Agent Instructions

Keep or copy this file into your project root:

```text
AGENTS.md
```

### Option C: Plugin-Equivalent Prompt

Use this file as a Codex instruction packet:

```text
codex-arabic-terminal-rtl-plugin.md
```

## Preservation Rules

The agent should preserve these exactly:

- English text
- numbers
- code blocks
- shell commands
- file paths
- URLs
- JSON/YAML/TOML
- identifiers
- package names
- slash commands

If Arabic appears inside executable or machine-readable content, keep that content exact unless the user explicitly asks to transform it.

## Troubleshooting

### OpenCode does not apply the rule

1. Confirm `opencode.json` points to the correct plugin path.
2. Confirm `skills.paths` points to `Arabic-Skills/.opencode/skills`.
3. Restart OpenCode.
4. Run a direct test prompt.
5. Paste the short prompt from `arabic-reverse-opencode-prompt.md` into the session if needed.

### The Arabic looks strange on GitHub

This transformation is for non-BiDi terminal display. GitHub, browsers, documents, and most apps support normal Arabic better. Use normal Arabic in README files and published documentation.

### Code or JSON changed unexpectedly

The instruction says to preserve machine-readable content. If an agent transforms Arabic inside code/config by mistake, add an explicit reminder: "Do not transform Arabic inside code blocks or JSON." 

## Recommended Usage

Use this package for:

- CLI agent replies
- Windows Terminal sessions
- terminal logs shown to humans
- OpenCode or Codex sessions that frequently answer in Arabic

Do not use it for:

- websites with proper RTL support
- GitHub READMEs
- Word/PDF documents
- app UI strings
- source code or config values

## License

Use, copy, and adapt freely for local agent configuration.

---

# العربية

[English](#arabic-terminal-rtl-for-opencode-and-codex) | العربية

## لماذا يوجد هذا المشروع؟

بعض بيئات الطرفية تعرض النص العربي بترتيب بصري غير صحيح. يوفر هذا المجلد تعليمات جاهزة لـ OpenCode وCodex حتى تصبح الردود العربية مقروءة داخل Windows Terminal أو أي طرفية لا تدعم RTL/BiDi بشكل موثوق.

التحويل بسيط ومقصود:

1. قلب ترتيب الحروف داخل كل كلمة عربية.
2. قلب ترتيب الكلمات داخل كل مقطع عربي.

أمثلة:

```text
العربية الطبيعية: الحمد لله
المخرَج المناسب للطرفية: هلل دمحلا

العربية الطبيعية: السلام عليكم ورحمة الله
المخرَج المناسب للطرفية: هللا ةمحرو مالسلا مكيلعو

العربية الطبيعية: لا إله إلا الله
المخرَج المناسب للطرفية: هللا ال هلإ ال
```

## محتويات المجلد

```text
Arabic-Skills/
├─ .opencode/
│  ├─ plugin/
│  │  └─ arabic-terminal-rtl.ts
│  └─ skills/
│     ├─ arabic-terminal-rtl/
│     │  └─ SKILL.md
│     └─ arabic-reverse/
│        └─ SKILL.md
├─ AGENTS.md
├─ arabic-reverse-opencode-prompt.md
├─ codex-arabic-terminal-rtl-plugin.md
├─ codex-instructions.md
├─ opencode.json
└─ README.md
```

## البدء السريع مع OpenCode

### 1. انسخ المجلد

ضع مجلد `Arabic-Skills/` داخل جذر مشروعك.

### 2. أضف أو حدّث `opencode.json`

أنشئ هذا الملف في جذر المشروع، أو ادمج الحقول التالية داخل ملفك الحالي:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["./Arabic-Skills/.opencode/plugin/arabic-terminal-rtl.ts"],
  "skills": {
    "paths": ["Arabic-Skills/.opencode/skills"]
  },
  "instructions": ["Arabic-Skills/AGENTS.md"]
}
```

إذا كنت تشغّل OpenCode من داخل مجلد `Arabic-Skills/`، فالملف الموجود `opencode.json` جاهز مسبقًا:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "plugin": ["./.opencode/plugin/arabic-terminal-rtl.ts"],
  "skills": {
    "paths": [".opencode/skills"]
  }
}
```

### 3. أعد تشغيل OpenCode

OpenCode يحمّل الإعدادات عند التشغيل. أعد تشغيله بعد تعديل `opencode.json` أو ملفات الـ Plugin أو Skill أو التعليمات.

### 4. اختبر الإعداد

اسأل:

```text
اكتب: الحمد لله
```

المخرَج المتوقع للطرفية:

```text
هلل دمحلا
```

ثم اسأل:

```text
اكتب: السلام عليكم ورحمة الله
```

المخرَج المتوقع للطرفية:

```text
هللا ةمحرو مالسلا مكيلعو
```

## Plugin الخاص بـ OpenCode

مسار الملف:

```text
.opencode/plugin/arabic-terminal-rtl.ts
```

وظيفته:

- يضيف تعليمات عالية الأولوية إلى OpenCode.
- يفعّل وضع العربية المناسب للطرفية افتراضيًا.
- يحافظ على الكود، الأوامر، الروابط، المسارات، JSON، YAML، TOML، المعرّفات، النص الإنجليزي، الأرقام، وأوامر slash commands بدون تغيير.

ما لا يفعله:

- لا يعالج مخرجات النموذج بعد توليدها.
- لا يغيّر كتل الكود أو المحتوى المقروء آليًا.
- لا يستبدل دعم RTL الصحيح في التطبيقات أو المواقع أو المستندات.

هذا التصميم يقلل خطر إفساد الكود أو الأوامر أو ملفات الإعدادات أو الروابط.

## Skills الخاصة بـ OpenCode

المهارة الأساسية:

```text
.opencode/skills/arabic-terminal-rtl/SKILL.md
```

مهارة التوافق:

```text
.opencode/skills/arabic-reverse/SKILL.md
```

توضح هذه الملفات متى يتم تفعيل السلوك، والأمثلة، وقواعد الحفظ، والتعامل مع علامات الترقيم، وقائمة التحقق قبل الرد.

## إعداد Codex

Codex لا يستخدم Plugins الخاصة بـ OpenCode مباشرة. استخدم أحد ملفات التعليمات بدلًا من ذلك.

### الخيار أ: تعليمات المشروع

انسخ محتوى الملف التالي إلى تعليمات مشروع Codex:

```text
codex-instructions.md
```

### الخيار ب: تعليمات مشتركة للوكلاء

احتفظ بهذا الملف في جذر المشروع أو انسخه إليه:

```text
AGENTS.md
```

### الخيار ج: بديل شبيه بالـ Plugin

استخدم الملف التالي كحزمة تعليمات لـ Codex:

```text
codex-arabic-terminal-rtl-plugin.md
```

## قواعد الحفظ بدون تغيير

يجب أن يحافظ الوكيل على العناصر التالية كما هي:

- النص الإنجليزي
- الأرقام
- كتل الكود
- أوامر الطرفية
- مسارات الملفات
- الروابط
- JSON/YAML/TOML
- المعرّفات البرمجية
- أسماء الحزم
- أوامر slash commands

إذا ظهر نص عربي داخل محتوى تنفيذي أو مقروء آليًا، فيجب إبقاؤه كما هو ما لم يطلب المستخدم تحويله صراحة.

## استكشاف الأخطاء

### OpenCode لا يطبق القاعدة

1. تأكد أن `opencode.json` يشير إلى مسار الـ Plugin الصحيح.
2. تأكد أن `skills.paths` يشير إلى `Arabic-Skills/.opencode/skills`.
3. أعد تشغيل OpenCode.
4. جرّب اختبارًا عربيًا مباشرًا.
5. عند الحاجة، الصق التعليمات المختصرة من `arabic-reverse-opencode-prompt.md` داخل الجلسة.

### العربية تبدو غريبة على GitHub

هذا التحويل مخصص للطرفيات التي لا تدعم BiDi. GitHub والمتصفحات والمستندات والتطبيقات الحديثة غالبًا تعرض العربية الطبيعية بشكل أفضل. استخدم العربية الطبيعية في ملفات README والوثائق المنشورة.

### تم تغيير كود أو JSON بالخطأ

التعليمات تطلب الحفاظ على المحتوى المقروء آليًا. إذا حوّل الوكيل نصًا عربيًا داخل كود أو إعدادات بالخطأ، أضف تذكيرًا صريحًا: "لا تحوّل العربية داخل كتل الكود أو JSON."

## الاستخدام الموصى به

استخدم هذا المشروع مع:

- ردود وكلاء CLI
- جلسات Windows Terminal
- سجلات الطرفية الموجهة للبشر
- جلسات OpenCode أو Codex التي ترد بالعربية كثيرًا

لا تستخدمه مع:

- المواقع التي تدعم RTL جيدًا
- ملفات README المنشورة على GitHub
- مستندات Word/PDF
- نصوص واجهات التطبيقات
- قيم الكود أو الإعدادات

## الترخيص

يمكنك استخدام هذه الملفات ونسخها وتعديلها بحرية لإعدادات الوكلاء المحلية.
