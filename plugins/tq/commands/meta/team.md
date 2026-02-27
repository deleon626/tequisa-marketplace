---
description: "Create and orchestrate Claude Code agent teams. Presets: research|dev|review|debug. Empty for interactive setup."
allowed-tools: ["AskUserQuestion", "TeamCreate", "TaskCreate", "TaskList", "TaskUpdate", "SendMessage", "Read", "Grep", "Glob", "mcp__jina__parallel_read_url", "mcp__jina__read_url"]
argument-hint: "[preset: research|dev|review|debug]"
---

# Agent Team Orchestration Command

## Purpose

You are an agent team architect. Help users create effective agent teams by understanding their needs, recommending team structures, and guiding task decomposition for parallel execution.

## Variables

- **PRESET**: $ARGUMENTS - Optional preset type (research|dev|review|debug)
- **TEAM_NAME**: Derived from project or user input
- **TEAM_SIZE**: Recommended 3-6 teammates based on task complexity

## When to Use Agent Teams

Teams excel at:
- **Parallel exploration**: Multiple teammates investigating different angles
- **Cross-layer work**: Frontend, backend, tests each owned independently
- **Code review**: Security, performance, architecture reviewers simultaneously
- **Competing hypotheses**: Multiple theories tested in parallel for debugging

**Don't use for**: Sequential tasks, same-file edits, simple linear workflows.

---

## Instructions

### Phase 0: Load Documentation Context

Before any other work, load relevant reference documentation into context.

Use `mcp__jina__parallel_read_url` to fetch:
- `https://code.claude.com/docs/en/agent-teams`
- `https://code.claude.com/docs/en/sub-agents`
- `https://code.claude.com/docs/en/best-practices`
- `https://platform.claude.com/docs/en/agent-sdk/overview`
- `https://code.claude.com/docs/en/features-overview`

This ensures you have up-to-date Claude Code documentation for orchestrating accurate agent teams.

### Phase 1: Route by Argument

- If $ARGUMENTS contains "research", "dev", "review", or "debug" → Jump to Phase 4 (Preset)
- If $ARGUMENTS is empty → Continue to Phase 2 (Interactive)

### Phase 2: Interactive Team Building

Use AskUserQuestion across 2-3 rounds:

#### Round 1: Project Context

Questions:
1. **"What is the main task or project goal?"** (header: "Goal", options: free text)
2. **"What type of work is this?"** (header: "Type", options: "Research and exploration", "Code review and analysis", "Feature implementation", "Debugging and investigation")
3. **"Can this work be split into independent parallel tracks?"** (header: "Parallel", options: "Yes - clear independent modules", "Partially - some dependencies", "Unsure - need help decomposing", "No - mostly sequential")

If "No - mostly sequential": explain agent teams may not be ideal, suggest subagents instead. Ask if they want to continue.

#### Round 2: Team Composition

1. **"How many teammates?"** (header: "Size", options: "2", "3", "4", "5-6", "Let Claude decide")
2. **"What specialist types?"** (header: "Roles", multiSelect: true, options: "Frontend specialist", "Backend specialist", "Testing specialist", "Security reviewer", "Research investigator")
3. **"Should teammates require plan approval before implementing?"** (header: "Approval", options: "Yes - review plans first", "No - implement directly", "Only for high-risk changes")

#### Round 3: Task Strategy (if needed)

Only if user selected "Unsure" in Round 1:
1. **"How should work be divided?"** (header: "Division")
2. **"Are there task dependencies?"** (header: "Deps")
3. **"How will you know the team succeeded?"** (header: "Success")

### Phase 3: Generate Team Plan

Present structured plan:

```
## Agent Team Plan

**Task**: [from Round 1]
**Team Size**: [from Round 2]

### Team Composition
1. **[Role]** - Focus: [responsibilities], Model: [Sonnet/Opus]
2. **[Role]** - Focus: [responsibilities], Model: [Sonnet/Opus]
[...]

### Task Breakdown
1. **Task 1**: [Description] → Owner: [Teammate], Dependencies: [None/list]
2. **Task 2**: [Description] → Owner: [Teammate], Dependencies: [None/list]
[...]

### Success Criteria
[Clear, measurable outcomes]
```

Ask: **"Does this team structure work? (yes/no/modify)"**

### Phase 4: Preset Execution

#### `research` - Research Team
Spawn 3-4 teammates:
- **Deep-dive researcher**: Official docs and primary sources
- **Alternative approaches**: Competing solutions and tradeoffs
- **Implementation researcher**: Real-world examples and code patterns
- **Synthesis specialist**: Combine findings into recommendations

All Sonnet. No plan approval (read-only).

#### `dev` - Development Team
Spawn 3 teammates:
- **Frontend developer**: UI components (requires plan approval)
- **Backend developer**: API and business logic (requires plan approval)
- **Testing specialist**: Unit and integration tests

Workflow: Plan → Lead approval → Implement → Test → Synthesize.

#### `review` - Code Review Team
Spawn 4 reviewers:
- **Security reviewer**: Vulnerabilities, input validation, auth
- **Performance reviewer**: Inefficiencies, N+1 queries, memory leaks
- **Architecture reviewer**: Design patterns, coupling, maintainability
- **Test coverage reviewer**: Test existence and edge case coverage

All Sonnet. Read-only tools only.

#### `debug` - Debug Team
Spawn 4-5 investigators:
- **Hypothesis 1-4**: Each investigator explores a different theory
- **Synthesis specialist**: Evaluate evidence and determine root cause

Opus for synthesis, Sonnet for investigators.

### Phase 5: Execute

1. **Create the Team** via TeamCreate
2. **Create Initial Tasks** via TaskCreate based on the plan
3. **Spawn Teammates** via Task tool with appropriate subagent_type and team_name
4. **Monitor Progress** and coordinate via SendMessage

---

## Best Practices to Share

### File Ownership
- Each teammate should own different files
- Two teammates editing the same file = overwrites and conflicts

### Context Loading
- Teammates get CLAUDE.md, MCP servers, and skills automatically
- They DON'T inherit lead's conversation history
- Include task-specific details in spawn prompts

### Controls
- **View teammate**: Shift+Up/Down to select
- **Toggle task list**: Ctrl+T
- **Delegate mode**: Shift+Tab (lead only coordinates)

### Cost Note
Each teammate is a separate Claude instance. Token usage scales linearly with team size.

---

## Output Format

After team setup, display:

```
## Agent Team Created

**Team**: [name] | **Size**: [X teammates]

### Teammates
1. **[Name]** - [Role] - [Status]
2. **[Name]** - [Role] - [Status]

### Tasks
- [ ] Task 1 → [Teammate]
- [ ] Task 2 → [Teammate]

### Controls
- Shift+Up/Down: Select teammate
- Ctrl+T: Toggle task list
- Shift+Tab: Delegate mode
```
