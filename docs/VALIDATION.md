# Release validation

Version: 1.0.0. This file records local verification, not a published release.

## Verified locally on 2026-09-13

- Host: Windows, Python 3.13.15, standard library only.
- `python scripts/validate_skill.py . --repository`: PASS, zero errors/warnings.
- `python -m unittest discover -s tests -v`: 16 tests passed, none skipped.
- All four scaffold targets produced self-contained drafts, accepted with
  `--allow-draft` and rejected as unfinished without it.
- Tested refusal to overwrite, path/name rejection, Unicode and quoted descriptions,
  malformed metadata, description limits, broken/escaping/case-mismatched links,
  Python syntax errors, symlink refusal, code-example links, and CLI exit codes.
- A direct Codex-target scaffold and draft validation also passed in the workspace.

The tests initially could not use Python's private temporary-directory permissions
inside the restricted Windows host. The suite now supports an explicit
`DBS_TEST_DIR` pointing to a writable fixture location outside the package, and
the final successful run used that setting within the sandbox. No elevated
execution was required for the final successful run. Testing exposed and fixed
two validator issues: code examples being treated as links, and Windows path
resolution concealing filename-case mismatches.

## Not verified or released

The optional installed skill-creator `quick_validate.py` could not start because
its PyYAML dependency is absent in both available Python runtimes. No dependencies
were installed to run it. The repository's dependency-free validator and all 16
tool tests passed as recorded above.

The adapters were reviewed against linked official guidance. Live behavioral
evaluation in Claude and ChatGPT and GitHub-hosted CI has not been performed.
The core was authored in Codex; this is not equivalent to an independent runtime
evaluation of all behavioral cases. Run the protocol in the testing guide for
your actual environment before depending on the generated capability.

The maintainer now confirms permission to publish with AI Foundations' website
link and adaptation credit. This record is based on that confirmation; MIT remains
limited to new tooling. See [ATTRIBUTION.md](../ATTRIBUTION.md).
