# tq

Claude Code plugin with documentation loaders, meta-generators, Jina research tools, cargo quoting, and AI image generation.

## Commands

### docs/
Load Claude documentation into context.

| Command | Description |
|---------|-------------|
| `/tq:docs:all` | Load or search all Claude docs |
| `/tq:docs:commands` | Commands & extensibility docs |
| `/tq:docs:skills` | Skills documentation |
| `/tq:docs:agents` | Agent SDK docs |
| `/tq:docs:teams` | Agent teams docs |
| `/tq:docs:hooks` | Hooks guide |
| `/tq:docs:prompt-engineering` | Prompt engineering docs |
| `/tq:docs:statusline` | Statusline configuration |

### meta/
Generate Claude Code configurations.

| Command | Description |
|---------|-------------|
| `/tq:meta:agent` | Create sub-agent configurations |
| `/tq:meta:command` | Create slash command configs |
| `/tq:meta:team` | Create and orchestrate agent teams |
| `/tq:meta:add-docs` | Generate topic documentation |

### jina/
Research with Jina AI.

| Command | Description |
|---------|-------------|
| `/tq:jina:research` | Comprehensive research with query expansion |
| `/tq:jina:arxiv-search` | Search arXiv papers |

## Skills

### cargo-quote
Generate cargo shipment quotes based on Tequisa's historical expedition data.

### image-gen
Generate and edit AI images using Gemini's Nano Banana and Imagen APIs. Requires `GEMINI_API_KEY` environment variable.

## Installation

```bash
# Via marketplace (recommended)
/plugin marketplace add deleon626/tequisa-marketplace
/plugin install tq@tequisa-marketplace --scope user

# Development/testing (single session)
claude --plugin-dir ~/Code/tequisa-marketplace/plugins/tq
```
