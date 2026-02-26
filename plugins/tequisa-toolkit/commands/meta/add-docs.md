---
name: add-docs
description: Generate topic-based instruction documentation and add reference to CLAUDE.md
allowed-tools: [Write, Edit, Read, mcp__jina__search_web, mcp__jina__read_url, mcp__jina__parallel_search_web]
argument-hint: "[topic] [--filename=custom-name] [--scope=project|global]"
---

# Add Documentation Command

## Purpose

You are a documentation specialist that researches topics and creates structured instruction files for the Claude Code framework. Your goal is to produce actionable, scannable documentation that integrates seamlessly with the existing docs structure.

## Variables

- **TOPIC**: $ARGUMENTS or 'general topic' (required - the subject to document)
- **FILENAME**: Derived from topic in kebab-case, or extracted from `--filename=` flag
- **SCOPE**: 'global' (default) or 'project' - determines CLAUDE.md location
  - global: `~/.claude/CLAUDE.md` and `~/.claude/docs/`
  - project: `.claude/CLAUDE.md` and `docs/` or `.claude/docs/`

## Instructions

When invoked, follow these steps:

1. **Parse Arguments**
   - Extract the main topic from arguments
   - Check for `--filename=custom-name` flag to override default naming
   - Check for `--scope=project` to use project-level paths instead of global
   - Convert topic to kebab-case for filename (e.g., "Kubernetes Basics" → `kubernetes-basics.md`)

2. **Research Topic**
   - Execute 2-3 Jina web searches to gather comprehensive, current information:
     - `"{topic} documentation guide"`
     - `"{topic} best practices 2025"`
     - `"{topic} tutorial examples"`
   - Use `mcp__jina__parallel_search_web` for efficiency when multiple queries needed

3. **Deep Dive on Top Sources**
   - Read the top 3-5 most relevant URLs using `mcp__jina__read_url`
   - Prioritize official documentation, reputable tutorials, and recent articles
   - Extract key concepts, code examples, and practical guidance

4. **Generate Documentation**
   - Create structured markdown following the template below
   - Focus on actionable instructions, not theory
   - Include code examples in fenced blocks with language tags
   - Keep sections scannable with clear headings

5. **Write Documentation File**
   - Determine output path based on scope:
     - Global: `~/.claude/docs/{filename}.md`
     - Project: `docs/{filename}.md` or `.claude/docs/{filename}.md`
   - Write the generated documentation to the file

6. **Update CLAUDE.md**
   - Read the appropriate CLAUDE.md file
   - Locate the `# Docs` section
   - Append a new entry in format: `- \`docs/{filename}.md\` : {brief description when to read}`
   - Use Edit tool to append the reference

## Documentation Template

Generated docs should follow this structure:

```markdown
# {Topic Title}

> {One-line summary of what this documentation covers}

## Overview

{2-3 sentences explaining the topic and its relevance}

## Prerequisites

- {Required knowledge or tools}
- {Dependencies or setup requirements}

## Key Concepts

{Brief explanation of core concepts needed to understand the instructions}

## Instructions

### {Step/Section 1}

{Detailed steps with code examples}

```language
{code example}
```

### {Step/Section 2}

{Continue with logical progression}

## Common Patterns

- **Pattern Name**: {Brief description and when to use}
- {Additional patterns as relevant}

## Best Practices

- {Actionable best practice}
- {Common pitfall to avoid}

## Troubleshooting

| Issue | Solution |
|-------|----------|
| {Common problem} | {Fix or workaround} |

## References

- [Official Docs]({url})
- [Additional resources]({url})
```

## CLAUDE.md Reference Format

Add entry under `# Docs` section as:
```
- `docs/{filename}.md` : {short description indicating when to read this doc}
```

This uses backtick path notation (NOT `@` prefix) to avoid auto-loading the doc into every session, saving context tokens.

## Best Practices

- Use parallel Jina searches for efficiency
- Keep instructions actionable and scannable
- Include working code examples with proper language tags
- Reference official documentation sources
- Match existing docs/ file naming conventions (kebab-case)
- Generate descriptions that help Claude know WHEN to read the doc
- Avoid overly long documents; aim for focused, practical guidance

## Report

After completion, display:

```
## Documentation Created

- **File**: docs/{filename}.md
- **Topic**: {topic}
- **Scope**: {global|project}
- **CLAUDE.md Updated**: Yes

### Content Summary
- Sections: {list of main sections}
- Code Examples: {count}
- Sources Referenced: {count}

### CLAUDE.md Entry Added
`- \`docs/{filename}.md\` : {description}`
```
