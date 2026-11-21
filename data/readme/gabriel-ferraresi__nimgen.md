<p align="center">
<h1 align="center">🎨 NIMGEN</h1>
<p align="center">
<strong>First MCP Server for NVIDIA NIM FLUX</strong>
</p>
<p align="center">
Generate and edit images using FLUX.1 models with your existing NVIDIA API key.
<br />
No extra subscriptions. No separate API keys. Just NIM.
</p>

<p align="center">
<a href="https://www.npmjs.com/package/nimgen"><img src="https://img.shields.io/npm/v/nimgen.svg?color=blue&label=npm" alt="npm version"></a>
<a href="https://github.com/gabriel-ferraresi/NIMGEN/blob/main/LICENSE"><img src="https://img.shields.io/badge/License-Apache%202.0-blue.svg" alt="License"></a>
<a href="https://build.nvidia.com"><img src="https://img.shields.io/badge/Powered%20by-NVIDIA%20NIM-76B900?logo=nvidia" alt="NVIDIA NIM"></a>
</p>

<p align="center">
<a href="#why-nimgen">Why NIMGEN?</a> •
<a href="#quick-start">Quick Start</a> •
<a href="#glossary">Glossary</a> •
<a href="#tools">Tools</a> •
<a href="#models">Models</a> •
<a href="#configuration">Configuration</a> •
<a href="#faq">FAQ</a>
</p>

---

## Why NIMGEN?

**NIMGEN is the first MCP server specifically built for NVIDIA NIM FLUX models.**

Most image generation MCP servers require separate API keys from providers like Replicate, Stability AI, or OpenAI. **NIMGEN uses your existing NVIDIA API key** — the same one you already use for LLM inference via NIM.

| Feature | NIMGEN | Other MCPs |
|---------|--------|------------|
| Uses existing NVIDIA key | ✅ | ❌ |
| No extra subscription | ✅ | ❌ |
| FLUX.1 models via NIM | ✅ | Some (via Replicate) |
| Image editing (Kontext) | ✅ | Rare |
| Free NIM credits (1000+) | ✅ | Varies |
| Self-hosted option | ✅ | Limited |

---

## Quick Start

### 1. Get your NVIDIA API Key

If you don't have one already:

1. Go to [build.nvidia.com](https://build.nvidia.com)
2. Sign in or create a free account
3. Navigate to **API Keys** section
4. Click **Generate Key**
5. Copy your key (starts with `nvapi-...`)

**Free tier includes 1,000+ credits** for testing!

### 2. Set the environment variable

```bash
# Windows (PowerShell)
$env:NVIDIA_API_KEY = "nvapi-your-key-here"

# Linux / macOS
export NVIDIA_API_KEY="nvapi-your-key-here"

# Verify it's set (optional)
echo $env:NVIDIA_API_KEY  # Windows
echo $NVIDIA_API_KEY      # Linux/macOS
```

### 3. Add to your MCP client

#### OpenCode / Oh-My-OpenCode

Add to your `opencode.jsonc`:

```jsonc
{
  "mcp": {
    "nimgen": {
      "type": "local",
      "command": ["npx", "-y", "nimgen"],
      "environment": {
        "NVIDIA_API_KEY": "{env:NVIDIA_API_KEY}"
      },
      "enabled": true,
      "timeout": 60000
    }
  }
}
```

#### Claude Desktop

Add to `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "nimgen": {
      "command": "npx",
      "args": ["-y", "nimgen"],
      "env": {
        "NVIDIA_API_KEY": "nvapi-your-key-here"
      }
    }
  }
}
```

#### Cursor / VS Code

Add to `.cursor/mcp.json` or `.vscode/mcp.json`:

```json
{
  "servers": {
    "nimgen": {
      "command": "npx",
      "args": ["-y", "nimgen"],
      "env": {
        "NVIDIA_API_KEY": "nvapi-your-key-here"
      }
    }
  }
}
```

---

## Glossary

New to AI image generation or MCP? Here's what the terms mean:

| Term | Definition |
|------|------------|
| **MCP** | Model Context Protocol — a standard for connecting AI assistants to external tools and data sources |
| **NIM** | NVIDIA Inference Microservices — NVIDIA's API platform for running AI models in the cloud |
| **FLUX.1** | A family of state-of-the-art image generation models by Black Forest Labs |
| **FLUX.1 Dev** | High-quality model for detailed, artistic images (slower, better quality) |
| **FLUX.1 Schnell** | Fast model for quick prototyping (4 steps, optimized for speed) |
| **FLUX.1 Kontext** | Image-to-image model for editing existing images with text prompts |
| **cfg_scale** | Classifier-Free Guidance Scale — controls how closely the AI follows your prompt (1-20). Higher = more faithful, lower = more creative. Default: 5 |
| **steps** | Number of inference iterations. More steps = better quality but slower. FLUX.1 Dev: 20-50, Schnell: 4 |
| **seed** | A number that controls randomness. Same seed + same prompt = same image every time. Use 0 for random |
| **negative_prompt** | Things to exclude from the image (e.g., "blurry, low quality, watermark") |

---

## Tools

### `generate_image`

Generate an image from a text description using NVIDIA NIM FLUX models.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Text description of the image (max 2000 chars) |
| `model` | string | — | `flux-1-dev` | Model: `flux-1-dev` or `flux-1-schnell` |
| `steps` | number | — | auto | Inference steps (more = better quality) |
| `cfg_scale` | number | — | `5` | Prompt adherence (1-20) |
| `negative_prompt` | string | — | — | Things to exclude |
| `seed` | number | — | `0` | Seed for reproducibility |

### `edit_image`

Edit an existing image using text instructions (FLUX.1-Kontext).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `prompt` | string | ✅ | — | Edit instructions |
| `image_path` | string | ✅ | — | Path to source image (PNG, JPEG, WebP, GIF) |
| `steps` | number | — | `20` | Inference steps (1-30) |
| `cfg_scale` | number | — | `7` | Prompt adherence (1-20) |
| `seed` | number | — | `0` | Seed for reproducibility |

**Note:** `image_path` must be within the output directory or current working directory for security.

### `list_models`

List all available FLUX models on NVIDIA NIM and their capabilities.

---

## Models

| Model | Key | Type | Speed | Quality | Best For |
|-------|-----|------|-------|---------|----------|
| **FLUX.1 Dev** | `flux-1-dev` | Text → Image | Medium | ⭐⭐⭐⭐⭐ | Final art, production assets |
| **FLUX.1 Schnell** | `flux-1-schnell` | Text → Image | Fast | ⭐⭐⭐ | Prototyping, quick drafts |
| **FLUX.1 Kontext** | `flux-1-kontext` | Image → Image | Medium | ⭐⭐⭐⭐ | Photo editing, mockups |

---

## Configuration

All configuration is via environment variables:

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `NVIDIA_API_KEY` | ✅ | — | Your NVIDIA API key (`nvapi-...`) |
| `NIMGEN_OUTPUT_DIR` | — | `./nimgen-output` | Directory to save generated images |
| `NIMGEN_BASE_URL` | — | `https://ai.api.nvidia.com/v1/genai` | Custom NIM endpoint |

### Self-Hosted NIM

If you're running NIM locally with Docker, set the base URL:

```bash
export NIMGEN_BASE_URL="http://localhost:8000/v1"
```

---

## Limitations

| Limit | Value | Notes |
|-------|-------|-------|
| Max prompt length | 2,000 characters | Longer prompts are rejected |
| Max image size | 50 MB | For input images in edit_image |
| Supported formats | PNG, JPEG, WebP, GIF | Both input and output |
| Max steps (Dev) | 50 | Higher doesn't always mean better |
| Max steps (Schnell) | 4 | Model is optimized for 4 steps |
| Max steps (Kontext) | 30 | For image editing |

### Rate Limits

NVIDIA NIM has rate limits based on your account tier:
- **Free tier**: ~1,000 credits (varies)
- **Paid tier**: Higher limits

When you hit rate limits, you'll see: `"Rate limit exceeded. Please wait a moment and try again."`

---

## Examples

### Social Media Post

```
Generate an image: Professional tech company social media banner
with gradient background from dark blue to purple, abstract
geometric shapes, and clean modern aesthetic.
```

### Product Mockup

```
Edit this image: Add a holographic logo floating above
the laptop screen with volumetric lighting and lens flare.
```

### Tattoo Preview

```
Edit this image: Add a realistic Japanese dragon tattoo
covering the forearm, black and gray style with fine
line work, photorealistic skin texture.
```

### Website Hero Image

```
Generate an image: Futuristic data center with rows of
glowing server racks, blue and green LED lighting,
cinematic perspective.
```

---

## FAQ

### General

**Q: What is NIMGEN?**
A: NIMGEN is an MCP (Model Context Protocol) server that lets you generate and edit images using NVIDIA's FLUX.1 models through your existing NVIDIA API key.

**Q: Do I need a separate subscription?**
A: No! NIMGEN uses your existing NVIDIA NIM API key. If you already use NVIDIA for LLM inference, you're all set.

**Q: Is it free?**
A: NVIDIA offers free credits (1,000+) when you sign up. After that, you pay per image generated through NVIDIA's pricing.

**Q: Which model should I use?**
A: Use `flux-1-dev` for high-quality final images, `flux-1-schnell` for quick prototypes, and `flux-1-kontext` for editing existing images.

### Troubleshooting

**Q: I get "NVIDIA_API_KEY environment variable is required"**
A: Make sure you've set the environment variable:
- Windows: `$env:NVIDIA_API_KEY = "nvapi-your-key"`
- Linux/macOS: `export NVIDIA_API_KEY="nvapi-your-key"`

**Q: I get "Invalid NVIDIA API key"**
A: Your key might be incorrect or expired. Get a new key at [build.nvidia.com](https://build.nvidia.com). Make sure it starts with `nvapi-`.

**Q: I get "Rate limit exceeded"**
A: You've hit NVIDIA's API limits. Wait a few seconds and try again. Consider upgrading your NVIDIA account for higher limits.

**Q: I get "Access denied: path outside allowed directories"**
A: For security, `edit_image` only accepts images from the output directory or current working directory. Move your image there first.

**Q: I get "Invalid image format"**
A: NIMGEN supports PNG, JPEG, WebP, and GIF. Make sure your image is in one of these formats.

**Q: I get "Image too large"**
A: Maximum image size is 50MB. Compress your image or use a smaller file.

**Q: I get "Prompt too long"**
A: Maximum prompt length is 2,000 characters. Shorten your prompt.

**Q: Generation is slow**
A: FLUX.1 Dev takes 20-50 steps and can take 30-60 seconds. Use `flux-1-schnell` for faster generation (4 steps, ~5-10 seconds).

**Q: I get "NVIDIA NIM service temporarily unavailable"**
A: NVIDIA's servers are experiencing issues. Wait a few minutes and try again.

### Technical

**Q: What Node.js version do I need?**
A: Node.js 18.0.0 or higher is required.

**Q: Can I use NIMGEN with self-hosted NIM?**
A: Yes! Set `NIMGEN_BASE_URL` to your local NIM endpoint:
```bash
export NIMGEN_BASE_URL="http://localhost:8000/v1"
```

**Q: Where are images saved?**
A: By default, images are saved to `./nimgen-output/`. Change with `NIMGEN_OUTPUT_DIR`.

**Q: Can I generate multiple images at once?**
A: Currently, NIMGEN generates one image per call. Batch generation is on the roadmap.

---

## Troubleshooting

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `NVIDIA_API_KEY is required` | Environment variable not set | Set `NVIDIA_API_KEY` with your key |
| `Invalid NVIDIA API key` | Wrong or expired key | Get a new key at build.nvidia.com |
| `Rate limit exceeded` | Too many requests | Wait a moment and retry |
| `Access denied: path outside allowed directories` | Image outside allowed dirs | Move image to output dir or cwd |
| `Invalid image format` | Unsupported file type | Use PNG, JPEG, WebP, or GIF |
| `Image too large` | File exceeds 50MB | Compress or use smaller file |
| `Prompt too long` | Exceeds 2000 chars | Shorten your prompt |
| `Service temporarily unavailable` | NVIDIA servers down | Wait and retry |

### Debug Mode

To see more details about what's happening:

```bash
# Run directly to see startup logs
NVIDIA_API_KEY=nvapi-... npx nimgen
```

---

## Development

```bash
# Clone and install
git clone https://github.com/gabriel-ferraresi/NIMGEN.git
cd NIMGEN
npm install

# Build
npm run build

# Run locally
NVIDIA_API_KEY=nvapi-... node dist/index.js
```

---

## License

Apache-2.0 — see [LICENSE](LICENSE) for details.

---

<p align="center">
Built with 💚 by <a href="https://www.tech86.com.br">Gabriel Ferraresi</a>
<br />
Powered by <a href="https://build.nvidia.com">NVIDIA NIM</a> + <a href="https://modelcontextprotocol.io">Model Context Protocol</a>
</p>
