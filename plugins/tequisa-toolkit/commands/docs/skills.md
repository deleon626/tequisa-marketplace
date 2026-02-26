---
description: "Load Claude Code Agent Skills documentation into context"
allowed-tools: ["mcp__jina__parallel_read_url", "mcp__jina__read_url"]
---

Use mcp__jina__parallel_read_url to fetch all URLs in a single call:

URLs to fetch:
- https://code.claude.com/docs/en/skills
- https://code.claude.com/docs/en/best-practices
- https://code.claude.com/docs/en/common-workflows
- https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills

Once loaded, respond: "Agent Skills documentation loaded into context."
