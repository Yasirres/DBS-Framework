---
name: {{name}}
description: {{description_json}}
---

# {{title}}

## Direction

TODO: Define one concrete input/output contract and observable acceptance criteria.
Activate only for the capability described above. Define near-miss requests that
must use another route. A reminder or scheduled run alone is not a request to build
a new capability.

### Workflow

1. Inspect supplied input and resolve essential missing information.
2. Apply the task's rules and only the relevant Blueprints.
3. Execute required Solutions using actually available capabilities.
4. Verify the output against acceptance criteria and deliver it with test evidence.

### Modes

Fast Mode: build and test the authorized draft from clear inputs, stating material
assumptions. Interactive Mode: resolve consequential choices with focused questions
while continuing independent work. Present concise rationale, not private reasoning.
Neither mode expands authorization.

## Blueprints

TODO: Link needed domain references and their load points, or state that none are needed.

## Solutions

TODO: Define execution inputs, outputs, tool dependencies, permissions, failure and
retry behavior; or state that no execution layer is needed. Options include native
tools, plugins/connectors, MCP, APIs, scripts, browser/computer use, and file generation.

## Validation

TODO: Supply realistic positive, negative-trigger, malformed-input, and unavailable-tool
cases with observable expected outcomes. Report actual results separately from plans.


## Platform adapter

Read the [platform adapter](references/platforms/claude.md) when deploying here.
Identify the Claude host and supported skill loading mechanism. Discover enabled tools before execution.
