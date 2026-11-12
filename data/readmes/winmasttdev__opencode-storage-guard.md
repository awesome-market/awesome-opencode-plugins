# opencode-storage-guard

An OpenCode plugin that gives the agent honest answers about disk space, finds
the files that are eating it, and refuses to touch the one copy of your data
that has no backup.

Four read-only-by-default tools are added to the `storage` namespace:

| Tool | Purpose |
| --- | --- |
| `storage_disk_report` | Free/used space per mount, low-space and protected-mount warnings |
| `storage_big_files` | Largest files under a directory (symlinks never followed) |
| `storage_photos_guard` | "Is this path protected, and may I destroy it?" — answered before the fact |
| `storage_cache_clean` | Reclaimable space in known caches; deletes only when you ask it to |

---

## Why

The machine this plugin was written for has a second disk mounted at
`/mnt/GamesProjects`. On it lives the family photo library — the *only* copy.
Not a mirror, not a sync target, just the one NTFS partition that was never
re-imaged because the drive is fragile.

An assistant asked to "free up some disk space" is exactly the kind of actor
that will find the biggest directory and delete it. With this plugin installed
the agent has to go through `storage_photos_guard` first, and the answer for
anything under that mount is a hard `BLOCKED` with the reason attached. The
photos stay.

The same plugin also gives the agent a way to *actually* reclaim space
(safely) instead of guessing which directories are junk.

---

## Installation

The plugin is plain TypeScript with **no runtime dependencies and no build
step** — OpenCode loads `index.ts` directly.

### From a local checkout (`file://` URL)

Add this to `opencode.jsonc` (project level) or
`~/.config/opencode/opencode.json` (global level):

```jsonc
{
  "$schema": "https://opencode.ai/config.json",
  "plugins": [
    {
      "package": "file:///home/winmastt/dev/opencode-storage-guard",
      "options": {
        "protectedPaths": ["/mnt/GamesProjects"],
        "minFreeGb": 20,
        "allowCleanup": true
      }
    }
  ]
}
```

### From a local checkout (plain path)

The same thing without the URL scheme:

```jsonc
{
  "plugins": [
    {
      "package": "/home/winmastt/dev/opencode-storage-guard",
      "options": {
        "protectedPaths": ["/mnt/GamesProjects"],
        "minFreeGb": 20,
        "allowCleanup": true
      }
    }
  ]
}
```

### From npm

Once the package is published, the npm-style form works. The `options` block
is optional — the defaults are safe:

```jsonc
{
  "plugins": [
    {
      "package": "opencode-storage-guard",
      "options": {
        "protectedPaths": ["/mnt/GamesProjects"],
        "minFreeGb": 20,
        "allowCleanup": true
      }
    }
  ]
}
```

> `allowCleanup` is the only switch that can make this plugin destructive.
> Leave it `false` (the default) until you have read the
> [Safety](#safety) section.

---

## Options

All options are optional and are read from `ctx.options`.

| Option | Type | Default | Meaning |
| --- | --- | --- | --- |
| `protectedPaths` | `string[]` | `[]` | Roots that must never be written to, repartitioned, formatted or deleted. Matched as *path prefixes* with a directory boundary, so `/mnt/GamesProjects` protects `/mnt/GamesProjects/photos` but not `/mnt/GamesProjects2`. |
| `minFreeGb` | `number` | `10` | Warn when a mount has less than this many free gigabytes. A warning only — nothing is deleted. |
| `allowCleanup` | `boolean` | `false` | Master switch for `storage_cache_clean`. While `false`, the tool reports reclaimable space but refuses to delete anything. |
| `cleanupTargets` | `string[]` | all targets | Restrict `storage_cache_clean` to these target ids (`pacman`, `npm`, `bun`, `pip`, `journal`, `docker`, `trash`, `gradle`). |
| `maxScanEntries` | `number` | `250000` | Cap on filesystem entries visited during one scan, so a scan of `/` cannot hang the session. |

---

## Tools

### `storage_disk_report`

Reports free and used space for every mounted filesystem.

**Input**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | no | Report which mount contains this path. |

**Returns** a text table with one row per mount (size, used, free, use%,
notes) followed by warnings for low-space mounts, protected mounts and mounts
running out of inodes.

**Example**

```
/mnt/GamesProjects/photos lives on /mnt/GamesProjects (ntfs3 on /dev/sdb1)

Mount                          Size      Used      Free    Use%  Notes
/mnt/GamesProjects             932 GiB   625 GiB   306 GiB  67.1%  PROTECTED
/                              467 GiB   209 GiB   235 GiB  44.7%
/boot/efi                      1022 MiB  24.7 MiB  997 MiB  2.4%

Warnings:
- /boot/efi has only 1.0 GB free (below the 20 GB threshold)
- /mnt/GamesProjects is PROTECTED - never repartition, format or delete it
```

### `storage_big_files`

Walks a directory and returns the largest files.

**Input**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | **yes** | Directory to scan. |
| `limit` | `number` | no | How many files to return (default `25`). |
| `minSizeMb` | `number` | no | Only report files of at least this size in MiB. |
| `crossMounts` | `boolean` | no | Allow the walk to descend into other filesystems (default `false`). |

**Returns** the number of entries visited plus the largest files (biggest
first), each annotated with its size and age.

**Example**

```
Scanned 359 entries under /home/winmastt/dev

  8.7 MiB    5m ago  /home/winmastt/dev/opencode-storage-guard/node_modules/typescript/lib/typescript.js
  5.9 MiB    5m ago  /home/winmastt/dev/opencode-storage-guard/node_modules/typescript/lib/_tsc.js
  1.8 MiB    5m ago  /home/winmastt/dev/opencode-storage-guard/node_modules/typescript/lib/lib.dom.d.ts
  595 KiB    5m ago  /home/winmastt/dev/opencode-storage-guard/node_modules/typescript/lib/lib.webworker.d.ts
  574 KiB    5m ago  /home/winmastt/dev/opencode-storage-guard/node_modules/typescript/lib/typescript.d.ts
```

If the walk hits `maxScanEntries` the output says so explicitly
(`scan stopped early at the entry cap`) instead of silently returning a
partial list.

### `storage_photos_guard`

The guard rail. Answers two questions about a path before anything touches
it: is it inside a protected root, and may the named operation proceed?

**Input**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `path` | `string` | **yes** | Path to check. |
| `operation` | `string` | no | Operation you intend to perform (`delete`, `format`, `write`, …). Default `write`. |

**Returns** `ALLOWED` or `BLOCKED`, the resolved mount, and a plain-English
reason. The following operation names are treated as destructive and are
called out explicitly: `format`, `mkfs`, `repartition`, `resize`, `wipe`,
`delete`, `rm`, `overwrite`, `write`, `clean`, `truncate`. The match is
case-insensitive and catches destructive verbs inside longer names, so
`force-wipe-disk` is destructive too.

**Example — protected root**

```
BLOCKED
path: /mnt/GamesProjects/photos/2024
operation: delete
mount: /mnt/GamesProjects (ntfs3 on /dev/sdb1)
reason: /mnt/GamesProjects/photos/2024 is inside a protected root (/mnt/GamesProjects). Refusing a destructive operation here.
protected roots: /mnt/GamesProjects
```

**Example — anywhere else**

```
ALLOWED
path: /home/winmastt/dev
operation: write
mount: / (ext4 on /dev/sda3)
reason: /home/winmastt/dev is not inside a protected root. write is allowed, but double-check the target.
protected roots: /mnt/GamesProjects
```

### `storage_cache_clean`

Reports how much space could be reclaimed from well-known cache locations and
(optionally) reclaims it.

**Input**

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `target` | `string` | no | Only this target id. |
| `apply` | `boolean` | no | Actually delete. Defaults to `false` (report only). |

**Returns** a per-target line with the reclaimable size and the outcome, plus
the total. Known target ids: `pacman`, `npm`, `bun`, `pip`, `journal`,
`docker`, `trash`, `gradle`.

**Example — dry run**

```
Reclaimable space (dry run - pass apply=true to act):

pacman     11.1 MiB  not applied
npm             0 B  not applied
bun         7.9 MiB  not applied
pip             0 B  not applied
journal         0 B  not applied
docker          0 B  not applied
trash      67.6 KiB  not applied
gradle          0 B  not applied

Total reclaimable: 19.1 MiB
Protected roots: /mnt/GamesProjects
```

With `apply: true` the tool asks OpenCode for permission (`storage-cleanup`)
before it touches anything, and prints `Cleanup applied:` followed by the same
per-target table with the real outcomes.

---

## Safety

The plugin is built so that the worst thing it can do is refuse to work.

- **Dry run by default.** `storage_cache_clean` only reports until you pass
  `apply: true` *and* the instance was started with `allowCleanup: true`.
  Without `allowCleanup`, applying is refused with an explicit message.
- **Protected roots are never touched.** Every path under a `protectedPaths`
  entry is off-limits: the guard blocks destructive operations *and* writes,
  and the cleanup tool skips any target that lives inside a protected root
  (`PROTECTED - skipped`).
- **Destructive operations are named explicitly.** The operation names listed
  above are matched case-insensitively, so a compound name such as
  `reformat-disk` is still treated as destructive.
- **Permission prompt before deletion.** Before anything is removed, the
  plugin calls OpenCode's `ctx.permission.assert` with the action
  `storage-cleanup` and the affected path, so the user gets to approve or
  deny the deletion.
- **Symlinks are never followed.** The scanner uses `lstat` and skips
  symlinks entirely, so it cannot be tricked into leaving the scanned tree,
  looping through a self-referencing link, or reporting a link's target as a
  file inside the tree.
- **Other filesystems are skipped by default.** A scan does not cross a mount
  boundary unless you explicitly ask with `crossMounts: true`.
- **Scans are bounded.** `maxScanEntries` caps the number of filesystem
  entries visited per scan.

Nothing in this plugin repartitions, formats or mounts a filesystem. The
`format` / `mkfs` operation names exist only so the guard can *refuse* them.

---

## Requirements

- **Linux.** The plugin reads `/proc/self/mounts` and measures filesystems
  with `statfs(2)`. On macOS or Windows the disk report is empty and the
  guard still protects configured paths, but the mount-aware parts do nothing.
- **`/proc` mounted** (the usual case on Linux).
- **Node.js or Bun.** The plugin is plain TypeScript with explicit `.ts`
  import extensions, so it runs unmodified under Node's type stripping
  (Node 22.6+ with `--experimental-strip-types`, enabled by default from
  Node 23.6) and under Bun, which is what OpenCode itself uses.
- **No runtime dependencies, no build step.** `npm install` is only needed for
  the TypeScript compiler and `@types/node` used by the tests.

## Development

```bash
npm install --no-audit --no-fund   # dev dependencies only
npx tsc --noEmit                   # type check
npm test                           # node:test suite
```

The test suite covers the formatting helpers, protected-path matching, mount
resolution, option resolution, the guard's destructive-operation handling and
the cleanup target list, plus filesystem behaviour (symlink handling, dry-run
vs. apply) against throwaway temp directories. No network access is required.

## License

[MIT](./LICENSE)
