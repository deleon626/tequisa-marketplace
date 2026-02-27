# Skill Lifecycle

How Claude discovers, activates, and executes skills.

## Overview

Skills are **model-invoked**: Claude decides which skills to use based on your request. You don't explicitly call them—Claude automatically applies relevant skills when your request matches their description.

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  Discovery  │ -> │  Activation │ -> │  Execution  │
│  (startup)  │    │  (matching) │    │  (running)  │
└─────────────┘    └─────────────┘    └─────────────┘
```

## Discovery Phase

**When:** At conversation startup

**What happens:**
- Claude scans all skill locations (enterprise, personal, project, plugin)
- Only **name** and **description** metadata is loaded
- Full SKILL.md body is NOT loaded yet
- ~100 tokens per skill for discovery overhead

**Why it matters:**
- Keeps startup fast even with many skills
- Your description must contain enough context for matching
- "When to use" information belongs in description, not body

## Activation Phase

**When:** Your request matches a skill's description

**What happens:**
1. Claude analyzes your request
2. Semantic matching against all skill descriptions
3. Best-match skill(s) identified
4. **Confirmation prompt** shown to you
5. Full SKILL.md body loaded into context (~5k words max)

**Matching behavior:**
- Uses semantic similarity, not exact keyword matching
- Multiple skills can match; Claude selects most relevant
- Vague descriptions reduce match accuracy

**Example flow:**
```
Request: "Review this PR for security issues"
    ↓
Match: description contains "security review", "PR review"
    ↓
Prompt: "Use security-review skill?"
    ↓
Load: Full SKILL.md body enters context
```

## Execution Phase

**When:** After activation confirmation

**What happens:**
1. Claude follows instructions in SKILL.md body
2. Referenced files loaded **on demand** (progressive disclosure)
3. Bundled scripts executed **without loading into context**
4. Task completed according to skill guidance

**Resource loading:**
- Reference files: Loaded when Claude determines they're needed
- Scripts: Executed, only output enters context
- Assets: Used for output, never loaded into context

## Flow Diagram

```
┌──────────────────────────────────────────────────────────┐
│                     USER REQUEST                          │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ DISCOVERY: Scan skill metadata (name + description only) │
│ Cost: ~100 tokens per skill                              │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ MATCHING: Semantic comparison against descriptions       │
│ Result: Best-match skill(s) identified                   │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ CONFIRMATION: "Use [skill-name]?" prompt                 │
│ User approves or declines                                │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ ACTIVATION: Full SKILL.md body loaded into context       │
│ Cost: Variable, aim for <500 lines                       │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│ EXECUTION: Follow instructions, load resources as needed │
│ Scripts: Run without loading source into context         │
│ References: Load only when Claude needs them             │
└──────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────┐
│                      RESPONSE                             │
└──────────────────────────────────────────────────────────┘
```

## Implications for Skill Authors

### 1. Description is Critical

The description is the **only thing Claude sees** during discovery. Include:
- What the skill does (specific capabilities)
- When to use it (trigger terms users would say)

### 2. Body Loads On-Demand

Don't put "when to use" in the body—it won't help with activation. The body should contain:
- Step-by-step instructions
- Best practices and patterns
- Links to reference files

### 3. Resources Are Lazy-Loaded

Claude decides when to load reference files. Structure your SKILL.md with clear navigation:
```markdown
For detailed API patterns, see references/api-patterns.md
```

### 4. Scripts Run Without Context Cost

Scripts execute and only their **output** enters context. Use scripts for:
- Complex validation logic
- Data processing
- Consistent, repeatable operations

### 5. Keep Context Lean

Context is shared across the conversation. Minimize footprint:
- SKILL.md under 500 lines
- Reference files for detailed content
- Scripts for code-heavy operations
