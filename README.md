# DBS Framework

**Direction / Blueprints / Solutions** — a platform-neutral architecture for
reusable AI skills, agents, and workflow systems.

DBS separates workflow decisions, specialized knowledge, and execution. Maintain
one core and adapt it to **Claude, ChatGPT, and Codex** through small platform
adapters. This is an authoring framework, not a hosted agent runtime or scheduler.

**Origin:** this is an unofficial adaptation of
[The DBS Framework Skill by AI Foundations](https://aifoundations.io/resources/the-dbs-framework-skill).
Credit for the original DBS framework and source skill belongs to AI Foundations.
Developed by this repository's maintainer from their original work, this version
adds platform-neutral guidance, separate adapters, modes, and tooling;
it is not an official AI Foundations release or an endorsed project.

**Attribution and permission:** the maintainer confirms that AI Foundations permits
publication of this adaptation with a link to their website and clear source credit.
See [ATTRIBUTION.md](ATTRIBUTION.md) for that record and [LICENSE](LICENSE) for
the separate MIT scope covering new tooling.

## Start here

1. Read [SKILL.md](SKILL.md) or provide it to your AI environment.
2. Use the [Claude](references/platforms/claude.md),
   [ChatGPT](references/platforms/chatgpt.md), or
   [Codex](references/platforms/codex.md) adapter for setup and capability mapping.
3. Ask: “Use DBS in Fast Mode to build a reusable monthly report workflow from a
   supplied CSV. Validate totals and deliver a local PDF. Do not publish it.”
4. Review the resulting contract and run representative tests before relying on it.

For a plain chat, explicitly provide the instructions and required references.
For a skill-aware host, install the package using that host's supported location
or import flow. **Adapters are guidance, not installed integrations.** Tools and
permissions depend on the actual environment. See [validation status](docs/VALIDATION.md).

## The architecture

| Layer | Responsibility | Typical form |
| --- | --- | --- |
| Direction | Trigger, decisions, workflow, acceptance criteria | `SKILL.md` |
| Blueprints | Domain rules, style, schemas, examples | `references/` |
| Solutions | Execution and verifiable outputs | Native tools, plugins/connectors, MCP, APIs, scripts, browser/computer use, file generation |

Use only necessary layers. A production capability may need Direction alone,
Direction + Solutions, or all three. Read [principles](references/dbs-principles.md).

**Fast Mode** produces a complete draft from clear inputs with a consolidated
review. **Interactive Mode** resolves consequential uncertainty through focused
questions. Both preserve the user's authorization and host permissions.

DBS applies to designing reusable capabilities. “Remind me tomorrow,” “run this
existing task,” and one-off edits do not activate it merely because they mention
automation or workflows. An explicit request to use DBS remains supported.

## Repository map

```text
dbs-framework/
├── SKILL.md
├── README.md
├── CONTRIBUTING.md
├── LICENSE
├── ATTRIBUTION.md
├── CHANGELOG.md
├── .gitignore
├── .github/workflows/ci.yml
├── references/
│   ├── dbs-principles.md
│   ├── testing-guide.md
│   └── platforms/{claude,chatgpt,codex}.md
├── templates/
│   ├── generic-skill-template.md
│   ├── claude-skill-template.md
│   ├── chatgpt-skill-template.md
│   └── codex-skill-template.md
├── scripts/{validate_skill,scaffold_skill}.py
├── tests/test_tools.py
└── docs/VALIDATION.md
```

## Generate a starter

Python 3.10+; no third-party packages or network access required. Run from the
repository root (Windows users can substitute `py` for `python` if needed):

```sh
python scripts/scaffold_skill.py monthly-report --output ./examples --platform codex --description "Create monthly reports from supplied CSV data when a report is requested."
python scripts/validate_skill.py ./examples/monthly-report --allow-draft
```

Choose `generic`, `claude`, `chatgpt`, or `codex`. The generator creates a new
directory and refuses an existing destination. It does not install anything or
generate task-specific implementation. Complete the TODOs before normal validation.
Templates carry starter markers intentionally; generated platform packages contain
a local adapter and do not depend on a remote DBS repository at runtime.

Validate this repository and run tests:

```sh
python scripts/validate_skill.py . --repository
python -m unittest discover -s tests -v
```

The validator uses a documented, restricted frontmatter profile, not a full YAML
parser. Read [testing and limitations](references/testing-guide.md) before using
it to check packages with platform-specific metadata.

## Publish and contribute

See [CONTRIBUTING.md](CONTRIBUTING.md) for contribution and compatibility checks.

Published release: [**v1.0.0**](https://github.com/Yasirres/DBS-Framework/releases/tag/v1.0.0),
released on 2026-09-13. Changes after that release are recorded under Unreleased
in [CHANGELOG.md](CHANGELOG.md). Adapted from AI Foundations' DBS
skill architecture guide supplied by the user. The original Direction / Blueprints /
Solutions model and progressive disclosure are preserved; shared instructions are
now platform-neutral.

## License

[MIT](LICENSE) covers only the newly authored Python scripts, Python tests, and
CI configuration. The adapted documentation and templates are not offered under
MIT: the reported permission covers publication with attribution, not MIT
relicensing of the original material. See [ATTRIBUTION.md](ATTRIBUTION.md).
Vendor services and third-party integrations have their own terms.
