# Claude adapter

Keep the shared DBS contract authoritative for architecture. Identify the host:
Claude Code, Claude chat, or an API environment. They do not share every capability.

## Packaging and use

- In Claude Code, place the complete package at
  `.claude/skills/dbs-framework/` for project use, or the documented personal skills
  location for user-wide use. Retain the root `SKILL.md` and referenced directories.
  Invoke `/dbs-framework` and provide the task.
- For Claude chat or API skill loading, use the host's documented import procedure
  if offered. Do not assume copying a local directory installs it in a remote host.
- If skill loading is unavailable, provide the core instructions and the relevant
  references in the conversation. Explicitly request application of DBS.

Use the [Claude template](../../templates/claude-skill-template.md) for new packages.
Its adapter is a packaging supplement, not a second copy of DBS.

## Capability mapping

Check enabled tools and permissions. Map Solutions to available native tools,
MCP, shell, API integrations, browser actions, or artifact generation. A reference
to a tool does not install it. Read only required Blueprints. If the host cannot
read package paths, supply their contents explicitly.

Verify created files before sharing. Separate a generated artifact from a completed
external action. Permission behavior belongs to the host and the user's task scope.

## Acceptance smoke test

Invoke DBS to build a reusable CSV summary capability from a synthetic sample.
Expect an input/output contract, selected layers, a usable draft, and validation
evidence. Then request a simple reminder: it should follow the scheduling route
without creating a new DBS package. Record the host, enabled tools, and outcome.

Official references (reviewed 2026-09-13):
- [Claude Code skills](https://code.claude.com/docs/en/skills)
- [Agent Skills overview](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview)
