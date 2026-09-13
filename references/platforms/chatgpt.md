# ChatGPT adapter

Identify the actual ChatGPT surface and its available configuration. Do not infer
skill loading, terminal access, background execution, or integration access from
the model name. A Markdown attachment alone is not proof of skill installation.

## Portable setup

1. Provide the body of the core `SKILL.md` as task instructions, or place it in an
   editable instructions field where the host supports that workflow.
2. Make relevant Blueprints and this adapter accessible as files or supplied text.
   If relative paths cannot be resolved, use their filenames and provide the content.
3. Explicitly request DBS for the reusable capability. Do not rely solely on YAML
   frontmatter for automatic activation in a normal conversation.

For a custom GPT, put behavior in **Instructions** and source material in
**Knowledge**. Test in Preview. For a host offering native skills, follow its
documented skill import process instead of assuming custom-GPT packaging applies.
Use the [ChatGPT template](../../templates/chatgpt-skill-template.md) as an authoring
starter; it is not an automatic GPT installer.

## Capability mapping

Map Solutions only to enabled capabilities: native tools, apps/connectors,
plugins, actions, MCP-backed integrations, code execution, browser/computer use,
or file generation where exposed. Configure required integrations separately.
If no execution capability is available, provide a concrete draft and explain
which execution step remains unperformed. Do not pretend scripts have run.

Knowledge retrieval is host-managed; explicitly surface essential constraints in
instructions and test that necessary references are used. Review generated file
content, provide an actual downloadable artifact when possible, and distinguish
file creation from public publication. A reminder request goes to an available
scheduler; DBS itself creates no schedule or background worker.

## Acceptance smoke test

Ask for a reusable house-style report workflow with a supplied style reference.
Check that the reference influences the draft. Disable an optional execution tool
and check that the output accurately identifies the limitation. Record the surface
and configuration rather than claiming coverage of every ChatGPT environment.

Official references (reviewed 2026-09-13):
- [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-a-gpt)
- [Build skills](https://learn.chatgpt.com/docs/build-skills)
