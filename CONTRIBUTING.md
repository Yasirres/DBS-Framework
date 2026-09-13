# Contributing

Preserve the AI Foundations website link and the statement that this adaptation
was developed from their work, as recorded in [ATTRIBUTION.md](ATTRIBUTION.md).
The reported publication permission is separate from the tooling's MIT license.

Open an issue describing a concrete use case or submit a focused pull request.
Keep Direction / Blueprints / Solutions terminology stable and shared rules in
the core. Put host-specific behavior in its adapter. Do not copy the core into
three platform variants or add a tool dependency just because one exists.

Before a pull request:

1. Use Python 3.10+ and run `python scripts/validate_skill.py . --repository`.
2. Run `python -m unittest discover -s tests -v`.
3. For script changes, add tests for observable behavior and failure modes.
4. For trigger/workflow changes, run affected cases in the
   [testing guide](references/testing-guide.md). Report host and actual outcomes;
   identify any skipped platform checks explicitly.
5. Update relevant docs, official source links, and the changelog. Keep public
   fixtures synthetic and omit credentials, account identifiers, and client data.

Describe the problem, resulting behavior, and validation in the pull request.
New tooling contributions are submitted under the scoped MIT license. Preserve
existing notices and identify third-party material and the permission covering it.
Do not describe all adapted documentation as MIT-licensed.

Use semantic versions: patch for compatible fixes, minor for compatible additions,
major for breaking CLI or contract changes. Adapters may evolve independently in
content but ship with the framework version. Do not claim live compatibility solely
from a structural test. Keep CI permissions read-only unless a reviewed change
requires more. Do not include secrets in public bug reports.
