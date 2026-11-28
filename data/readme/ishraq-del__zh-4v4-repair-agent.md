# 🎮 مهارة إصلاح C&C Generals Zero Hour 4v4

> **خبير الإصلاح الشبكي** لمباريات 8 لاعبين LAN. يشتغل على نفس موديل Sisyphus، يفهم مشاكل اللعبة بعمق، يقدر يصلح الكمبيوترات البعيدة عبر SSH تلقائياً.

---

## 📌 المشكلة

لما تلعب **Command & Conquer: Generals Zero Hour** مع 8 شباب LAN:
- الـ **mid-game desync** (10-30 دقيقة) — "Game has detected a mismatch"
- الـ **late-game crash** — "Serious Error" أو "Fatal Error"
- الـ **Twilight Flame** — الوحدات تعلق على حواف المنحدرات
- الـ **slide show** — اللعبة تبطئ بعد 15 دقيقة

المهارة تحل كل هذا.

---

## 🚀 التثبيت (5 دقائق)

### 1. ثبّت opencode على كمبيوتر الـ Master

لازم يكون Windows 10/11. حمّل من https://opencode.ai

### 2. فعّل OpenSSH Server على الـ 7 أجهزة الباقية

على كل جهاز، كـ Administrator، شغّل PowerShell:

```powershell
Add-WindowsCapability -Online -Name OpenSSH.Server~~~~0.0.1.0
Start-Service sshd
Set-Service -Name sshd -StartupType 'Automatic'
New-NetFirewallRule -DisplayName "OpenSSH" -Direction Inbound -LocalPort 22 -Protocol TCP -Action Allow -Profile Private
```

### 3. انقل المهارة إلى opencode

انسخ مجلد `zh_repair_agent/` كاملاً إلى:

```
C:\Users\<user>\.config\opencode\skills\zh-4v4-repair-agent\
```

أو لو تبي على مستوى المشروع، إلى:

```
<project>\.opencode\skills\zh-4v4-repair-agent\
```

### 4. (اختياري) فعّل المفتاح العام عشان ما يطلب كلمة سر

على الـ Master:
```powershell
ssh-keygen -t ed25519 -f $env:USERPROFILE\.ssh\zh_repair_key
```

على كل جهاز LAN (مرة وحدة، يتطلب كلمة السر):
```powershell
ssh-copy-id -i $env:USERPROFILE\.ssh\zh_repair_key.pub admin@192.168.1.11
```

### 5. (اختياري) ثبّت GenPatcher على كل جهاز

حمّل من https://legi.cc/genpatcher/ → Run as Administrator → Apply Fixes → Install GenTool.

---

## 💬 الاستخدام

### أوامر تفهمها المهارة تلقائياً

| قل | المهارة تفهم |
|-----|--------------|
| "تأكد من الشباب" | تشيك كل الـ 8 PCs، تعدّل الإعدادات الخاطئة |
| "جهز الجلسة" | تشيك كامل، تجهز كل شي قبل ما تبدأ اللعب |
| "صار desync" | تحلل المشكلة تلقائياً، تشخّص السبب، تصلحه |
| "مين فيه مشكلة" | تحدد اللاعب/الكمبيوتر اللي يسبب desync |
| "شيك الكمبيوترات" | فحص سريع للحالة |
| "twilight flame" | خريطة Twilight Flame، توصيات خاصة |
| "4v4 desync" | تشخيص كامل لمشكلة desync |
| "8 player LAN" | إعداد جلسة LAN |

### أمثلة محادثات

**قبل الجلسة:**
```
أنت: جهز الجلسة
المهارة: [تشيك 8 PCs] → 6 ✅، 1 ⚠ (MaxParticleCount=2500)، 1 ❌ (GenTool مفقود)
       أنصلح الاتنين قبل ما نبدأ؟
أنت: نعم
المهارة: [تصلح] → كله ✅. ابدأ المباراة.
```

**لما يصير desync:**
```
أنت: صار desync عند الدقيقة 18
المهارة: [تحلل] → السبب: PC-3 عنده Generals.exe مختلف (LAA patched)
       GenTool عنده reduced mode على PC-3.
       الإصلاح: نحذف LAA patch من PC-3 ونعيد تثبيت Generals.exe الأصلي.
       أعملها؟
أنت: افعلها
المهارة: [تنشر الإصلاح] → تم. PC-3 عاد للوضع الطبيعي. جرّب المباراة مرة ثانية.
```

---

## 📁 هيكل المهارة

```
zh_repair_agent/
├── SKILL.md                        # الملف الرئيسي (يقرأه الموديل أولاً)
├── README.md                       # هذا الملف
├── references/
│   ├── domain-knowledge.md         # ليش تصير desyncs (المعرفة العميقة)
│   ├── known-fixes.md              # أوامر جاهزة للتطبيق
│   ├── diagnostic-procedures.md    # runbook لكل مشكلة
│   ├── peer-connect.md             # إعداد SSH/WinRM
│   └── safety-rules.md             # أشياء لا تعملها أبداً
├── assets/
│   ├── checklist.md                # قائمة ما قبل كل جلسة
│   ├── desync-decision-tree.md     # شجرة التشخيص
│   └── ini-templates.md            # INI جاهزة للنسخ
└── scripts/
    └── fleet-check.ps1             # (اختياري) سكريبت فحص سريع
```

---

## 🧠 اللي تعرفه المهارة

| الموضوع | التفاصيل |
|---------|----------|
| **GenPatcher v2.14** | يصلح Win 10/11، يفرض MaxParticleCount=1000 |
| **GenTool v8.8** | anti-cheat + widescreen + observer |
| **TheSuperHackers weekly** | يصلح الـ 8 memory leaks + pathfinder bug |
| **MaxParticleCount=1000** | السبب الأول للـ desync (80% من الحالات) |
| **30 FPS lockstep** | المحرك hardcoded 30 FPS، 500ms latency budget |
| **LAA vs GenTool** | متعارضين، اختار واحد |
| **Hamachi vs Physical LAN** | فيزيائي أفضل بكثير |
| **Twilight Flame** | استعمل BagaturKhan fixed version |

---

## 🔧 المشاكل المعروفة والحلول السريعة

### "data mismatch" في 10-30 دقيقة
1. تحقق من `MaxParticleCount = 1000` على الـ 8 (السبب الأول — 80% من الحالات)
2. تحقق من تطابق `Generals.exe` و `game.dat` SHA256 على الـ 8
3. ثبّت TheSuperHackers weekly لو ما ثبت (يصلح الـ 8 memory leaks)

### "Twilight Flame lag"
- **استعمل** [BagaturKhan fixed version](https://www.moddb.com/games/cc-generals-zero-hour/addons/twilight-flame-fixed-version) — الخريطة الرسمية فيها bug موثّق (Twilight Flame exception handler "يعمل بالعكس")

### "Game won't start"
- شغّل GenPatcher → Apply Fixes (يصلح 50+ مشكلة، يثبت runtimes ناقصة، يصلح الـ registry)
- شيك أن مسار التثبيت بدون أحرف عربية أو خاصة

### "One player always desyncs"
- قارن `Generals.exe` و `game.dat` SHA256 عنده بالـ 7 الباقيين
- شيك الـ Mods (ROTR, Contra, ShockWave) عنده
- شيك الـ antivirus (خاصة Malwarebytes)
- شيك إذا OneDrive عنده يغيّر مسار Documents

### "Slow / lag spikes"
- شيك الكابلات (Cat5e gigabit، لا WiFi)
- اقتل OneDrive، Discord، ICQ، Malwarebytes قبل матч
- شيك CPU الـ host: المحرك single-threaded، واحد core بـ 100% = bottleneck

---

## ⚠️ حدود المهارة

- **Master PC لازم Windows 10/11.** Linux/macOS ما تشتغل (تحتاج PowerShell).
- **الـ 7 PCs الباقيين لازم OpenSSH Server OR WinRM مفعّل.** بدون هذا، ما تقدر تتحكم.
- **4v4 (8 players) هو الحد الأقصى.** Legionnaire نفسه يقول "1 mismatch per 5 6+ player matches is normal" — حتى مع كل الإصلاحات. 3v3 أكثر استقراراً بكثير. لو الـ user يبغى desync صفر، العب 2v2 أو 3v3.
- **اللعبة عمرها 23 سنة.** ما في patch رسمي من EA. الإصلاحات من المجتمع (TheSuperHackers, GenPatcher, GenTool).
- **v1.04 نفسه فيه bugs موثّقة في الكود المصدري** (8 memory leaks، pathfinding regression). ما في حل كامل — الحل الواقعي = TheSuperHackers weekly + GenPatcher + GenTool + إعدادات صحيحة.

---

## 📞 للمساعدة

- المهارة نفسها فيها `references/` لكل ما تحتاجه
- Web: [GenPatcher FAQ](https://legi.cc/bugs-solutions-and-faq/)، [TheSuperHackers GitHub](https://github.com/TheSuperHackers/GeneralsGameCode)، [GameReplays](https://www.gamereplays.org/cnczerohour/)
- مجتمعات: [GameReplays Generals ZH](https://www.gamereplays.org/community/forumdisplay.php?fid=86)، [Revora Generals](https://forums.revora.net/forum/50-generals/)

---

## 📋 Checklist سريع قبل أي جلسة

```
[ ] الـ 8 PCs على نفس الـ subnet
[ ] SSH مفتوح على الـ 7
[ ] GenPatcher v2.14 على الـ 8
[ ] GenTool v8.8 على الـ 8
[ ] TheSuperHackers weekly على الـ 8
[ ] MaxParticleCount=1000 على الـ 8
[ ] SendDelay=yes على الـ 8
[ ] IPAddress set على الـ 8
[ ] Maps CRC identical على الـ 8
[ ] لا VPN (Hamachi/Radmin)
[ ] لا Antivirus (خاصة Malwarebytes)
[ ] لا OneDrive
[ ] كابلات Cat5e gigabit
```

لو كل شي ✅: **ابدأ اللعب.**

---

صُنع بـ ❤️ لمجموعة LAN حقتك. بالتوفيق في матches.
