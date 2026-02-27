# Troubleshooting Skills

Common problems and solutions when working with skills.

## Skill Not Triggering

### Symptom
Skill exists but Claude doesn't use it for relevant requests.

### Cause: Vague Description

The description field is how Claude decides whether to use your skill.

**Bad** (vague, no triggers):
```yaml
description: Helps with documents.
```

**Good** (specific capabilities + trigger terms):
```yaml
description: Extract text and tables from PDF files, fill forms, merge documents. Use when working with PDF files or when user mentions PDFs, forms, document extraction.
```

### Cause: Trigger Info in Body

The body only loads **after** activation. Move "when to use" info to the description.

**Wrong:**
```yaml
---
name: pdf-helper
description: PDF processing skill.
---

Use this skill when working with PDFs...  # Too late!
```

**Right:**
```yaml
---
name: pdf-helper
description: PDF processing skill. Use when working with PDFs, extracting text, or filling forms.
---
```

### Solution

Rewrite your description to answer:
1. What does this skill do? (specific capabilities)
2. When should Claude use it? (trigger keywords)

## Skill Doesn't Load

### Check File Path

Skills must be at the correct path with exact filename `SKILL.md` (case-sensitive):

| Type | Correct Path |
|------|-------------|
| Personal | `~/.claude/skills/my-skill/SKILL.md` |
| Project | `.claude/skills/my-skill/SKILL.md` |
| Plugin | `my-plugin/skills/my-skill/SKILL.md` |

### Check YAML Syntax

Common YAML issues:

**Blank line before frontmatter:**
```yaml

---           # Wrong: blank line above
name: my-skill
---
```

**Tabs instead of spaces:**
```yaml
---
name: my-skill
	description: Uses tab    # Wrong: tab character
---
```

**Missing closing delimiter:**
```yaml
---
name: my-skill
description: Something
# Missing closing ---
```

### Debug Mode

Run Claude Code with debug flag to see skill loading errors:

```bash
claude --debug
```

## Skill Has Errors

### Dependencies Not Installed

If your skill uses external packages, they must be installed in your environment before Claude can use them.

**Document dependencies in SKILL.md:**
```markdown
## Requirements

Install required packages:
pip install pypdf pdfplumber
```

### Script Permissions

Scripts need execute permissions:

```bash
chmod +x scripts/*.py
chmod +x scripts/*.sh
```

### File Path Issues

Always use forward slashes, even on Windows:

```markdown
# Correct
See references/api-docs.md
Run scripts/validate.py

# Wrong
See references\api-docs.md
Run scripts\validate.py
```

## Multiple Skills Conflict

### Symptom
Claude uses the wrong skill or seems confused between similar skills.

### Cause
Descriptions are too similar.

### Solution
Make descriptions distinct with specific trigger terms:

**Instead of both having "data analysis":**
- Skill A: `"Analyze sales data in Excel files and CRM exports"`
- Skill B: `"Analyze log files and system metrics"`

The more specific your trigger terms, the easier it is for Claude to match correctly.

## Plugin Skills Not Appearing

### Clear Cache and Reinstall

```bash
rm -rf ~/.claude/plugins/cache
```

Then restart Claude Code and reinstall the plugin:

```bash
/plugin install plugin-name@marketplace-name
```

### Verify Plugin Structure

Skills must be in a `skills/` directory at the plugin root:

```
my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

## Skills with Subagents

### Symptom
Subagent doesn't have access to your skills.

### Cause
Skills don't automatically inherit to subagents.

### Solution
Explicitly list skills in AGENT.md:

```yaml
# .claude/agents/code-reviewer/AGENT.md
---
name: code-reviewer
description: Review code for quality
skills: pr-review, security-check
---
```

**Note:** Built-in agents (Explore, Plan, Verify) and the Task tool do not have access to your skills. Only custom subagents with explicit `skills` field can use them.

## Quick Diagnostic Checklist

Use this checklist when a skill isn't working:

- [ ] **Path correct?** SKILL.md at right location
- [ ] **YAML valid?** No tabs, starts line 1, proper delimiters
- [ ] **Description specific?** Includes trigger terms
- [ ] **Dependencies installed?** Required packages available
- [ ] **Permissions set?** Scripts are executable
- [ ] **Paths use forward slashes?** Even on Windows
- [ ] **Restart Claude Code?** After creating/editing skills
- [ ] **Debug mode?** Run `claude --debug` for errors

## Getting Help

If none of the above solutions work:

1. Check the [official docs](https://code.claude.com/docs/en/skills.md)
2. Run `claude --debug` and check for specific errors
3. Verify with "What skills are available?" to confirm loading
4. Test with a minimal skill to isolate the issue
