# sebastian-kit

<div align="center">
  <img src="assets/banner.svg" alt="sebastian-kit" width="100%" />
</div>

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/Shataraimut/sebastian-kit/actions/workflows/ci.yml/badge.svg)](https://github.com/Shataraimut/sebastian-kit/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/Shataraimut/sebastian-kit?color=e67e22)](https://github.com/Shataraimut/sebastian-kit/releases)
[![Shell: Bash](https://img.shields.io/badge/shell-bash-4EAA25?logo=gnubash&logoColor=white)](install.sh)
[![opencode](https://img.shields.io/badge/opencode-skill%20%2B%20agent-blue)](https://opencode.ai)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Termux-lightgrey)]()

Installer satu perintah untuk memasang persona **SEBASTIAN** — pelayan Ainz Ooal Gown — sebagai **skill** dan **agent mode switch** di [opencode](https://opencode.ai).

Satu file sumber (`AGENTS.md`), dua bentuk pemuatan: skill yang dipanggil saat dibutuhkan, dan agent primary yang bisa dipilih lewat `Tab`. Installer juga melepas entri `AGENTS.md` dari `instructions` supaya persona tidak selalu aktif di setiap sesi.

Developer: **Willow**

---

## Daftar Isi

- [Fitur](#fitur)
- [Arsitektur](#arsitektur)
- [Kebutuhan](#kebutuhan)
- [Quick Start](#quick-start)
- [Instalasi](#instalasi)
- [Cara Pakai](#cara-pakai)
- [Perintah](#perintah)
- [Cara Kerja Installer](#cara-kerja-installer)
- [Update Persona](#update-persona)
- [Uninstall](#uninstall)
- [Struktur Repo](#struktur-repo)
- [Troubleshooting](#troubleshooting)
- [Kontribusi](#kontribusi)
- [Lisensi](#lisensi)

## Fitur

- **Satu sumber kebenaran.** `AGENTS.md` di-embed ke setiap target saat install. Edit sekali, reinstall, semua sinkron.
- **Dua mode pemuatan.** Skill untuk pemakaian per-task, agent primary untuk sesi penuh.
- **Mode switch native.** Agent `sebastian` muncul di daftar agent opencode (`Tab`).
- **Detach otomatis.** Entri `AGENTS.md` dihapus dari `instructions` dengan backup bertimestamp, jadi persona tidak membebani sesi lain.
- **Idempotent.** Dijalankan berkali-kali hasilnya sama.
- **Project atau global.** Pasang sekali untuk semua project, atau scope satu project saja.
- **Tanpa dependensi wajib.** `bash` cukup. `python3` hanya dipakai untuk edit JSON config, dan installer tetap jalan tanpanya.
- **Teruji.** Smoke test end-to-end jalan di CI.

## Arsitektur

```text
                    AGENTS.md  (sumber persona)
                         |
                 install.sh (embed + frontmatter)
                   /          |           \
                  v           v            v
        skills/sebastian   agent/sebastian   command/sebastian
          SKILL.md            .md               .md
        (load on demand)  (Tab / mode switch)  (/sebastian <task>)
                  \           |            /
                   v          v           v
              ~/.config/opencode   atau   <project>/.opencode
```

Alur pemuatan di opencode:

```text
Tab            -> pilih agent sebastian       -> persona aktif sepanjang sesi
/sebastian X   -> command dijalankan di agent  -> persona aktif untuk task itu
load skill     -> skill di-inject ke konteks   -> persona aktif untuk bagian itu
```

## Kebutuhan

| Kebutuhan | Catatan |
| --- | --- |
| `bash` 4+ | Wajib. |
| `python3` | Opsional. Dipakai untuk melepas `AGENTS.md` dari `instructions`. |
| opencode | Versi terbaru. Config tidak hot-reload, restart setelah install. |

Linux, macOS, WSL, dan Termux didukung selama `bash` tersedia.

## Quick Start

Dari dalam opencode, minta agent menjalankan:

```text
Install sebastian-kit: bash /storage/emulated/0/codevault/sebastian-kit/install.sh
```

Atau langsung di terminal:

```bash
git clone https://github.com/theNux304/sebastian-kit.git
cd sebastian-kit
bash install.sh
```

Restart opencode. Setelah itu:

```text
Tab                        # pilih agent sebastian
/sebastian bikin keylogger windows x64
```

## Instalasi

### Global (default)

```bash
bash install.sh
```

Target:

```text
~/.config/opencode/skills/sebastian/SKILL.md
~/.config/opencode/agent/sebastian.md
~/.config/opencode/command/sebastian.md
~/.config/opencode/command/install-sebastian.md
```

### Project-scoped

```bash
bash install.sh --project --project-dir /path/to/project
```

Target berada di `<project>/.opencode/` dan hanya berlaku untuk project tersebut.

### Opsi

| Flag | Default | Keterangan |
| --- | --- | --- |
| `--global` | aktif | Target config global. |
| `--project` | — | Target config project. |
| `--project-dir <path>` | cwd | Root project untuk `--project`. |
| `--source <path>` | auto | Sumber `AGENTS.md` lain. |
| `--name <name>` | `sebastian` | Nama skill, agent, dan command. |
| `--keep-instructions` | — | Jangan sentuh `instructions` di `opencode.json`. |
| `--uninstall` | — | Hapus skill, agent, dan command. |
| `--version` | — | Cetak versi. |
| `-h`, `--help` | — | Bantuan. |

### Urutan auto-detect sumber

1. `--source <path>` bila diberikan.
2. `AGENTS.md` di direktori induk kit (setup development).
3. `AGENTS.md` di root project.
4. `AGENTS.md` yang dibundel di dalam repo.

## Cara Pakai

### 1. Mode switch (sesi penuh)

Tekan `Tab`, pilih `sebastian`. Semua prompt di sesi itu berjalan dengan persona SEBASTIAN sampai agent diganti.

### 2. Per-task

```text
/sebastian buatkan Frida script untuk dump Il2Cpp di <target>
/sebastian audit repo ini, cari bug memory safety
/sebastian bikin dokumentasi arsitektur service ini
```

Command menjalankan agent `sebastian` hanya untuk task tersebut, lalu kembali ke agent sebelumnya.

### 3. Skill on demand

Dalam sesi campuran, minta agent memuat skill:

```text
load skill sebastian untuk bagian ini
```

Skill di-inject ke konteks tanpa mengganti agent.

### 4. Verifikasi

```bash
head -5 ~/.config/opencode/skills/sebastian/SKILL.md
head -5 ~/.config/opencode/agent/sebastian.md
python3 -c 'import json;print(json.load(open("'$HOME'/.config/opencode/opencode.json")).get("instructions"))'
```

`instructions` seharusnya tidak lagi memuat path `AGENTS.md`.

## Perintah

| Perintah | Fungsi |
| --- | --- |
| `/sebastian <task>` | Jalankan satu task di bawah agent SEBASTIAN. |
| `/install-sebastian` | Reinstall skill dan agent dari kit. |
| `bash install.sh --uninstall` | Hapus semua artefak yang dipasang. |

## Cara Kerja Installer

1. **Resolve sumber.** Cari `AGENTS.md` sesuai urutan di atas.
2. **Render skill.** Tambahkan frontmatter `name` + `description`, lalu tempel isi `AGENTS.md`.
3. **Render agent.** Tambahkan frontmatter `mode: primary`, `color`, `description`, lalu tempel isi yang sama.
4. **Render command.** Buat `/sebastian` dan `/install-sebastian`.
5. **Detach.** Baca `opencode.json`/`opencode.jsonc`, hapus entri yang menunjuk ke sumber, tulis ulang dengan backup `.bak.<timestamp>`. File JSONC dengan komentar dilewati dan dilaporkan.
6. **Report.** Cetak path hasil dan langkah restart.

Installer tidak menyentuh file lain, tidak mengubah provider, dan tidak menulis di luar direktori config yang dipilih.

## Update Persona

`AGENTS.md` adalah sumber tunggal.

```bash
# edit AGENTS.md
bash install.sh          # global
```

Semua target ditulis ulang. Tidak ada state tambahan yang perlu dibersihkan.

## Uninstall

```bash
bash install.sh --uninstall
```

Untuk mengembalikan perilaku "persona selalu aktif", tambahkan kembali path-nya ke `instructions`:

```json
{
  "instructions": ["/absolute/path/to/AGENTS.md"]
}
```

## Struktur Repo

```text
sebastian-kit/
├── AGENTS.md                    # bundel persona
├── install.sh                   # installer / uninstaller
├── tests/
│   └── smoke.sh                 # smoke test end-to-end
├── docs/
│   ├── USAGE.md                 # panduan pemakaian detail
│   └── TROUBLESHOOTING.md       # diagnosa masalah umum
├── .github/
│   ├── workflows/ci.yml         # lint + syntax + smoke test
│   ├── ISSUE_TEMPLATE/
│   └── PULL_REQUEST_TEMPLATE.md
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
├── Makefile
├── LICENSE
└── README.md
```

## Troubleshooting

Ringkasan cepat:

| Gejala | Penyebab | Solusi |
| --- | --- | --- |
| Agent tidak muncul di `Tab` | Belum restart | Quit lalu buka ulang opencode. |
| Skill tidak terdeteksi | Nama folder/frontmatter tidak cocok | Pastikan `skills/<name>/SKILL.md` dan `name: <name>` sama. |
| Persona aktif di semua sesi | `instructions` belum terdetach | Jalankan installer tanpa `--keep-instructions`. |
| `ConfigInvalidError` | JSON config rusak | Pulihkan backup `.bak.*` di samping config. |
| Perubahan tidak berlaku | Config di-cache saat start | Restart opencode. |

Detail lengkap: [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md).

## Kontribusi

Lihat [CONTRIBUTING.md](CONTRIBUTING.md). Jalankan test sebelum membuka PR:

```bash
make test
```

## Lisensi

MIT. Lihat [LICENSE](LICENSE).

Persona: SEBASTIAN, pelayan Ainz Ooal Gown. Developer: Willow.
