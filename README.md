# tequisa-marketplace

Claude Code plugin marketplace by Denny Leonardo.

## Available Plugins

| Plugin | Description |
|--------|-------------|
| tq | Docs loaders, meta-generators, Jina research, cargo quoting, AI image gen |

## Structure

```
tequisa-marketplace/
├── .claude-plugin/
│   └── marketplace.json
├── plugins/
│   └── tq/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── commands/
│       ├── skills/
│       └── README.md
└── README.md
```

## Installation

```bash
# 1. Add this marketplace (one-time)
/plugin marketplace add deleon626/tequisa-marketplace

# 2. Install a plugin
/plugin install tq@tequisa-marketplace --scope user
```

Or use `/plugin` → Discover tab to browse and install interactively.
