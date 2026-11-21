# Moodle Herd Installer Skill

A skill for AI coding assistants (Claude, OpenCode, etc.) to install and configure **Moodle LMS** on **Laravel Herd**.

## Why This Skill?

Moodle 5.x introduced a new directory structure with a `public/` folder, which causes issues with Laravel Herd/Valet:

- CSS/JS files return HTML instead of actual content
- `ERR_CONTENT_DECODING_FAILED` errors
- Slash arguments not working with Nginx
- Database driver confusion (mysqli vs mariadb)

This skill documents all the solutions discovered through trial and error.

## Key Fixes

| Issue | Solution |
|-------|----------|
| CSS/JS not loading | `$CFG->slasharguments = false;` |
| Gzip decode errors | Add `gzip off;` to Nginx config |
| dirroot errors | Point to `/public` folder |
| DB connection fails | Use `mariadb` driver, port `3307` |

## Installation

### For OpenCode / Claude

Copy the `SKILL.md` file to your skills directory:

```bash
# OpenCode
cp -r moodle-herd-installer ~/.opencode/skills/

# Claude Code
cp -r moodle-herd-installer ~/.claude/skills/
```

### Manual Usage

Just reference the `SKILL.md` file when setting up Moodle on Herd.

## Files

```
moodle-herd-installer/
├── SKILL.md                         # Main skill instructions
├── assets/
│   ├── config.template.php          # Ready-to-use config template
│   └── nginx-gzip-off.conf          # Nginx fix snippet
└── README.md                        # This file
```

## Quick Start

1. Clone Moodle 5.x
2. Link from `public/` folder: `cd moodle/public && herd link moodle`
3. Copy `assets/config.template.php` to `moodle/config.php`
4. Replace placeholders in config
5. Run: `php admin/cli/install_database.php --agree-license`
6. Access: https://moodle.test

## Tested With

- Moodle 5.1.1 (MOODLE_501_STABLE)
- Laravel Herd (Windows)
- MariaDB 10.11
- PHP 8.4

## Contributing

Found another issue? PRs welcome!

## License

MIT
