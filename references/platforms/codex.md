# Codex adapter

Keep the core neutral. In a local Codex workspace, inspect applicable `AGENTS.md`
instructions, available runtimes, tools, and file permissions before implementation.
Do not assume cloud and desktop tasks share files or installed dependencies.

## Packaging and use

Use the skill location configured for the current Codex environment. A common
project location is `.agents/skills/dbs-framework/`; keep `SKILL.md` and all referenced
resources together. Refresh skill discovery if the host requires it, verify the
skill is listed, and explicitly invoke `$dbs-framework` with a concrete request.
Installation locations can vary; the active host's documentation takes precedence.

Optional `agents/openai.yaml` metadata is a Codex supplement. It is not required
for the neutral core and must not change its business rules. Use the
[Codex template](../../templates/codex-skill-template.md) for generated capabilities.

## Capability mapping

Solutions can use native tools, plugins/connectors, MCP, scripts and CLI tools,
APIs, browser/computer use, and file generation when available. Prefer the existing
project's dependency and test conventions. Preserve unrelated user edits.

Place generated artifacts in the task's output location, run appropriate tests,
and cite real output paths. Local tests do not prove an external action succeeded.
Respect host permissions and the user's authorization for publishing or account
changes. Fast Mode changes conversation pacing, never execution permissions.

## Acceptance smoke test

In a temporary workspace ask DBS to generate a reusable CSV validator skill.
Run its checks with valid and malformed input. Confirm a second generation into
the same location does not overwrite user files. Record environment and commands.

Official reference (reviewed 2026-09-13):
- [OpenAI skill authoring guidance](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
