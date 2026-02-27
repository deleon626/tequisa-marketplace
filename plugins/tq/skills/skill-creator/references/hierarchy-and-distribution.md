# Skill Hierarchy and Distribution

Where skills live, precedence rules, and sharing options.

## Skill Locations

| Location | Path | Scope |
|----------|------|-------|
| Enterprise | Managed settings (platform-specific) | All users in organization |
| Personal | `~/.claude/skills/` | You, across all projects |
| Project | `.claude/skills/` | Anyone working in repository |
| Plugin | `skills/` in plugin directory | Anyone with plugin installed |

### Personal Skills

Store in your home directory. Available in every project you work on.

```
~/.claude/skills/
├── my-workflow/
│   └── SKILL.md
└── code-review/
    └── SKILL.md
```

### Project Skills

Store in repository root. Shared with anyone who clones the repo.

```
my-project/
└── .claude/
    └── skills/
        └── team-standards/
            └── SKILL.md
```

### Plugin Skills

Bundled inside a plugin. Distributed via plugin marketplace.

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── bundled-skill/
        └── SKILL.md
```

## Precedence Rules

When multiple skills share the same name, higher locations win:

```
Enterprise (highest priority)
    ↓
Personal
    ↓
Project
    ↓
Plugin (lowest priority)
```

**Example:**

If both exist:
- `~/.claude/skills/code-review/SKILL.md` (personal)
- `.claude/skills/code-review/SKILL.md` (project)

The **personal** version is used because personal > project.

### Use Cases for Precedence

1. **Personal override**: Your personal preferences over team defaults
2. **Enterprise enforcement**: Org-wide standards override individual settings
3. **Plugin customization**: Override bundled plugin behavior with project-specific version

## Distribution Options

### Project Distribution

Simplest approach. Commit skills to version control:

```bash
# Add project skills to git
git add .claude/skills/
git commit -m "Add team coding standards skill"
git push
```

Anyone who clones gets the skills automatically.

**Best for:**
- Team-specific workflows
- Repository-specific standards
- Shared team knowledge

### Plugin Distribution

Package skills for reuse across multiple projects:

1. Create plugin structure:
   ```
   my-plugin/
   ├── .claude-plugin/
   │   └── plugin.json
   └── skills/
       └── my-skill/
           └── SKILL.md
   ```

2. Add to plugin marketplace or distribute directly

3. Users install:
   ```bash
   /plugin install my-plugin@marketplace-name
   ```

**Best for:**
- Reusable workflows
- Community sharing
- Framework-specific skills

### Enterprise Distribution

Administrators deploy skills organization-wide through managed settings.

**Best for:**
- Compliance requirements
- Org-wide standards
- Centralized governance

Contact your admin for enterprise skill deployment.

## Directory Structure Examples

### Personal Setup

```
~/.claude/
└── skills/
    ├── commit-helper/
    │   └── SKILL.md
    ├── code-review/
    │   ├── SKILL.md
    │   └── references/
    │       └── checklist.md
    └── api-design/
        ├── SKILL.md
        └── scripts/
            └── validate.py
```

### Project Setup

```
my-project/
├── .claude/
│   └── skills/
│       └── team-workflow/
│           ├── SKILL.md
│           └── references/
│               ├── style-guide.md
│               └── review-checklist.md
├── src/
└── README.md
```

### Plugin Setup

```
my-awesome-plugin/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── skill-one/
│   │   └── SKILL.md
│   └── skill-two/
│       ├── SKILL.md
│       └── scripts/
│           └── helper.py
└── README.md
```

## Best Practices

### Naming Conventions

- Use kebab-case for directories: `code-review`, `api-design`
- Keep names descriptive but concise
- Avoid conflicts with common names at higher precedence levels

### Version Control

- **Do commit**: Project skills (`.claude/skills/`)
- **Don't commit**: Personal skills (they're in home directory)
- **Consider**: `.gitignore` for local skill overrides

### Organization Tips

1. **Personal**: General-purpose skills you use everywhere
2. **Project**: Team-specific standards and workflows
3. **Plugin**: Reusable skills worth sharing with others
