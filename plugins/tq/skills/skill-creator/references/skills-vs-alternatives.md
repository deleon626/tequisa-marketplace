# Skills vs Alternatives

When to use skills versus other Claude Code customization options.

## Quick Decision Table

| Use this | When you want to... | Triggering |
|----------|---------------------|------------|
| **Skills** | Give Claude specialized knowledge | Claude chooses automatically |
| **Slash commands** | Create reusable prompts | You type `/command` |
| **CLAUDE.md** | Set project-wide instructions | Always loaded |
| **Subagents** | Delegate with isolated context | Claude delegates or explicit |
| **Hooks** | Run scripts on events | Fires on tool events |
| **MCP servers** | Connect to external tools/data | Claude calls as needed |

## Detailed Comparisons

### Skills vs Slash Commands

| Aspect | Skills | Slash Commands |
|--------|--------|----------------|
| Activation | Automatic (Claude decides) | Manual (`/command`) |
| Context | Knowledge and workflows | Reusable prompts |
| Best for | Domain expertise, standards | Specific actions, shortcuts |

**Use Skills when:**
- Claude should automatically apply knowledge
- The guidance fits many situations
- You want "always available" expertise

**Use Slash Commands when:**
- You want explicit control over when it runs
- It's a specific action (deploy, commit, lint)
- You want a keyboard shortcut for a prompt

**Example:**
- **Skill**: "Code review standards" - Claude applies when reviewing any code
- **Command**: `/deploy staging` - You explicitly trigger deployment

### Skills vs CLAUDE.md

| Aspect | Skills | CLAUDE.md |
|--------|--------|-----------|
| Loading | On-demand (when matched) | Always loaded |
| Scope | Domain-specific | Project-wide |
| Size | Can be larger (progressive disclosure) | Should be concise |

**Use Skills when:**
- Guidance is domain-specific (PDFs, APIs, etc.)
- You have detailed workflows or references
- Loading everything would waste context

**Use CLAUDE.md when:**
- Rules apply to ALL interactions
- It's project configuration (build commands, style)
- It should never be skipped

**Example:**
- **Skill**: "PDF extraction workflow" - only needed for PDF tasks
- **CLAUDE.md**: "Use TypeScript strict mode" - applies to all code

### Skills vs Subagents

| Aspect | Skills | Subagents |
|--------|--------|-----------|
| Context | Same conversation | Separate context |
| Tools | Same tools | Can have different tools |
| Purpose | Add knowledge | Delegate tasks |

**Use Skills when:**
- Adding expertise to current conversation
- No need for isolated execution
- You want guidance, not delegation

**Use Subagents when:**
- Task needs isolation (separate context)
- Different tool access required
- Complex delegation with specific outcomes

**Example:**
- **Skill**: "Security review guidelines" - informs Claude's analysis
- **Subagent**: "Security scanner" - runs isolated security checks

### Skills vs MCP Servers

| Aspect | Skills | MCP Servers |
|--------|--------|-------------|
| Purpose | Teach HOW to use tools | PROVIDE the tools |
| Content | Knowledge, workflows | Tool implementations |
| Integration | Markdown instructions | API connections |

**Use Skills when:**
- Claude needs domain knowledge
- You're teaching patterns or workflows
- The tools already exist

**Use MCP when:**
- You need to connect external systems
- Providing new capabilities (database, API)
- Claude needs to call external services

**Example:**
- **MCP**: Connects Claude to your database
- **Skill**: Teaches Claude your data model and query patterns

### Skills vs Hooks

| Aspect | Skills | Hooks |
|--------|--------|-------|
| Triggering | Request matching | Tool events |
| Execution | Claude follows guidance | Scripts run automatically |
| Purpose | Knowledge application | Automation |

**Use Skills when:**
- Claude should apply knowledge
- Guidance involves judgment
- Output varies by situation

**Use Hooks when:**
- Action should ALWAYS happen
- No judgment needed (lint, format)
- You want guaranteed execution

**Example:**
- **Skill**: "Commit message standards" - Claude crafts message
- **Hook**: "Run linter on file save" - automatic, no judgment

## Decision Flowchart

```
Need to customize Claude's behavior?
│
├─ Should it ALWAYS apply to every interaction?
│   └─ Yes → CLAUDE.md
│
├─ Do you need to connect external tools/data?
│   └─ Yes → MCP Server
│
├─ Should a script run automatically on events?
│   └─ Yes → Hook
│
├─ Do you want explicit control over when it runs?
│   └─ Yes → Slash Command
│
├─ Does the task need isolated context?
│   └─ Yes → Subagent
│
└─ Should Claude automatically apply domain knowledge?
    └─ Yes → Skill
```

## Combination Patterns

These customizations work together:

### Skill + MCP
- **MCP**: Provides database connection
- **Skill**: Teaches query patterns and data model

### Skill + Slash Command
- **Skill**: Contains review standards (auto-applied)
- **Command**: `/review detailed` for extra-thorough review

### Skill + Subagent
- **Skill**: Defines review criteria
- **Subagent**: Runs isolated review with skill loaded

### Hook + Skill
- **Hook**: Runs linter on save
- **Skill**: Guides Claude on fixing lint errors

## Summary

| Choose | When |
|--------|------|
| **Skills** | Domain knowledge Claude applies automatically |
| **Slash commands** | Actions you explicitly trigger |
| **CLAUDE.md** | Universal project rules |
| **Subagents** | Isolated task delegation |
| **Hooks** | Automatic event-driven scripts |
| **MCP** | External tool/data connections |
