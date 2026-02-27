# Metadata Reference

Complete YAML frontmatter field reference for SKILL.md files.

## Required Fields

| Field | Description | Constraints |
|-------|-------------|-------------|
| `name` | Skill identifier | Lowercase, numbers, hyphens only; max 64 chars; must match directory name |
| `description` | What skill does and when to use | Max 1024 chars; used for activation matching |

### name

The unique identifier for your skill. Must follow these rules:
- Lowercase letters, numbers, and hyphens only
- No consecutive hyphens (`my--skill` is invalid)
- No leading/trailing hyphens (`-my-skill` is invalid)
- Maximum 64 characters
- Should match the skill directory name

```yaml
name: pdf-processor      # Valid
name: PDF-Processor      # Invalid (uppercase)
name: pdf_processor      # Invalid (underscore)
```

### description

Critical for skill activation. Claude uses this to decide when to apply your skill.

**Good description** (specific, includes trigger terms):
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, document extraction.
```

**Bad description** (vague, no triggers):
```yaml
description: Helps with documents.
```

## Optional Fields

| Field | Description | Example |
|-------|-------------|---------|
| `allowed-tools` | Tools Claude can use without permission | `Read, Grep, Glob` |
| `model` | Override model for this skill | `claude-sonnet-4-20250514` |

### allowed-tools

Restricts Claude to specific tools when this skill is active. If omitted, Claude uses its standard permission model.

**Common patterns:**

```yaml
# Read-only skill
allowed-tools: Read, Grep, Glob

# Python execution only
allowed-tools: Read, Bash(python:*)

# Full access (omit field entirely)
# allowed-tools: [not specified]
```

**Use cases:**
- Security-sensitive workflows requiring restricted capabilities
- Read-only skills that shouldn't modify files
- Skills limited to specific operations (e.g., only data analysis)

### model

Override the conversation's default model for this skill.

```yaml
model: claude-sonnet-4-20250514
```

**When to use:**
- Skills requiring specific model capabilities
- Complex reasoning tasks needing stronger models
- Cost optimization with faster models for simple tasks

If omitted, defaults to the conversation's current model.

## Validation Rules

The YAML frontmatter must follow these rules:

1. **Start on line 1** - No blank lines before the opening `---`
2. **Proper delimiters** - Open with `---`, close with `---`
3. **Spaces for indentation** - Never use tabs
4. **Case-sensitive field names** - Use lowercase exactly as documented

**Valid frontmatter:**
```yaml
---
name: my-skill
description: Does something useful. Use when user asks about X.
allowed-tools: Read, Grep
---
```

**Invalid frontmatter:**
```yaml

---
Name: my-skill
description: Does something useful
---
```
(Has blank line before `---` and uppercase `Name`)

## Quick Reference

```yaml
---
# Required
name: skill-name-here
description: What it does. When to use it. Include trigger keywords.

# Optional
allowed-tools: Read, Grep, Glob, Bash(python:*)
model: claude-sonnet-4-20250514
---
```
