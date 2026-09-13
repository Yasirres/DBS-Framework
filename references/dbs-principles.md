# DBS principles

## Direction: the decision and workflow layer

The entrypoint states when to act, what to produce, the workflow, acceptance
criteria, and pointers to knowledge and execution. It should be sufficient to
choose the next step without loading the entire repository. Keep specialized
facts out of it. Trigger descriptions aid selection; they do not guarantee routing.

## Blueprints: the knowledge layer

Use focused reference files for domain rules, schemas, voice, pricing, output
structures, or examples. For volatile facts record source, owner, and verification
date. Load only the file required at the current step. If unavailable, ask for
essential facts or label assumptions; do not fabricate company-specific details.

Public examples must use synthetic data. Keep private customer blueprints in a
separate private location and pass them explicitly when needed.

## Solutions: the execution layer

Solutions includes native tools, plugins, connectors, MCP, APIs, scripts, browser
and computer-use actions, and file generation. It is a role, not a mandatory folder.
A tool invocation may be the whole execution layer. Code belongs in `scripts/`
only when useful; tool contracts can be documented in a reference.

For each operation document:

| Contract field | Example: export a report |
| --- | --- |
| Input | Validated rows and report period |
| Capability and fallback | Available PDF tool; local renderer if supported |
| Authorization | Local output directory; publishing separately scoped |
| Result evidence | Readable PDF path and reconciled totals |
| Failure | Preserve source data; report export error |
| Retry | At most one retry for a transient export failure |
| External write | Use idempotency key or inspect delivery status before retry |

Deterministic calculations and schema validation improve repeatability. Generated
language, images, remote services, and UI operations are not inherently deterministic.
Test their observable output rather than promising identical results.

## Choose only the layers needed

| Layers | Use when | Example |
| --- | --- | --- |
| Direction | A workflow and general knowledge suffice | Structured brainstorming |
| Direction + Blueprints | Domain facts or style must be supplied | House-style editorial review |
| Direction + Solutions | Execution is needed without special domain knowledge | CSV conversion with validation |
| Direction + Blueprints + Solutions | Both specialized rules and execution matter | Branded report with validated totals |

One capability should have one coherent purpose. Split unrelated jobs, not every
step. Platform adapters translate packaging, capability discovery, and result
delivery; they must not fork the shared business logic.

## Example contract

“Build a reusable workflow that turns a supplied sales CSV into a monthly PDF.”

Direction: inspect schema, validate rows, compute totals, render, verify, deliver.
Blueprints: currency rules and layout only if supplied or required.
Solutions: CSV parser, decimal calculations, and available PDF generation.
Acceptance: invalid rows are reported; totals reconcile; PDF opens; no email is sent
unless requested. A scheduler is an optional integration, not implied by “monthly.”
