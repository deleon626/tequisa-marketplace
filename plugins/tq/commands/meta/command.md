---
name: meta-command-generator
description: Create slash command configuration files. Generates complete command definitions with proper structure and documentation. Use when: "create command", "new slash command", "build custom command"
allowed-tools: Write, Read, WebFetch, mcp__jina__parallel_read_url, mcp__jina__read_url
argument-hint: "[command-description]"
---

# Meta Command Generator

## Purpose

Expert slash-command architect that helps create properly structured Claude Code custom commands. Generates complete command definitions with clear instructions, best practices, and proper frontmatter formatting.

## Variables

- **COMMAND_DESCRIPTION**: $ARGUMENTS - Description of what the command does
- **COMMAND_NAME**: Derived from description (kebab-case)
- **OUTPUT_DIR**: `.claude/commands/` (project) or `~/.claude/commands/` (personal)

## Instructions

### Phase 0: Load Documentation Context

Before any other work, load relevant reference documentation into context.

Use `mcp__jina__parallel_read_url` to fetch:
- `https://code.claude.com/docs/en/skills`
- `https://code.claude.com/docs/en/hooks-guide`
- `https://code.claude.com/docs/en/common-workflows`
- `https://code.claude.com/docs/en/plugins-reference`
- `https://code.claude.com/docs/en/slash-commands`

This ensures you have up-to-date Claude Code documentation for generating accurate commands.

### Phase 1: Analyze Input
1. **Parse Description**: Understand:
   - Primary command purpose
   - Main tasks and workflow
   - Target users
   - Required tools

2. **Classify Complexity**:
   - Simple: Single-step, single-tool (Skip research)
   - Complex: Multi-step, multiple-domain (Proceed to research)

### Phase 1.5: Load Templates (Conditional)

For all commands, first read templates to ensure proper structure:
- Invoke `--templates` flag to load `TEMPLATES.md`
- Reference "Command Templates" section for structure and patterns
- Skip this step only if user explicitly says "skip templates"

### Phase 2: Documentation (Conditional)
For simple commands (analysis, single transformation): Skip to design.
For complex commands (multi-step workflows): Load documentation.

3. **Fetch Latest Docs** (complex only):
   - Claude Code slash commands documentation
   - Available tools and tool capabilities
   - Command structure standards

4. **Review Patterns**: Examine existing command examples

### Phase 3: Design Command
5. **Generate Command Name**:
   - Single-word preferred (e.g., `cleanup`, `parse`, `delegate`)
   - Multi-word when needed for clarity (e.g., `implementation-planner`)
   - Kebab-case format

6. **Determine Tools**: Identify minimal set needed
   - Read, Grep for analysis
   - Write, Edit for modification
   - WebFetch for external data
   - Specialized tools only when required

7. **Craft Description**: Action-oriented, clear purpose

### Phase 4: Build Command
8. **Structure Instructions**:
   - Numbered step-by-step actions
   - Clear variable definitions
   - Input validation
   - Error handling

9. **Define Best Practices**: Domain-specific guidance

10. **Specify Output Format**: Clear structure for results

### Phase 5: Generate File
11. **Create Markdown**: Complete command definition
    - Frontmatter with all required fields
    - Proper YAML syntax
    - Clear sections

12. **Validate Structure**:
    - Frontmatter correctness
    - Tool authorization
    - Step clarity
    - Output format definition

## Best Practices

### Command Design
- **Single Responsibility**: Clear, focused purpose
- **Minimal Tools**: Start with essentials, add only when necessary
- **Clear Naming**: Descriptive kebab-case names
- **Action-Oriented**: Clear indication of what command does

### Documentation
- **Step-by-Step**: Numbered, actionable instructions
- **Input Validation**: Check and validate user input
- **Error Handling**: Handle edge cases explicitly
- **Examples**: Provide concrete usage examples

### Tool Usage
- **Principle of Least Privilege**: Only necessary tools
- **Read Before Write**: Always validate before modifying
- **Clear Intent**: Each tool serves specific purpose

## Security Considerations

- Never generate commands for destructive, malicious, or unauthorized purposes
- Validate all user input before processing
- Handle sensitive data with appropriate restrictions
- Follow safety guidelines for file operations and external access
- Commands must comply with ethical standards

## Examples

### Basic Command: "analyze-logs"
```
Purpose: Analyze application logs for errors
Tools: Read, Grep
Steps: 1) Read log file, 2) Search for errors, 3) Summarize findings
```

### Command with Arguments: "find-duplicates [file-type]"
```
Purpose: Find duplicate files of specific type
Tools: Read, Glob, Grep
Steps: 1) Get file list, 2) Compare hashes, 3) Report duplicates
```

### Complex Multi-Tool Command: "validate-and-format"
```
Purpose: Validate code and apply formatting
Tools: Read, Write, WebFetch (fetch linter config)
Steps: 1) Load config, 2) Validate syntax, 3) Format, 4) Write results
```

## Output Format

Generate a complete markdown file with:

### For Analysis Commands
Include:
- **Summary**: What was analyzed
- **Findings**: Key results
- **Recommendations**: Suggested actions

### For Implementation Commands
Include:
- **Changes Made**: What was modified
- **Validation**: How to verify results
- **Next Steps**: Follow-up actions

### For Simple Commands
Provide:
- Direct response with results
- Clear, organized output
- Next steps if applicable

## Report

After generating the command file:

- **Command**: Name and description
- **Location**: Where file was written
- **Tools**: Authorized tools list
- **Usage**: How to invoke with examples
- **Validation**:
  - [ ] File created in correct location
  - [ ] Frontmatter syntax valid
  - [ ] Tools properly authorized
  - [ ] Instructions clear and testable
  - [ ] Output format defined
