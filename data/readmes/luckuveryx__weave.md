# Weave

Weave turns your OpenCode sessions into a tank of jellies. Leave it on a spare
screen and you can see which agents are working, which are idle, and which are
waiting for you, without opening a session list.

![A dark round tank with six moon, fried-egg, and white-spotted jellies](docs/images/weave-tank.webp)

_One jelly is one session._

Weave is read-only. It watches your sessions and never sends commands to OpenCode.

## How to read the tank

Every unarchived root session and its subagents become jellies. Archiving a root
hides the whole family. A root session is slightly larger than its own subagents.
A session that remains on screen keeps its place. New sessions fade in, and
sessions that leave fade out.

Each server gets a species in the order you list your servers, cycling through
moon, fried egg, and white-spotted. Connect a laptop, a remote machine, and a
shared server, and the tank shows which sessions come from each one.

A running session is a little brighter. A pending permission glows coral. A
pending question glows amber. An OpenCode outage leaves the jellies already on
screen while Weave tries to reconnect. If it cannot reconnect, restart Weave.

![A selected white-spotted jelly beside its specimen placard with a live close-up, title, source, directory, and status](docs/images/weave-inspect.webp)

_Select a jelly to read its session details and see a live close-up._

Hover or focus a jelly to see its title. Click, tap, or press Enter to open the
placard. Its close-up shows the selected jelly live, and a faint line follows the
jelly to the placard. The title is a button. It copies a text summary of the
session, including the title, source, status, and directory. Escape or a click
on empty water closes the placard. On a phone, the placard becomes a fixed bottom
sheet.

![A coral fried-egg jelly among six jellies, marking a session waiting for permission](docs/images/weave-attention.webp)

## Watch more than one server

Weave connects to one or more OpenCode servers. It reconnects to each server
independently, so an unavailable server does not hide the others. The top-left
status icon is green when every server is connected. It is amber while a server
is connecting or retrying, and red when a server is unavailable. Click or tap it
to see the server names. If the browser loses its connection to Weave, the status
list disappears and a notice asks you to refresh the page.

## Get started

You need Bun 1.4.4 or newer and a reachable OpenCode server.

```sh
bun install
```

Start the server with the URL and password of your OpenCode server:

```sh
WEAVE_OPENCODE_URL=http://127.0.0.1:4096 \
WEAVE_OPENCODE_PASSWORD=your-password \
bun run serve
```

Start the client in another terminal:

```sh
bun run dev
```

Open `http://127.0.0.1:5173`. The client proxies `/rpc` to
`WEAVE_DEV_RPC_URL`, which defaults to `http://127.0.0.1:4310`. If you change
`WEAVE_PORT`, set `WEAVE_DEV_RPC_URL` to match.

## Configuration

| Variable                  | Required | Default     | Meaning                                |
| ------------------------- | -------- | ----------- | -------------------------------------- |
| `WEAVE_OPENCODE_SOURCES`  | no       | none        | Ordered JSON array of OpenCode sources |
| `WEAVE_OPENCODE_URL`      | fallback | none        | URL of the OpenCode server             |
| `WEAVE_OPENCODE_PASSWORD` | fallback | none        | OpenCode password                      |
| `WEAVE_HOST`              | no       | `127.0.0.1` | Host the server listens on             |
| `WEAVE_PORT`              | no       | `4310`      | Port the server listens on             |

For more than one server, set `WEAVE_OPENCODE_SOURCES`:

```sh
WEAVE_OPENCODE_SOURCES='[{"id":"laptop","username":"opencode","password":"replace-laptop-password","url":"http://127.0.0.1:4096"},{"id":"remote","username":"remote-user","password":"replace-remote-password","url":"https://opencode.example.com"}]' \
bun run serve
```

Each entry needs a unique `id`, a `username`, a `password`, and an HTTP or HTTPS
`url`. The array must not be empty. Credentials stay on the backend and never
reach the browser.

When `WEAVE_OPENCODE_SOURCES` is set, it overrides `WEAVE_OPENCODE_URL` and
`WEAVE_OPENCODE_PASSWORD`. Without it, those two variables configure one server
with ID `local`. Invalid configuration stops startup. Restart Weave after a
configuration change.

## How it runs

A Bun server reads sessions from your OpenCode servers. A React client draws the
tank with Three.js from one shared live connection.

The tank shows no visible session list, dashboard, or navigation at rest. The
water makes one orbit in about eight minutes. Jellies pass through one another.
The glass is the only boundary.

## Development

To work on the tank without a real OpenCode server, run:

```sh
bun run dev:mock
```

This starts a fake OpenCode, the Weave server, and the client. It prints
`DEV_READY` with the UI URL and a control URL for switching fixtures, including a
session that leaves and returns.

Other commands:

- `bun run check` runs typecheck, lint, format check, and tests.
- `bun run build` writes the client build to `dist/client`.
- `bun run preview` serves that build and proxies `/rpc` to the same server URL as `dev`.
- `bun run verify` runs the RPC and browser checks in `.agents/skills/verify-weave`.
- `bun run format` formats the repository.
