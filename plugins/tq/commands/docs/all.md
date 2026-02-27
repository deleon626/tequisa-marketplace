---
description: "Load or search Claude documentation. No args = load all, with keyword = search & filter"
allowed-tools: ["mcp__jina__parallel_read_url", "mcp__jina__read_url"]
argument-hint: "[keyword]"
---

# Claude Documentation: Load or Search

## Step 1: Fetch Documentation Map

Use `mcp__jina__read_url` to fetch the official documentation map:
```
https://code.claude.com/docs/en/claude_code_docs_map.md
```

Alternative index: `https://code.claude.com/docs/llms.txt`

**If the documentation map fetch fails**, use the hardcoded fallback URLs in the Fallback section below.

---

## Step 2: Route by Arguments

### If NO keyword provided (`$ARGUMENTS` is empty):

**Load all documentation.**

Extract ALL URLs from the documentation map. Use `mcp__jina__parallel_read_url` to fetch them all (batch in groups of 5 if needed).

Once loaded, respond: "All Claude documentation loaded into context."

### If keyword provided (`$ARGUMENTS` has a value):

**Search and filter documentation.**

Parse the markdown structure to extract document entries.
Filter entries where:
- Title contains the keyword (case-insensitive)
- Section name contains the keyword
- Description/content points contain the keyword

Score matches:
- Primary: Exact keyword in title (highest relevance)
- Secondary: Keyword in section headers
- Related: Keyword in description/content

**If no matches found**: Search for related terms or suggest browsing the full doc map.

Use `mcp__jina__parallel_read_url` to fetch the top 5-10 most relevant matched URLs.

**Generate formatted report:**

```markdown
# Claude Documentation: "$ARGUMENTS"

## Primary Documentation

### [Document Title](URL)
- Section: Section Name
- Direct Link: URL

#### Key Topics:
- Topic 1
- Topic 2

#### Content Excerpt:
> Relevant excerpt from document content...

## Related Topics
- [Related Document](URL) - Section Name
```

---

## Fallback URLs (if documentation map is unavailable)

### Commands & Extensibility
- https://code.claude.com/docs/en/slash-commands
- https://code.claude.com/docs/en/hooks-guide
- https://code.claude.com/docs/en/common-workflows
- https://code.claude.com/docs/en/plugins-reference
- https://code.claude.com/docs/en/mcp

### Agent SDK & Subagents
- https://platform.claude.com/docs/en/agent-sdk/overview
- https://platform.claude.com/docs/en/agent-sdk/python
- https://code.claude.com/docs/en/sub-agents
- https://code.claude.com/docs/en/best-practices
- https://github.com/anthropics/claude-agent-sdk-typescript

### Skills
- https://code.claude.com/docs/en/skills
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

### Prompt Engineering
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/overview
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/be-clear-and-direct
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/system-prompts
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/use-xml-tags
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/multishot-prompting
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/chain-of-thought
- https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/long-context-tips
- https://www.anthropic.com/engineering/claude-code-best-practices
