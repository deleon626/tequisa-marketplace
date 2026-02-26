# tequisa-toolkit

Claude Code plugin with documentation loaders, meta-generators, Jina research tools, cargo quoting, and AI image generation.

## Commands

### docs/
Load Claude documentation into context.

| Command | Description |
|---------|-------------|
| `/tequisa-toolkit:docs:all` | Load or search all Claude docs |
| `/tequisa-toolkit:docs:commands` | Commands & extensibility docs |
| `/tequisa-toolkit:docs:skills` | Skills documentation |
| `/tequisa-toolkit:docs:agents` | Agent SDK docs |
| `/tequisa-toolkit:docs:teams` | Agent teams docs |
| `/tequisa-toolkit:docs:hooks` | Hooks guide |
| `/tequisa-toolkit:docs:prompt-engineering` | Prompt engineering docs |
| `/tequisa-toolkit:docs:statusline` | Statusline configuration |

### meta/
Generate Claude Code configurations.

| Command | Description |
|---------|-------------|
| `/tequisa-toolkit:meta:agent` | Create sub-agent configurations |
| `/tequisa-toolkit:meta:command` | Create slash command configs |
| `/tequisa-toolkit:meta:team` | Create and orchestrate agent teams |
| `/tequisa-toolkit:meta:add-docs` | Generate topic documentation |

### jina/
Research with Jina AI.

| Command | Description |
|---------|-------------|
| `/tequisa-toolkit:jina:research` | Comprehensive research with query expansion |
| `/tequisa-toolkit:jina:arxiv-search` | Search arXiv papers |

## Skills

### cargo-quote
Generate cargo shipment quotes based on Tequisa's historical expedition data.

### image-gen
Generate and edit AI images using Gemini's Nano Banana and Imagen APIs. Requires `GEMINI_API_KEY` environment variable.

## Installation

```bash
# Via marketplace (recommended)
/plugin marketplace add deleon626/tequisa-marketplace
/plugin install tequisa-toolkit@tequisa-marketplace --scope user

# Development/testing (single session)
claude --plugin-dir ~/Code/tequisa-marketplace/plugins/tequisa-toolkit
```
