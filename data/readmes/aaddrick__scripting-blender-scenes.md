<p align="center">
  <strong>Scripting Blender Scenes</strong><br>
  <em>A skill for coding agents that build Blender scenes they can't see.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/github/license/aaddrick/scripting-blender-scenes?style=flat" alt="License"></a>
  <a href=".github/workflows/checks.yml"><img src="https://img.shields.io/github/actions/workflow/status/aaddrick/scripting-blender-scenes/checks.yml?label=checks&style=flat" alt="Checks"></a>
  <a href=".github/workflows/plugin-load-check.yml"><img src="https://img.shields.io/github/actions/workflow/status/aaddrick/scripting-blender-scenes/plugin-load-check.yml?label=plugin%20loads&style=flat" alt="Plugin loads"></a>
</p>

<p align="center">
  <a href="https://www.linkedin.com/in/aaddrick/">Connect on LinkedIn!</a>
</p>

Your coding agent can't see Blender's viewport. It works through `bpy` scripts and headless renders, so it calls a fix done because the script ran, the spec says so, or the rest pose looks right. Then the character's foot sinks through the floor on frame 140.

This skill teaches the agent to measure the built, evaluated, world-space scene over the frames that matter, with checks it has seen fail on the defect. It covers modeling, contact and clipping, rigging, animation, lighting, baking, game export, simulation, scatter, delivery, and the `bpy` errors that waste the most time. It installs in Claude Code, Claude Desktop and claude.ai, Codex, Antigravity CLI, Cursor, Devin CLI, Factory Droid, Gemini CLI, GitHub Copilot CLI, Grok Build CLI, Hermes Agent, Kimi Code, OpenCode, Pi, Qwen Code, Muse, and Muse Code.

## Install

<details>
<summary><strong>Claude Code</strong></summary>

```bash
claude plugin marketplace add aaddrick/scripting-blender-scenes
```

```bash
claude plugin install scripting-blender-scenes@scripting-blender-scenes
```

The skill loads on its own when you work on a Blender scene. To load it by hand, type:

```
/scripting-blender-scenes:scripting-blender-scenes
```

</details>

<details>
<summary><strong>Claude Desktop, Cowork, and claude.ai</strong></summary>

**Step 1.** Open **Customize > Plugins**, select **Add**, then **Add marketplace**.

**Step 2.** Choose **Add from a repository**.

**Step 3.** Enter `aaddrick/scripting-blender-scenes`. Leave **Sync automatically** on so the plugin updates when this repository does. Then select **Sync**.

**Step 4.** Select **Add** next to **Scripting blender scenes**.

**Step 5.** Claude confirms the plugin is installed. It also appears in the desktop app and Cowork on the same account.

</details>

<details>
<summary><strong>Codex CLI and Codex app</strong></summary>

Add the marketplace and install the plugin:

```bash
codex plugin marketplace add aaddrick/scripting-blender-scenes
```

```bash
codex plugin add scripting-blender-scenes@scripting-blender-scenes
```

Check that it installed:

```bash
codex plugin list
```

The Codex app reads the same Codex config, so the plugin shows up there too. Open **Plugins** in the sidebar to see it.

Start a new thread. Codex loads the skill when the task matches. To load it by hand, type:

```
$scripting-blender-scenes:scripting-blender-scenes
```

</details>

<details>
<summary><strong>Antigravity CLI</strong></summary>

```bash
agy plugin install https://github.com/aaddrick/scripting-blender-scenes
```

Check that it installed:

```bash
agy plugin list
```

Start a new session. Antigravity CLI loads the skill when the task matches. To load it by hand, type:

```
/scripting-blender-scenes:scripting-blender-scenes
```

Coming from Gemini CLI? If `agy plugin import gemini` brought this extension over, run the install command above anyway so the current copy replaces the imported one.

</details>

<details>
<summary><strong>Cursor</strong></summary>

In Cursor Agent chat, type:

```
/add-plugin https://github.com/aaddrick/scripting-blender-scenes
```

Or open **Customize**, import a plugin **From GitHub Repository**, and enter `https://github.com/aaddrick/scripting-blender-scenes`. Then select **Install** next to **Scripting Blender Scenes** and choose project or user scope.

A plugin added from a GitHub URL can get stuck on an old commit. For dependable updates, clone the repository into Cursor's local plugin folder instead:

```bash
git clone https://github.com/aaddrick/scripting-blender-scenes.git ~/.cursor/plugins/local/scripting-blender-scenes
```

Then run **Developer: Reload Window**. Clone into that folder, don't symlink to it: Cursor skips symlinks that point outside it. To update, run `git pull` there and reload again.

Check that it installed: open **Customize**, then **Skills**. `scripting-blender-scenes` appears under **Agent Decides**.

Cursor loads the skill when the task matches. To load it by hand, type:

```
/scripting-blender-scenes
```

</details>

<details>
<summary><strong>Devin CLI</strong></summary>

Devin needs a signed-in account to manage plugins. If you are not signed in yet, run `devin auth login` first.

```bash
devin plugins install aaddrick/scripting-blender-scenes
```

Check that it installed:

```bash
devin plugins info scripting-blender-scenes
```

Start a new session. Devin loads the skill when the task matches. To load it by hand, type:

```
/scripting-blender-scenes:scripting-blender-scenes
```

To update it later:

```bash
devin plugins update scripting-blender-scenes
```

</details>

<details>
<summary><strong>Factory Droid</strong></summary>

```bash
droid plugin marketplace add https://github.com/aaddrick/scripting-blender-scenes
```

```bash
droid plugin install scripting-blender-scenes@scripting-blender-scenes
```

Check that it installed:

```bash
droid plugin list
```

In a Droid session, run `/skills` and open the Plugins tab to see the skill. Droid loads it when the task matches. To load it by hand, type `/scripting-blender-scenes` at the start of a prompt.

To update it later:

```bash
droid plugin marketplace update scripting-blender-scenes
droid plugin update scripting-blender-scenes@scripting-blender-scenes
```

</details>

<details>
<summary><strong>Gemini CLI</strong></summary>

```bash
gemini extensions install https://github.com/aaddrick/scripting-blender-scenes
```

Check that it installed:

```bash
gemini extensions list
```

The output lists `scripting-blender-scenes` under **Agent skills**. Start a new session. Gemini CLI loads the skill when the task matches and asks you to approve it first. To load it by hand, ask Gemini to use the `scripting-blender-scenes` skill.

To update it later:

```bash
gemini extensions update scripting-blender-scenes
```

</details>

<details>
<summary><strong>GitHub Copilot CLI</strong></summary>

```bash
copilot plugin marketplace add aaddrick/scripting-blender-scenes
```

```bash
copilot plugin install scripting-blender-scenes@scripting-blender-scenes
```

Check that it installed:

```bash
copilot skill list
```

`scripting-blender-scenes` shows under "Plugin skills". Copilot loads it when the task matches. To load it by hand, ask Copilot to use the `scripting-blender-scenes` skill.

</details>

<details>
<summary><strong>Grok Build CLI</strong></summary>

```bash
grok plugin install aaddrick/scripting-blender-scenes --trust
```

Check that it installed:

```bash
grok inspect
```

`scripting-blender-scenes` appears under Skills. Start a new session. Grok loads the skill when the task matches. To load it by hand, type:

```
/scripting-blender-scenes
```

</details>

<details>
<summary><strong>Hermes Agent</strong></summary>

```bash
hermes skills install aaddrick/scripting-blender-scenes/skills/scripting-blender-scenes
```

Check that it installed:

```bash
hermes skills list
```

Start a new session. Hermes loads the skill when the task matches. To load it by hand, type:

```
/scripting-blender-scenes
```

You can install it as a plugin instead, with `hermes plugins install aaddrick/scripting-blender-scenes --enable`. A plugin skill does not load on its own, though: you have to ask Hermes to load the `scripting-blender-scenes` skill each time. The `skills install` route above does not have that limit.

</details>

<details>
<summary><strong>Kimi Code</strong></summary>

Inside Kimi Code, type:

```
/plugins install https://github.com/aaddrick/scripting-blender-scenes
```

Start a new session so the skill loads:

```
/new
```

Check that it installed. The plugin shows as enabled with no errors:

```
/plugins info scripting-blender-scenes
```

Kimi loads the skill when the task matches. To load it by hand, type:

```
/skill:scripting-blender-scenes
```

</details>

<details>
<summary><strong>OpenCode</strong></summary>

OpenCode loads skills from `~/.config/opencode/skills/` on its own. Clone this repository and link the skill folder there:

```bash
git clone https://github.com/aaddrick/scripting-blender-scenes.git ~/.local/share/scripting-blender-scenes
mkdir -p ~/.config/opencode/skills
ln -s ~/.local/share/scripting-blender-scenes/skills/scripting-blender-scenes ~/.config/opencode/skills/scripting-blender-scenes
```

On Windows, copy the folder instead of linking it.

Check that it installed:

```bash
opencode debug skill | grep '"name": "scripting-blender-scenes"'
```

Restart OpenCode. It loads the skill when the task matches. To load it by hand, ask it to use the skill tool to load `scripting-blender-scenes`.

To update, run `git -C ~/.local/share/scripting-blender-scenes pull`.

</details>

<details>
<summary><strong>Pi</strong></summary>

```bash
pi install https://github.com/aaddrick/scripting-blender-scenes
```

Check that it installed:

```bash
pi list
```

Start a new session. Pi loads the skill when the task matches. To load it by hand, type:

```
/skill:scripting-blender-scenes
```

</details>

<details>
<summary><strong>Qwen Code</strong></summary>

```bash
qwen extensions install https://github.com/aaddrick/scripting-blender-scenes:scripting-blender-scenes
```

The `:scripting-blender-scenes` suffix picks the plugin. Leave it off and Qwen asks you to pick one.

Check that it installed:

```bash
qwen extensions list
```

`scripting-blender-scenes` appears under `Skills:`. Restart Qwen Code. It loads the skill when the task matches. To load it by hand, type:

```
/scripting-blender-scenes:scripting-blender-scenes
```

To update it later:

```bash
qwen extensions update scripting-blender-scenes
```

</details>

<details>
<summary><strong>Muse (muse.ai)</strong></summary>

Muse loads skills from `~/workspace/skills/` on its own computer. Paste this command into a Muse chat and ask Muse to run it:

```bash
curl -fsSL https://raw.githubusercontent.com/aaddrick/scripting-blender-scenes/main/scripts/install_muse.sh | bash
```

The script copies the skill folder there and rewrites the `SKILL.md` header into the shape Muse reads. Start a new chat. Muse loads the skill when the task matches. To update, run the command again.

</details>

<details>
<summary><strong>Muse Code</strong></summary>

Clone the repository:

```bash
git clone https://github.com/aaddrick/scripting-blender-scenes.git
```

Install the skill for every project:

```bash
muse skills install scripting-blender-scenes/skills/scripting-blender-scenes --scope user
```

Check that it installed:

```bash
muse skills list
```

Start a new session. Muse Code loads the skill when the task matches. To load it by hand, type:

```
/skill scripting-blender-scenes
```

To install it as a plugin instead, turn on Muse Code's experimental plugins first. Plugins are off by default in Muse Code 1.4.2.

```bash
export MUSE_EXPERIMENTAL_PLUGINS=1
muse plugins marketplace add scripting-blender-scenes aaddrick/scripting-blender-scenes
muse plugins install scripting-blender-scenes@scripting-blender-scenes
```

</details>

<details>
<summary><strong>Any other agent that reads SKILL.md</strong></summary>

Copy the `skills/scripting-blender-scenes/` folder into your agent's skills folder. Keep the whole folder. `SKILL.md` links to the topic files beside it.

</details>

## What the skill asks of the agent

It sizes the job first. A quick fix gets a five-line project note and one controlled check per risk. A moving shot gets the checks for every neighbour the change can break, plus an independent verifier if one is available. A production gets everything.

On every job, the agent:

1. Finds the project's map (build entry point, generators, checks), or writes one.
2. Treats scripts as the source and the `.blend` as output. It edits the scripts and rebuilds.
3. Measures the built, evaluated, world-space result over the frames that matter.
4. Looks and measures. It reads full-size frames from the shot camera, and either check failing is a fail.
5. Names the neighbours of the change and reports what got worse.
6. Does not certify its own work. Someone else verifies it, or the report says nobody did.

A check counts only after it has gone red on a planted defect. A clipping check that never fails proves nothing.

## What is inside

The skill loads in layers. `SKILL.md` routes the agent to the one or two topic files the task needs.

| File | When the agent reads it |
|---|---|
| `SKILL.md` | Every Blender task: job sizing, the six rules, and the routing table |
| `project-map.md` | Finding or writing the project's map |
| `modeling.md` | Changing geometry, booleans, or detail |
| `contact.md` | Something resting on something, or z-fighting |
| `rigging.md` | Building or changing a rig, or skinning |
| `animation.md` | Changing motion, poses, or an animated camera |
| `lighting.md` | Lighting, materials, render settings, still cameras |
| `delivery.md` | Producing the delivered video, stills, or print files |
| `baking.md` | UVs, baking, or texture maps |
| `game-assets.md` | Budgets or glTF export for a game |
| `simulation.md` | Rigid-body or cloth simulation |
| `scatter.md` | Scattering or instancing with Geometry Nodes |
| `verifying.md` | Verifying someone else's work |
| `checks.md` | Choosing or writing a check, or judging a render by eye |
| `trusting-checks.md` | Proving a check catches the defect it claims to |
| `bpy-pitfalls.md` | A Blender error, at the matching section |
| `render-server.md` | A render failing on one machine only |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Corrections and new pitfalls are welcome, especially ones that come with the check that would have caught them.

## Credits

Blender is a trademark of the Blender Foundation. This project is not made or endorsed by the Blender Foundation, and uses the name only to say what the skill is for.

Multi-harness packaging follows the approach of [obra/superpowers](https://github.com/obra/superpowers).

## License

MIT. See [LICENSE](./LICENSE).
