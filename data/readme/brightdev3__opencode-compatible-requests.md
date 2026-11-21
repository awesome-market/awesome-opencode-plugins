# OpenCode-compatible requests

[![npm](https://img.shields.io/npm/v/opencode-compatible-requests.svg)](https://www.npmjs.com/package/opencode-compatible-requests)
[![CI](https://github.com/brightdev3/opencode-compatible-requests/actions/workflows/ci.yml/badge.svg)](https://github.com/brightdev3/opencode-compatible-requests/actions/workflows/ci.yml)

A small, dependency-free ESM library for HTTP APIs that accept requests only
from a particular client. You describe the request the upstream expects. The
library handles transport, deadlines, cancellation, JSON decoding, SSE decoding,
and errors.

The core is `createUpstreamClient`. AgentRouter and OpenCode Free are included
as working examples of that core, not as the limit of what it supports. The
package name reflects its origin, but the request wrapper is provider-agnostic.

This calls provider inference endpoints directly. It is **not** the OpenCode
server SDK, does not run agents or tools, and does not start OpenCode.

## Runtime and installation

- **Node.js 20+ or Bun** for the generic client and AgentRouter example.
- **Bun** for the OpenCode Free example, which uses Bun's native `fetch`.
- Some restricted upstreams are sensitive to the HTTP client, including TLS
  behavior. Use the runtime that the upstream accepts. The generic client uses
  the runtime's native `fetch` by default.
- No dependencies, copied configuration, or bundled credentials.

Install from npm:

```sh
npm install opencode-compatible-requests
```

The package is ESM-only.

Runnable examples:

```sh
# Generic upstream
UPSTREAM_URL="https://api.example.com/v1/chat/completions" \
UPSTREAM_API_KEY="..." \
UPSTREAM_MODEL="example-model" \
node examples/generic.mjs "Explain async iterators."

# Generic upstream that requires the full native OpenCode HTTP profile.
# Set your own existing OPENCODE_SESSION_ID and OPENCODE_PROJECT_ID as well.
bun examples/generic-opencode.mjs "Explain async iterators."

# Included examples
node examples/agentrouter.mjs "Explain async iterators."
bun examples/free-title.mjs "Add pagination to customer search."
```

## Generic upstream

Supply the endpoint, headers, and body that the upstream expects. The following
example uses an OpenAI-compatible Chat Completions endpoint, but the request
shape is yours to define.

```javascript
import { createUpstreamClient } from "opencode-compatible-requests";

const client = createUpstreamClient({
  buildRequest(prompt) {
    return {
      url: "https://api.example.com/v1/chat/completions",
      headers: {
        Authorization: `Bearer ${process.env.API_KEY}`,
        "User-Agent": "opencode/2.2.5",
      },
      body: {
        model: "example-model",
        messages: [{ role: "user", content: prompt }],
      },
    };
  },
});

const result = await client.complete("Explain async iterators in one paragraph.");
console.log(result.text);
```

Put the exact client-identifying headers the upstream requires in `headers`.
Depending on the upstream, that can include a user agent, an API key, a session
header, tracing headers, or project metadata. Do not add headers that the
upstream does not need.

Request rules:

- `buildRequest(input, options)` must be synchronous and return
  `{ url, method?, headers?, body?, redirect? }`.
- `body` objects are JSON-serialized. `Content-Type: application/json` is added
  when no content type is present.
- Strings and standard `BodyInit` values pass through unchanged, which supports
  form bodies, uploads, and other non-JSON requests.
- `method` defaults to `POST`.
- `redirect` defaults to `error`, so credentials and session headers are not
  forwarded to another origin.
- `url` must use HTTPS unless `allowInsecure: true` is set. Query strings are
  allowed. URL credentials and fragments are rejected.
- The client does not read environment variables or OpenCode configuration. Pass
  credentials explicitly or read them in your own code.

### Native OpenCode HTTP headers

A short `opencode/<version>` user agent is sufficient for some upstreams, but
not all. `createOpenCodeHeaders` builds the fuller native HTTP profile captured
from OpenCode 2.2.5, independently of the inference protocol:

```javascript
import {
  createOpenCodeHeaders, createUpstreamClient,
} from "opencode-compatible-requests";

const headers = createOpenCodeHeaders({
  // Use metadata from your own existing OpenCode session/project.
  sessionId: process.env.OPENCODE_SESSION_ID,
  projectId: process.env.OPENCODE_PROJECT_ID,
});

const client = createUpstreamClient({
  buildRequest: prompt => ({
    url: process.env.UPSTREAM_URL,
    headers: {
      ...headers,
      Authorization: `Bearer ${process.env.UPSTREAM_API_KEY}`,
    },
    body: {
      model: process.env.UPSTREAM_MODEL,
      messages: [{ role: "user", content: prompt }],
    },
  }),
});

// Run with Bun when that is the transport your upstream accepts.
console.log((await client.complete("Explain async iterators.")).text);
```

| Option | Default | Headers |
| --- | --- | --- |
| `version` | `2.2.5` | Version in `User-Agent` |
| `channel` | `latest` | Release channel in `User-Agent` |
| `client` | `cli` | Client in `User-Agent` and `x-opencode-client` |
| `projectId` | Omitted | `x-opencode-project` |
| `sessionId` | Omitted | `x-opencode-session`, `x-opencode-session-id`, `x-session-id`, `x-session-affinity` |

The default user agent is `opencode/latest/2.2.5/cli`. All four session aliases
use the same supplied value. The helper returns a fresh header object; it adds
neither authorization nor content type. It does not obtain, generate, or rotate
IDs. Missing IDs omit their headers, which can still result in rejection when an
upstream requires the complete profile. Only send metadata to endpoints you trust.

**Matching headers does not match the transport.** In a controlled replay,
the same captured request succeeded with Bun's native `fetch` but returned `403`
with Node's native `fetch`. A minimal user-message body also succeeded in Bun
with the full headers; the agent system prompt and tools were not necessary in
that test. This is evidence of a runtime/transport difference, not proof of a
particular TLS check or a guarantee for every provider. Use the accepted runtime
or explicitly inject an accepted transport with `fetch`.

The included AgentRouter and Free factories keep their narrower profiles;
this helper is opt-in. For capture and comparison instructions, see
[request profiles and `403` diagnosis](https://github.com/brightdev3/opencode-compatible-requests/blob/main/docs/request-profiles.md).

### Decoding responses

The default decoder understands common Chat Completions and Responses API
shapes. For any other response shape, provide `decodeResponse`:

```javascript
const client = createUpstreamClient({
  buildRequest: prompt => ({
    url: "https://api.example.com/v1/generate",
    body: { prompt },
  }),
  decodeResponse(body, response, options) {
    return {
      text: body.result.answer,
      model: body.model,
      finishReason: body.stop_reason,
    };
  },
});
```

`decodeResponse` can return a string or an object with a `text` string. The
original JSON is available as `result.response`. It can be async.

### Streaming

For SSE upstreams, provide `decodeStreamEvent`. It receives one parsed SSE event
at a time and returns one normalized event, an array of events, `null` to ignore
the event, or `{ events, done }` to finish explicitly.

```javascript
import { createUpstreamClient } from "opencode-compatible-requests";

const client = createUpstreamClient({
  buildRequest(prompt) {
    return {
      url: "https://api.example.com/v1/chat/completions",
      headers: { Authorization: `Bearer ${process.env.API_KEY}` },
      body: {
        model: "example-model",
        messages: [{ role: "user", content: prompt }],
        stream: true,
      },
    };
  },
  decodeStreamEvent(event, response, options, state) {
    if (event.data.trim() === "[DONE]") {
      return { type: "finish", reason: state.reason ?? "done", model: options.model };
    }
    const chunk = JSON.parse(event.data);
    const choice = chunk.choices?.[0];
    if (choice?.finish_reason) state.reason = choice.finish_reason;
    const text = choice?.delta?.content;
    return text ? { type: "text", text } : null;
  },
  requireDone: true,
  requireFinish: true,
});

for await (const event of client.stream("Your prompt")) {
  if (event.type === "text") process.stdout.write(event.text);
  if (event.type === "usage") console.log("Usage:", event.usage);
  if (event.type === "finish") console.log("Finished:", event.reason);
}
```

`state` is a fresh object for each stream call, so decoders can remember values
such as a finish reason or model without sharing state between concurrent calls.
The `[DONE]` marker is passed to `decodeStreamEvent` and then ends the stream.
`requireDone` and `requireFinish` turn missing terminal markers into errors.
Without a decoder, `stream()` yields raw `event` events and a synthetic `finish`
event at `[DONE]`.

Streaming events are normalized to:

| Event | Fields | Meaning |
| --- | --- | --- |
| `text` | `text` | Incremental answer text |
| `usage` | `usage` | Provider-native usage object |
| `finish` | `reason`, `model` | Recognized stream termination |
| `event` | `event`, `data` | Raw SSE event when no decoder is supplied |

Usage is not normalized. For example, Chat Completions often uses
`prompt_tokens` and `completion_tokens`, while Responses often uses
`input_tokens` and `output_tokens`.

### Inspect or build requests without sending

```javascript
const { url, init } = client.buildRequest("Your prompt");
// init contains method, headers, body, and redirect.
// Never log init: it can contain an API key or session header.

const response = await fetch(url, { ...init, signal: AbortSignal.timeout(30_000) });
```

`buildRequest()` performs no HTTP call, timeout management, status checking, or
parsing. Those responsibilities are yours when sending a built request yourself.
`complete()` and `stream()` perform the full managed call.

## Included examples

### AgentRouter

AgentRouter uses the Responses API and requires an API key, JSON content type,
and an `opencode/...` user agent. The factory supplies the documented profile.

```javascript
import { createAgentRouterClient } from "opencode-compatible-requests";

const client = createAgentRouterClient({
  apiKey: process.env.AGENTROUTER_API_KEY,
});

const result = await client.complete("Explain async iterators in one paragraph.");
console.log(result.text);
```

The default model is `gpt-6-astra`. Pass provider API model IDs such as
`gpt-6-astra`, **not** OpenCode identifiers such as
`agentrouter-bbidev/gpt-6-astra`. Responses API input arrays and additional
provider parameters are supported through the same client:

```javascript
const result = await client.complete(
  [{ role: "user", content: "Summarize this design." }],
  {
    model: "gpt-6-astra",
    parameters: {
      instructions: "Be concise.",
      max_output_tokens: 200,
    },
  },
);
```

`parameters` passes through to the JSON body. It cannot override `model`,
`input`, or `stream`; use the corresponding client API instead. Parameter
support and validation beyond those reserved fields belong to the provider.

### OpenCode Free

Run this example with **Bun**, and supply your own existing OpenCode session ID
as `OPENCODE_SESSION_ID`. The library neither obtains nor generates session IDs.

```javascript
import { createOpenCodeFreeClient } from "opencode-compatible-requests";

const client = createOpenCodeFreeClient({
  sessionId: process.env.OPENCODE_SESSION_ID,
});

const result = await client.complete(
  "Add pagination to the customer search endpoint.",
);
console.log(result.text);
```

The default model is `mimo-v2.6-flash-free`.

**This recipe uses a title-generation system prompt.** The returned text is
normally a conversation title, not an ordinary assistant answer. The first
1210 characters of that prompt are bundled verbatim as
`OPENCODE_FREE_TITLE_PREFIX`; there are no local capture-file dependencies.
The prefix intentionally ends mid-sentence because this wrapper preserves the
documented request rather than rewriting it.

For ordinary assistant completions through OpenCode, use its real CLI instead:

```sh
opencode run --model opencode/mimo-v2.6-flash-free "Explain async iterators."
```

Free requests always use streaming on the wire, including when calling
`complete()`. Additional Chat Completions parameters can be supplied using
`parameters`, but `model`, `messages`, `stream`, and `stream_options` are
reserved. Only one completion choice (`n: 1`) is supported.

## Configuration

Both the generic client and the included factories accept:

| Option | Default | Purpose |
| --- | --- | --- |
| `timeoutMs` | `60000` | Whole-call deadline. `0` disables it. |
| `fetch` | Native runtime `fetch` | Explicit transport injection, mainly for testing. |
| `allowInsecure` | `false` | Allow `http:` URLs. Generic client only. |
| `requireDone` | `false` | Require `[DONE]` or a decoder done signal. Generic client only. |
| `requireFinish` | `false` | Require a finish event. Generic client only. |

The AgentRouter and OpenCode Free factories also accept `model`, `baseURL`, and
`version`. `baseURL` must be HTTPS. `complete()` and `stream()` accept `model`,
`parameters`, `signal`, and `timeoutMs` per call. Client defaults are not mutated
by per-call overrides, and clients can be reused concurrently.

Use `baseURL` only with an endpoint you trust: the configured key or session ID
is sent there. Changing the version, model, headers, or transport does not
guarantee provider acceptance. A custom `fetch` is an explicit opt-out from the
runtime's default transport; it does not make a different runtime equivalent to
the one the upstream expects.

## Errors, deadlines, and cancellation

```javascript
import {
  APIError, ProtocolError, RequestTimeoutError,
} from "opencode-compatible-requests";

try {
  const result = await client.complete("Your prompt", {
    signal: AbortSignal.timeout(15_000),
    timeoutMs: 30_000,
  });
} catch (error) {
  if (error instanceof APIError) {
    console.error(error.status, error.code, error.retryAfterMs);
  } else if (error instanceof RequestTimeoutError) {
    console.error("The library deadline expired.");
  } else if (error instanceof ProtocolError) {
    console.error("Malformed or incomplete provider response.");
  } else {
    // Caller cancellation, network failure, or invalid configuration.
    throw error;
  }
}
```

- `APIError` exposes optional `status`, provider `code`, `requestId`, and
  `retryAfterMs`. `Retry-After` seconds and HTTP dates are supported. In-band
  errors may have no HTTP status. Its message can contain provider-supplied text.
- `RequestTimeoutError` identifies the library's own deadline and carries
  `timeoutMs`. The deadline includes body reads and time spent consuming an
  async iterator, not just waiting for response headers.
- Caller cancellation propagates the caller's `AbortSignal.reason`.
- Network errors are propagated unchanged. Invalid inputs throw `TypeError`.
- No automatic retries, fallback calls, session rotation, or quota workarounds.
  Client metadata does not remove provider usage limits.
- Nothing is logged by the library. Built requests and raw responses may contain
  sensitive values; do not publish them unredacted.

## How it works

1. `buildRequest` validates the request and serializes object bodies.
2. The transport links the caller's abort signal and a deadline to an internal
   controller, then calls the configured `fetch`.
3. Non-streaming calls read JSON, decode it with `decodeResponse` or the default
   decoder, and return text, model, usage, finish reason, and the original JSON.
4. Streaming calls incrementally decode UTF-8 and parse SSE frames independently
   of transport chunk boundaries, including CRLF, comments, and multiline data.
5. Each SSE event is passed to `decodeStreamEvent`, which maps it to normalized
   text, usage, finish, or raw events.
6. Stream readers, timers, and abort listeners are released on completion,
   error, cancellation, or early iterator exit.
7. Malformed JSON, invalid UTF-8, oversized SSE events, and truncated streams are
   rejected instead of being treated as empty successes.

SSE events have a 1,048,576-character limit. In-band provider errors are rejected
even if the HTTP status was 200. AgentRouter non-streaming raw JSON remains
available in `response`.

## Development

```sh
npm test
bun test
npm pack --dry-run
# Optional declaration check; downloads TypeScript into npm's tool cache.
npm exec --yes --package=typescript@5 -- tsc --noEmit --strict --lib es2022,dom --module nodenext --moduleResolution nodenext type-tests/index.ts
```

Tests use injected fetch functions and synthetic responses, including fragmented
SSE, UTF-8, usage, provider errors, cancellation, and timeouts. They do not call
providers or consume quota.

The ESM implementation is in `src/index.js`, declarations in `src/index.d.ts`,
the generic client in `src/upstream.js`, the included examples in
`src/agentrouter.js` and `src/opencode-free.js`, and the fixed prefix in
`src/title-prefix.js`. The opt-in native HTTP header helper is in
`src/opencode-headers.js`. The provider request skill is in
[`docs/opencode-api/SKILL.md`](docs/opencode-api/SKILL.md). Released under the
[MIT License](LICENSE).
